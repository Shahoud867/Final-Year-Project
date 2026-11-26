"""Regression export on the real workflow: the exported test fails while the cause is present (TC-EXP)."""

from __future__ import annotations

import subprocess
import sys

import pytest
from granite_core.checks import CheckStatus, derive_findings, evaluate_checks
from granite_core.evidence import sha256_of
from granite_core.experiment import run_experiment
from granite_core.regression import RegressionCase, evaluate_case, render_pytest, run_case, safe_name
from granite_core.runner import run_workflow

from refund_desk import make_fault
from tests.conftest import FakeModel


@pytest.fixture
def case(defn, task):
    out = run_workflow(defn, task, FakeModel(), fault=make_fault("stale_price"), seed=1)
    results = evaluate_checks(out.trace, defn.checks, defn.truth())
    finding = derive_findings(out.trace, results)[0]
    exp = run_experiment(defn, out.trace, "s2", FakeModel(), n=5, m=2, target_check_ids=[finding.check_id])
    trace = out.trace.model_dump(mode="json")
    return RegressionCase(
        finding_id="fnd_test01", title=finding.title, workflow="refund_desk", workflow_module="refund_desk",
        model="fake", seed=1, task_input=task, target_checks=[finding.check_id], origin_step="s2",
        origin_agent="Order Lookup", intervention=exp.intervention.model_dump(mode="json"),
        verdict=exp.summary.model_dump(mode="json"), trace_sha256=sha256_of(trace), failing_trace=trace,
    )


def test_stored_failure_still_fails_its_check(case):
    assert [r.status for r in evaluate_case(case, case.failing_trace)] == [CheckStatus.FAIL]


def test_fixed_system_passes_and_reinjected_fault_fails(case):
    assert [r.status for r in run_case(case, llm=FakeModel())] == [CheckStatus.PASS]
    assert [r.status for r in run_case(case, llm=FakeModel(), fault="stale_price")] == [CheckStatus.FAIL]


def test_case_round_trips_and_rejects_unknown_fields(case):
    again = RegressionCase.model_validate_json(case.model_dump_json())
    assert again == case
    with pytest.raises(ValueError):
        RegressionCase.model_validate({**case.model_dump(), "surprise": 1})


def test_rendered_module_is_valid_python_and_names_the_finding(case):
    source = render_pytest(case.model_copy(update={"title": 'tricky """ title \\ with\nnewline'}))
    compile(source, "test_granite_fnd_test01.py", "exec")
    assert "fnd_test01" in source and "Order Lookup" in source


def test_exported_files_run_under_pytest(case, tmp_path):
    """The two exported files, run by pytest in a fresh process with recorded answers unavailable to the fake model:
    the stored-failure test passes; the live re-run needs a model, so only the first test is selected here."""
    stem = safe_name("test_granite_" + case.finding_id)
    (tmp_path / f"{stem}.json").write_text(case.model_dump_json(), encoding="utf-8")
    (tmp_path / f"{stem}.py").write_text(render_pytest(case), encoding="utf-8")
    done = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(tmp_path / f"{stem}.py"),
         "-k", "recorded_failure"],
        capture_output=True, text=True, cwd=tmp_path, check=False,
    )
    assert done.returncode == 0, done.stdout + done.stderr
