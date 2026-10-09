"""Source of truth, policy rules and step parsing (TC-WF-*)."""

from __future__ import annotations

import pytest
from granite_core.dsl import MissingFieldError
from granite_core.runner import StepFailed, run_workflow

from refund_desk.steps import _norm, parse_json
from refund_desk.store import RetailStore, find_seed_dir
from tests.conftest import FakeModel

NL, FENCE = chr(10), chr(96) * 3


class TestStore:
    def test_snapshot_loaded(self, store):
        assert len(store.orders) == 75 and len(store.users) == 72
        assert store.version == "taubench_retail_v1"

    def test_catalog_total_rounds_and_sums(self, store):
        order = next(o for o in store.orders.values() if o["status"] == "delivered")
        ids = [i["item_id"] for i in order["items"]]
        assert store.catalog_total(ids) == round(sum(i["price"] for i in order["items"]), 2)

    def test_unknown_item_is_a_missing_field_not_a_crash(self, store):
        with pytest.raises(MissingFieldError):
            store.catalog_price("nope")

    def test_unknown_email_is_missing_field(self, store):
        with pytest.raises(MissingFieldError):
            store.user_id_for_email("nobody@example.com")

    def test_refund_allowed_only_for_delivered_orders_of_that_customer(self, store):
        delivered = next(o for o in store.orders.values() if o["status"] == "delivered")
        owner = store.users[delivered["user_id"]]["email"]
        other = next(u["email"] for uid, u in store.users.items() if uid != delivered["user_id"])
        pending = next(o for o in store.orders.values() if o["status"] == "pending")
        assert store.refund_allowed(delivered["order_id"], owner) is True
        assert store.refund_allowed(delivered["order_id"], other) is False
        assert store.refund_allowed(pending["order_id"], store.users[pending["user_id"]]["email"]) is False

    def test_email_lookup_is_case_insensitive(self, store):
        uid, user = next(iter(store.users.items()))
        assert store.user_id_for_email(user["email"].upper()) == uid

    def test_same_prices_detects_a_changed_price(self):
        items = [{"item_id": "a", "price": 10.0}]
        assert RetailStore.same_prices([{"item_id": "a", "price": 10.0}], items)
        assert not RetailStore.same_prices([{"item_id": "a", "price": 9.75}], items)
        assert not RetailStore.same_prices([{"item_id": "zzz", "price": 10.0}], items)

    def test_fix_prices_restores_catalogue(self, store):
        order = next(o for o in store.orders.values() if o["status"] == "delivered")
        stale = [{**i, "price": 0.01} for i in order["items"]]
        assert [i["price"] for i in store.fix_prices(stale)] == [i["price"] for i in order["items"]]

    def test_examples_are_runnable_and_cover_not_eligible_cases(self, store):
        ex = store.example_tasks(12)
        assert len(ex) == 12
        assert any("(pending)" in e["label"] for e in ex) and any("(cancelled)" in e["label"] for e in ex)
        assert all(e["order_id"] in e["message"] for e in ex)

    def test_seed_dir_override(self, monkeypatch, tmp_path):
        monkeypatch.setenv("GRANITE_SEED_DIR", str(tmp_path))
        assert find_seed_dir() == tmp_path


class TestParsing:
    def test_plain_json(self):
        assert parse_json('{"a": 1}') == {"a": 1}

    def test_json_wrapped_in_prose_or_fences(self):
        assert parse_json("Sure! " + FENCE + "json" + NL + '{"a": 1}' + NL + FENCE + " hope that helps") == {"a": 1}

    @pytest.mark.parametrize("bad", ["no json here", "{broken", "[1, 2]", "", '"just a string"'])
    def test_unusable_replies_fail_the_step(self, bad):
        with pytest.raises(StepFailed):
            parse_json(bad)

    @pytest.mark.parametrize(
        ("raw", "expected"),
        [("The Luggage Set", "luggage set"), ("  my pet beds ", "pet bed"), ("A Tea Kettle", "tea kettle"),
         ("bed", "bed"), ("YOUR Yoga Mat", "yoga mat")],
    )
    def test_item_name_normalisation(self, raw, expected):
        assert _norm(raw) == expected


class TestPolicyAndErrors:
    def test_delivered_order_is_eligible_and_prices_follow_lookup(self, defn, task):
        out = run_workflow(defn, task, FakeModel(), seed=1)
        s2, s3 = out.trace.step("s2"), out.trace.step("s3")
        refunded = {r["item_id"]: r["price"] for r in s3.outputs["items_to_refund"]}
        assert s3.outputs["eligible"] is True and refunded
        assert all(i["price"] == refunded[i["item_id"]] for i in s2.outputs["items"] if i["item_id"] in refunded)

    @pytest.mark.parametrize("status", ["pending", "cancelled"])
    def test_non_delivered_order_is_refused_with_reason_and_no_amount(self, defn, tasks, status):
        t = next(t for t in tasks if f"({status})" in t["label"])
        out = run_workflow(defn, {k: t[k] for k in ("message", "email", "order_id")}, FakeModel(), seed=1)
        s3 = out.trace.step("s3").outputs
        assert out.trace.run.status == "completed"
        assert s3["eligible"] is False and s3["items_to_refund"] == [] and status in s3["reason"]
        assert out.trace.step("s4").outputs["refund_amount"] == 0.0

    def test_someone_elses_order_is_refused(self, defn, task, store):
        other = next(u["email"] for u in store.users.values() if u["email"] != task["email"])
        out = run_workflow(defn, {**task, "email": other}, FakeModel(), seed=1)
        assert out.trace.step("s3").outputs["eligible"] is False
        assert "does not belong" in out.trace.step("s3").outputs["reason"]

    def test_unknown_order_ends_the_run_with_a_clear_error(self, defn, task):
        bad = {**task, "message": task["message"].replace(task["order_id"], "#W0000001")}
        out = run_workflow(defn, bad, FakeModel(), seed=1)
        assert out.trace.run.status == "errored"
        assert "not found" in (out.trace.step("s2").error or "")

    @pytest.mark.parametrize(
        "reply", ["not json", '{"order_id": "12345", "item_names": ["x"]}', '{"order_id": "#W1234567", "item_names": []}']
    )
    def test_unusable_intake_reply_is_an_errored_run_not_a_crash(self, defn, task, reply):
        out = run_workflow(defn, task, FakeModel(intake_reply=reply), seed=1)
        assert out.trace.run.status == "errored" and out.trace.step("s1").error

    def test_model_endpoint_down_is_reported_as_an_error(self, defn, task):
        out = run_workflow(defn, task, FakeModel(fail_after=0), seed=1)
        assert out.trace.run.status == "errored"
        assert "unreachable" in (out.trace.step("s1").error or "")
