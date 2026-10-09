"""Safe expression language for checks (ADR-004: AST whitelist, never ``eval``).

Check authors write small Python-looking expressions such as::

    approx(number_in(s5.message), truth.catalog_total(pluck(s3.items_to_refund, 'item_id')))

Only the constructs listed in ``_ALLOWED`` are accepted. There is no attribute access on real
objects (``a.b`` is a dictionary lookup), no calls except to a fixed function table and to
registered ``truth.<name>`` functions, no comprehensions, lambdas, imports, ``**`` or loops, and
hard limits on size and depth. A missing field raises :class:`MissingFieldError`, which the
checks engine reports as ABSTAIN, never as PASS.
"""

from __future__ import annotations

import ast
import math
import re
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Any

MAX_SOURCE_LEN = 500
MAX_NODES = 150
MAX_DEPTH = 14
MAX_STRING_LEN = 200
MAX_LIST_LEN = 10_000


class DSLError(Exception):
    """Base class for all expression-language errors."""


class DSLSyntaxError(DSLError):
    """The expression uses something outside the whitelist (reported at save time)."""


class MissingFieldError(DSLError):
    """A referenced field or source-of-truth entry does not exist. The check ABSTAINs."""


class DSLRuntimeError(DSLError):
    """The expression is valid but cannot be evaluated on this data. The check reports ERROR."""


_ALLOWED: tuple[type[ast.AST], ...] = (
    ast.Expression,
    ast.BoolOp,
    ast.And,
    ast.Or,
    ast.UnaryOp,
    ast.Not,
    ast.USub,
    ast.UAdd,
    ast.BinOp,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Compare,
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
    ast.In,
    ast.NotIn,
    ast.Call,
    ast.Constant,
    ast.Name,
    ast.Attribute,
    ast.Subscript,
    ast.List,
    ast.Tuple,
    ast.Load,
)


def _is_number(x: Any) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _need_numbers(fn: str, *vals: Any) -> None:
    for v in vals:
        if not _is_number(v):
            raise DSLRuntimeError(f"{fn}() needs numbers, got {type(v).__name__}")


_AMOUNT = re.compile(r"\$\s*([0-9][0-9,]*(?:\.[0-9]+)?)")
_NUMBER = re.compile(r"(?<![\w.])([0-9][0-9,]*(?:\.[0-9]+)?)")


def number_in(text: Any) -> float:
    """First ``$`` amount in a text, else its first number. No number -> MissingFieldError."""
    if not isinstance(text, str):
        raise DSLRuntimeError("number_in() needs text")
    m = _AMOUNT.search(text) or _NUMBER.search(text)
    if not m:
        raise MissingFieldError("no number found in text")
    return float(m.group(1).replace(",", ""))


def _pluck(items: Any, key: Any) -> list[Any]:
    if not isinstance(items, list) or not isinstance(key, str):
        raise DSLRuntimeError("pluck() needs a list and a field name")
    out = []
    for it in items:
        if not isinstance(it, Mapping) or key not in it:
            raise MissingFieldError(f"item has no field '{key}'")
        out.append(it[key])
    return out


def _sum(values: Any) -> float:
    if not isinstance(values, list):
        raise DSLRuntimeError("sum() needs a list")
    _need_numbers("sum", *values)
    return float(math.fsum(values))


def _len(x: Any) -> int:
    if not isinstance(x, (list, str)):
        raise DSLRuntimeError("len() needs a list or text")
    return len(x)


def _round(x: Any, n: Any = 2) -> float:
    _need_numbers("round", x, n)
    if not 0 <= n <= 6:
        raise DSLRuntimeError("round() digits must be 0..6")
    return round(float(x), int(n))


def _abs(x: Any) -> float:
    _need_numbers("abs", x)
    return float(abs(x))


def _minmax(fn: Callable[..., Any], name: str, *args: Any) -> Any:
    vals = list(args[0]) if len(args) == 1 and isinstance(args[0], list) else list(args)
    if not vals:
        raise DSLRuntimeError(f"{name}() of nothing")
    _need_numbers(name, *vals)
    return fn(vals)


def _contains(haystack: Any, needle: Any) -> bool:
    if isinstance(haystack, str) and isinstance(needle, str):
        return needle.lower() in haystack.lower()
    if isinstance(haystack, list):
        return needle in haystack
    raise DSLRuntimeError("contains() needs text/text or list/value")


def _all(xs: Any) -> bool:
    if not isinstance(xs, list):
        raise DSLRuntimeError("all() needs a list")
    return all(bool(x) for x in xs)


def _any(xs: Any) -> bool:
    if not isinstance(xs, list):
        raise DSLRuntimeError("any() needs a list")
    return any(bool(x) for x in xs)


# `approx` is handled in the evaluator (it needs the check's tolerance); the rest are plain.
FUNCTIONS: dict[str, Callable[..., Any]] = {
    "sum": _sum,
    "len": _len,
    "round": _round,
    "abs": _abs,
    "min": lambda *a: _minmax(min, "min", *a),
    "max": lambda *a: _minmax(max, "max", *a),
    "contains": _contains,
    "number_in": number_in,
    "pluck": _pluck,
    "all": _all,
    "any": _any,
}
FUNCTION_NAMES = frozenset(FUNCTIONS) | {"approx"}


@dataclass
class EvalOutcome:
    value: Any
    operands: list[Any] | None = None  # the two sides of a top-level comparison or approx()
    resolved: dict[str, Any] = field(default_factory=dict)  # field path -> value actually read
    truth_calls: list[dict[str, Any]] = field(default_factory=list)


def _clip(v: Any) -> Any:
    s = repr(v)
    return v if len(s) <= 300 else s[:300] + "..."


class Expression:
    """A validated expression. Build with :func:`compile_expression`."""

    def __init__(self, source: str, tree: ast.Expression) -> None:
        self.source = source
        self._tree = tree

    def references(self) -> set[str]:
        """Dotted field paths mentioned in the source (``s5.message``), without evaluating."""
        refs: set[str] = set()
        for node in ast.walk(self._tree):
            if isinstance(node, ast.Attribute | ast.Name):
                p = _path_of(node)
                if p and "." in p and p.split(".")[0] != "truth":
                    refs.add(p)
        # keep only maximal paths
        return {r for r in refs if not any(o != r and o.startswith(r + ".") for o in refs)}

    def evaluate(
        self,
        context: Mapping[str, Any],
        truth: Mapping[str, Callable[..., Any]] | None = None,
        tolerance: float = 0.01,
    ) -> EvalOutcome:
        ev = _Evaluator(context, truth or {}, tolerance)
        value = ev.visit(self._tree.body, top=True)
        return EvalOutcome(value, ev.operands, ev.resolved, ev.truth_calls)


def _path_of(node: ast.AST) -> str | None:
    parts: list[str] = []
    while True:
        if isinstance(node, ast.Attribute):
            parts.append(node.attr)
            node = node.value
        elif isinstance(node, ast.Subscript):
            sl = node.slice
            parts.append(f"[{sl.value!r}]" if isinstance(sl, ast.Constant) else "[?]")
            node = node.value
        elif isinstance(node, ast.Name):
            parts.append(node.id)
            break
        else:
            return None
    out = ""
    for p in reversed(parts):
        out += p if p.startswith("[") or not out else "." + p
    return out


def _depth(node: ast.AST) -> int:
    return 1 + max((_depth(c) for c in ast.iter_child_nodes(node)), default=0)


def compile_expression(source: str) -> Expression:
    """Parse and validate. Raises :class:`DSLSyntaxError` with a reason the author can act on."""
    if not isinstance(source, str) or not source.strip():
        raise DSLSyntaxError("expression is empty")
    if len(source) > MAX_SOURCE_LEN:
        raise DSLSyntaxError(f"expression longer than {MAX_SOURCE_LEN} characters")
    try:
        tree = ast.parse(source.strip(), mode="eval")
    except (SyntaxError, ValueError, RecursionError, MemoryError) as e:
        raise DSLSyntaxError(f"not a valid expression: {e}") from None
    nodes = list(ast.walk(tree))
    if len(nodes) > MAX_NODES:
        raise DSLSyntaxError(f"expression has more than {MAX_NODES} parts")
    if _depth(tree) > MAX_DEPTH:
        raise DSLSyntaxError(f"expression nested deeper than {MAX_DEPTH} levels")
    for node in nodes:
        _validate_node(node)
    return Expression(source.strip(), tree)


def _v_constant(node: ast.Constant) -> None:
    v = node.value
    if not (v is None or isinstance(v, (bool, int, float, str))):
        raise DSLSyntaxError("only numbers, text, true/false and None are allowed as constants")
    if isinstance(v, str) and len(v) > MAX_STRING_LEN:
        raise DSLSyntaxError("text constant too long")
    if isinstance(v, (int, float)) and not isinstance(v, bool) and abs(v) > 1e12:
        raise DSLSyntaxError("number constant too large")


def _v_name(node: ast.Name) -> None:
    if node.id.startswith("_"):
        raise DSLSyntaxError("names starting with '_' are not allowed")


def _v_attribute(node: ast.Attribute) -> None:
    if node.attr.startswith("_"):
        raise DSLSyntaxError("fields starting with '_' are not allowed")


def _v_call(node: ast.Call) -> None:
    if node.keywords:
        raise DSLSyntaxError("keyword arguments are not allowed")
    f = node.func
    ok_name = isinstance(f, ast.Name) and f.id in FUNCTION_NAMES
    ok_truth = isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name) and f.value.id == "truth"
    if not (ok_name or ok_truth):
        raise DSLSyntaxError(
            "only these functions may be called: " + ", ".join(sorted(FUNCTION_NAMES)) + ", truth.<name>"
        )
    if any(isinstance(a, ast.Starred) for a in node.args):
        raise DSLSyntaxError("starred arguments are not allowed")


def _v_subscript(node: ast.Subscript) -> None:
    sl = node.slice
    if not (isinstance(sl, ast.Constant) and isinstance(sl.value, (int, str)) and not isinstance(sl.value, bool)):
        raise DSLSyntaxError("only a constant index or key is allowed inside [...]")


def _v_compare(node: ast.Compare) -> None:
    if len(node.ops) != 1:
        raise DSLSyntaxError("chained comparisons are not allowed; use 'and'")


_NODE_VALIDATORS: dict[type[ast.AST], Callable[[Any], None]] = {
    ast.Constant: _v_constant,
    ast.Name: _v_name,
    ast.Attribute: _v_attribute,
    ast.Call: _v_call,
    ast.Subscript: _v_subscript,
    ast.Compare: _v_compare,
}


def _validate_node(node: ast.AST) -> None:
    if not isinstance(node, _ALLOWED):
        raise DSLSyntaxError(f"'{type(node).__name__}' is not allowed in check expressions")
    check = _NODE_VALIDATORS.get(type(node))
    if check is not None:
        check(node)


class _Evaluator:
    def __init__(self, ctx: Mapping[str, Any], truth: Mapping[str, Callable[..., Any]], tol: float) -> None:
        self.ctx, self.truth, self.tol = ctx, truth, tol
        self.operands: list[Any] | None = None
        self.resolved: dict[str, Any] = {}
        self.truth_calls: list[dict[str, Any]] = []

    # -- dispatch ------------------------------------------------------------------------
    def visit(self, node: ast.AST, top: bool = False) -> Any:
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, (ast.Name, ast.Attribute, ast.Subscript)):
            return self._path(node)
        if isinstance(node, (ast.List, ast.Tuple)):
            if len(node.elts) > MAX_LIST_LEN:
                raise DSLRuntimeError("list too long")
            return [self.visit(e) for e in node.elts]
        if isinstance(node, ast.BoolOp):
            vals = [self.visit(v) for v in node.values]
            return all(bool(v) for v in vals) if isinstance(node.op, ast.And) else any(bool(v) for v in vals)
        if isinstance(node, ast.UnaryOp):
            v = self.visit(node.operand)
            if isinstance(node.op, ast.Not):
                return not v
            _need_numbers("unary -", v)
            return -v if isinstance(node.op, ast.USub) else v
        if isinstance(node, ast.BinOp):
            return self._binop(node)
        if isinstance(node, ast.Compare):
            return self._compare(node, top)
        if isinstance(node, ast.Call):
            return self._call(node, top)
        raise DSLRuntimeError(f"cannot evaluate {type(node).__name__}")  # pragma: no cover

    def _path(self, node: ast.AST) -> Any:
        p = _path_of(node)
        if p is None:
            raise DSLRuntimeError("only plain field paths can be read")
        # walk the chain from the root name
        chain: list[ast.AST] = []
        cur: ast.AST = node
        while not isinstance(cur, ast.Name):
            chain.append(cur)
            cur = cur.value  # type: ignore[attr-defined]
        name = cur.id
        if name == "truth":
            raise DSLRuntimeError("'truth' can only be called, e.g. truth.price(x)")
        if name not in self.ctx:
            raise MissingFieldError(f"'{name}' is not available in this run")
        val: Any = self.ctx[name]
        for link in reversed(chain):
            if isinstance(link, ast.Attribute):
                key: Any = link.attr
            else:
                key = link.slice.value  # type: ignore[attr-defined]
            if isinstance(val, Mapping) and isinstance(key, str):
                if key not in val:
                    raise MissingFieldError(f"field '{key}' is missing (reading {p})")
                val = val[key]
            elif isinstance(val, list) and isinstance(key, int):
                if not -len(val) <= key < len(val):
                    raise MissingFieldError(f"index {key} is out of range (reading {p})")
                val = val[key]
            else:
                raise DSLRuntimeError(f"cannot read '{key}' from a {type(val).__name__} (reading {p})")
        self.resolved[p] = _clip(val)
        return val

    def _binop(self, node: ast.BinOp) -> float:
        a, b = self.visit(node.left), self.visit(node.right)
        _need_numbers("arithmetic", a, b)
        try:
            if isinstance(node.op, ast.Add):
                return float(a + b)
            if isinstance(node.op, ast.Sub):
                return float(a - b)
            if isinstance(node.op, ast.Mult):
                return float(a * b)
            return float(a / b)
        except ZeroDivisionError:
            raise DSLRuntimeError("division by zero") from None

    def _compare(self, node: ast.Compare, top: bool) -> bool:
        a, b = self.visit(node.left), self.visit(node.comparators[0])
        if top:
            self.operands = [_clip(a), _clip(b)]
        op = node.ops[0]
        try:
            if isinstance(op, ast.Eq):
                return bool(a == b)
            if isinstance(op, ast.NotEq):
                return bool(a != b)
            if isinstance(op, ast.In):
                return bool(a in b)
            if isinstance(op, ast.NotIn):
                return bool(a not in b)
            if _is_number(a) != _is_number(b):
                raise DSLRuntimeError("cannot order a number and a non-number")
            if isinstance(op, ast.Lt):
                return bool(a < b)
            if isinstance(op, ast.LtE):
                return bool(a <= b)
            if isinstance(op, ast.Gt):
                return bool(a > b)
            return bool(a >= b)
        except TypeError:
            raise DSLRuntimeError("values cannot be compared") from None

    def _call(self, node: ast.Call, top: bool) -> Any:
        f = node.func
        args = [self.visit(a) for a in node.args]
        if isinstance(f, ast.Attribute):  # truth.<name>(...)
            fn = self.truth.get(f.attr)
            if fn is None:
                raise DSLRuntimeError(f"unknown source-of-truth function 'truth.{f.attr}'")
            try:
                out = fn(*args)
            except DSLError:
                raise
            except (KeyError, LookupError) as e:
                raise MissingFieldError(f"truth.{f.attr}: {e}") from None
            except Exception as e:  # truth source misbehaving is an ERROR, never a PASS
                raise DSLRuntimeError(f"truth.{f.attr} failed: {type(e).__name__}") from None
            self.truth_calls.append({"function": f.attr, "arguments": _clip(args), "returned": _clip(out)})
            return out
        assert isinstance(f, ast.Name)
        if f.id == "approx":
            if len(args) not in (2, 3):
                raise DSLRuntimeError("approx(a, b[, tolerance]) takes 2 or 3 arguments")
            a, b = args[0], args[1]
            tol = args[2] if len(args) == 3 else self.tol
            _need_numbers("approx", a, b, tol)
            if top:
                self.operands = [_clip(a), _clip(b)]
            return abs(a - b) <= tol + 1e-9
        try:
            return FUNCTIONS[f.id](*args)
        except TypeError:
            raise DSLRuntimeError(f"wrong number of arguments for {f.id}()") from None
