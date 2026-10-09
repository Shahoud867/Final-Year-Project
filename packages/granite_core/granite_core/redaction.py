"""PII redaction before anything is stored (FR-SEC-01, NFR-08). Idempotent.

Replaces e-mail addresses, Pakistani CNIC numbers, card-like digit runs and phone numbers with
stable tokens such as ``<EMAIL_1>``. Identical values get identical tokens within one call, so
equality between redacted values is preserved (a check that compares two e-mails still works).
"""

from __future__ import annotations

import re
from collections.abc import Callable
from typing import Any

_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("EMAIL", re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")),
    ("CNIC", re.compile(r"\b\d{5}-\d{7}-\d\b")),
    ("CARD", re.compile(r"\b(?:\d[ -]?){13,19}\b")),
    (
        "PHONE",
        re.compile(r"(?<!\w)(?:\+\d{1,3}[ -]?)?(?:\(\d{2,4}\)[ -]?)?\d{3,4}[ -]\d{3,4}(?:[ -]\d{2,4})?(?!\w)"),
    ),
]


class Redactor:
    def __init__(self) -> None:
        self._seen: dict[tuple[str, str], str] = {}
        self._count: dict[str, int] = {}

    def _token(self, kind: str, value: str) -> str:
        key = (kind, value)
        if key not in self._seen:
            self._count[kind] = self._count.get(kind, 0) + 1
            self._seen[key] = f"<{kind}_{self._count[kind]}>"
        return self._seen[key]

    def _replacer(self, kind: str) -> Callable[[re.Match[str]], str]:
        return lambda m: self._token(kind, m.group(0))

    def text(self, s: str) -> str:
        for kind, pat in _PATTERNS:
            s = pat.sub(self._replacer(kind), s)
        return s

    def value(self, v: Any) -> Any:
        if isinstance(v, str):
            return self.text(v)
        if isinstance(v, list):
            return [self.value(x) for x in v]
        if isinstance(v, dict):
            return {k: self.value(x) for k, x in v.items()}
        return v


def redact(value: Any) -> Any:
    """Redact strings anywhere inside ``value`` (new object; the input is not modified)."""
    return Redactor().value(value)
