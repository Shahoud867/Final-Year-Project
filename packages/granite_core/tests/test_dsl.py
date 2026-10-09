"""Check-expression language: behaviour, and the malicious-expression suite (TC-CHK-04, TC-CHK-SEC)."""

from __future__ import annotations

import math

import pytest
from hypothesis import example, given, settings
from hypothesis import strategies as st

from granite_core.dsl import (
    DSLRuntimeError,
    DSLSyntaxError,
    MissingFieldError,
    compile_expression,
    number_in,
)

CTX = {
    "task": {"email": "a@example.com"},
    "s1": {"names": ["lamp", "mug"], "n": 2},
    "s2": {"items": [{"id": "a", "price": 10.5}, {"id": "b", "price": 4.25}], "status": "delivered"},
    "s5": {"message": "Your refund of $14.75 is on its way"},
}


def ev(src: str, truth: dict | None = None, tol: float = 0.01):
    return compile_expression(src).evaluate(CTX, truth, tol).value


# ---- behaviour ------------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "src,expected",
    [
        ("1 + 2 * 3", 7),
        ("s1.n == 2", True),
        ("s2.status == 'delivered' and s1.n > 1", True),
        ("not (s1.n < 1)", True),
        ("sum(pluck(s2.items, 'price'))", 14.75),
        ("len(s1.names)", 2),
        ("round(10 / 3, 2)", 3.33),
        ("contains(s5.message, 'REFUND')", True),
        ("number_in(s5.message)", 14.75),
        ("s2.items[0].price", 10.5),
        ("s2.items[1]['id'] == 'b'", True),
        ("min(3, 1, 2)", 1),
        ("max(pluck(s2.items, 'price'))", 10.5),
        ("all([1 == 1, 2 == 2])", True),
        ("any([1 == 2, 2 == 2])", True),
        ("-s1.n + 5", 3),
        ("'lamp' in s1.names", True),
    ],
)
def test_valid_expressions(src: str, expected: object) -> None:
    assert ev(src) == expected


def test_approx_uses_check_tolerance_and_reports_operands() -> None:
    out = compile_expression("approx(s2.items[0].price, 10.51)").evaluate(CTX, None, 0.02)
    assert out.value is True and out.operands == [10.5, 10.51]
    assert compile_expression("approx(10.5, 10.51)").evaluate(CTX, None, 0.001).value is False
    assert compile_expression("approx(10.5, 10.9, 0.5)").evaluate(CTX, None, 0.001).value is True


def test_truth_function_is_called_and_recorded() -> None:
    out = compile_expression("truth.price('a') == 10.5").evaluate(CTX, {"price": lambda k: 10.5}, 0.01)
    assert out.value is True
    assert out.truth_calls == [{"function": "price", "arguments": ["a"], "returned": 10.5}]


def test_resolved_values_are_recorded_for_evidence() -> None:
    out = compile_expression("s1.n + s2.items[0].price > 0").evaluate(CTX, None, 0.01)
    assert out.resolved["s1.n"] == 2 and out.resolved["s2.items[0].price"] == 10.5


def test_references_lists_maximal_paths() -> None:
    refs = compile_expression("approx(number_in(s5.message), sum(pluck(s2.items, 'price')))").references()
    assert refs == {"s5.message", "s2.items"}


# ---- abstain / error semantics (never a silent pass) --------------------------------------------------------


@pytest.mark.parametrize(
    "src", ["s9.x == 1", "s1.missing == 1", "s2.items[7].price > 0", "number_in('no digits here')"]
)
def test_missing_data_raises_missing_field(src: str) -> None:
    with pytest.raises(MissingFieldError):
        ev(src)


def test_missing_truth_entry_is_missing_not_error() -> None:
    with pytest.raises(MissingFieldError):
        ev("truth.price('zzz') == 1", {"price": lambda k: {}[k]})


@pytest.mark.parametrize(
    "src", ["1 / 0", "'a' + 1", "sum(5)", "len(3)", "s1.n < 'x'", "round(1.5, 99)", "truth.nope(1)"]
)
def test_unevaluable_expressions_are_runtime_errors(src: str) -> None:
    with pytest.raises(DSLRuntimeError):
        ev(src, {})


def test_broken_truth_source_is_an_error_not_a_pass() -> None:
    def boom(_: str) -> float:
        raise ConnectionError("db down")

    with pytest.raises(DSLRuntimeError):
        ev("truth.price('a') == 1", {"price": boom})


def test_number_in_prefers_dollar_amount_and_handles_commas() -> None:
    assert number_in("Order 12345: refund $1,234.50 today") == 1234.5
    assert number_in("about 7 items") == 7.0


# ---- malicious expressions: every one must be rejected at save time ---------------------------------------


MALICIOUS = [
    "__import__('os').system('echo pwned')",
    "().__class__.__bases__[0].__subclasses__()",
    "(lambda: 1)()",
    "[x for x in range(10)]",
    "{x: 1 for x in s1.names}",
    "s1.__class__",
    "open('/etc/passwd').read()",
    "eval('1+1')",
    "exec('import os')",
    "2 ** 99999999",
    "(y := 5)",
    "f'{s1.n}'",
    "s1.names[0:1]",
    "approx(1, 1, tolerance=2)",
    "'a' * 10 ** 9",
    "{'a': 1}",
    "{1, 2}",
    "import os",
    "getattr(s1, 'n')",
    "print(1)",
    "str(1)",
    "s1.n if s1.n else 0",
    "1 < s1.n < 3",
    "sum(*s1.names)",
    "_hidden.x == 1",
    "truth",  # allowed to parse; the evaluator refuses to read it (see below)
]


@pytest.mark.parametrize("src", [m for m in MALICIOUS if m != "truth"])
def test_malicious_expressions_are_rejected(src: str) -> None:
    with pytest.raises(DSLSyntaxError):
        compile_expression(src)


def test_bare_truth_cannot_be_read() -> None:
    with pytest.raises(DSLRuntimeError):
        ev("truth", {})


@pytest.mark.parametrize("src", ["", "   ", "1 +", "-(" * 40 + "1" + ")" * 40, "x" * 501, "1 + " * 80 + "1"])
def test_empty_malformed_or_oversized_expressions_are_rejected(src: str) -> None:
    with pytest.raises(DSLSyntaxError):
        compile_expression(src)


def test_redundant_parentheses_are_harmless() -> None:
    assert ev("(" * 60 + "1" + ")" * 60) == 1  # parentheses add no AST depth; only nested operations count


def test_huge_constants_are_rejected() -> None:
    with pytest.raises(DSLSyntaxError):
        compile_expression("1e30 == 1")
    with pytest.raises(DSLSyntaxError):
        compile_expression("'" + "a" * 300 + "' == 'b'")


# ---- property tests ---------------------------------------------------------------------------------------


@given(st.text(max_size=120))
@settings(max_examples=300, deadline=None)
def test_arbitrary_text_never_crashes_the_compiler(src: str) -> None:
    """Whatever a user types, compile either succeeds or raises DSLSyntaxError, nothing else."""
    try:
        compile_expression(src)
    except DSLSyntaxError:
        pass


_num = st.integers(min_value=-1000, max_value=1000)


@given(st.lists(_num, min_size=2, max_size=6), st.lists(st.sampled_from(["+", "-", "*"]), min_size=5, max_size=5))
@example(nums=[255, 425, 425, 457, 627, 683], ops=["*", "*", "*", "*", "*"])  # product beyond 2**53 (found by Hypothesis)
@settings(max_examples=200, deadline=None)
def test_arithmetic_agrees_with_python(nums: list[int], ops: list[str]) -> None:
    """DSL arithmetic is IEEE double by design (money is compared with tolerances), so agree up to float error."""
    src = str(nums[0])
    for n, op in zip(nums[1:], ops, strict=False):
        src += f" {op} ({n})"
    expected = eval(src)  # noqa: S307 - test-only oracle on integers we generated
    assert math.isclose(ev(src), expected, rel_tol=1e-12, abs_tol=1e-9)
