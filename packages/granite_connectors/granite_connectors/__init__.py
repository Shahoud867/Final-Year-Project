"""Granite connectors: bring traces in from observability platforms and send verdicts back.

The package depends on ``granite_core`` and the standard library only. Every platform is turned into the neutral
:class:`~granite_connectors.spans.SpanRecord` first, then :func:`~granite_connectors.mapping.map_trace` builds a
Granite Trace v1 from it (docs/plan/integrations-strategy.md, ADR-012).
"""

from .export import hex_id, trace_to_spans
from .http import ConnectorError, HttpClient
from .langfuse import LangfuseClient
from .mapping import MAPPER_VERSION, Edge, MappedTrace, map_trace
from .phoenix import PhoenixClient
from .spans import READS_KEY, STEP_KEY, Profile, SpanRecord

__all__ = [
    "MAPPER_VERSION", "READS_KEY", "STEP_KEY", "ConnectorError", "Edge", "HttpClient", "LangfuseClient",
    "MappedTrace", "PhoenixClient", "Profile", "SpanRecord", "hex_id", "map_trace", "trace_to_spans",
]
