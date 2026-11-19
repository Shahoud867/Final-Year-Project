"""Regression export: a confirmed finding becomes a case file and a pytest module, downloaded as one zip (F17)."""

from __future__ import annotations

import io
import zipfile

from granite_core.regression import RegressionCase, render_pytest, safe_name

from ..errors import ProblemError
from ..models import Finding
from ..registry import WORKFLOWS

README = """Granite regression test for finding {finding}

  pip install granite-core  (and the workflow package, here: {module})
  pytest {stem}.py

The first test checks that the stored failing run still fails its checks. The second runs the workflow on the same
task and passes once the cause is fixed. To see it fail while the cause is present, re-inject the fault:

  GRANITE_REGRESSION_FAULT=<fault name> pytest {stem}.py

Model answers come from GRANITE_CASSETTE (a recording); without one the second test cannot run offline.
"""


def build_case(f: Finding) -> RegressionCase:
    """The regression case of a finding whose origin was confirmed by replay; 409 otherwise."""
    confirmed = [(h, e) for h in f.hypotheses for e in h.experiments if e.verdict == "confirmed"]
    if not confirmed:
        raise ProblemError(409, "No confirmed origin",
                           "Export needs an origin confirmed by replay. Verify or investigate the finding first.")
    hyp, exp = confirmed[-1]
    run = f.run
    if run.trace is None or not run.trace_sha256:
        raise ProblemError(409, "No trace", "The run behind this finding has no stored trace.")
    entry = WORKFLOWS[run.workflow_key]
    return RegressionCase(
        finding_id=f.id, title=f.title, workflow=run.workflow_key, workflow_module=entry.module, model=run.model,
        seed=run.seed, task_input=dict(run.task_input), target_checks=[f.check_id] if f.check_id else [],
        origin_step=hyp.step_id, origin_agent=hyp.agent, intervention=exp.intervention or {},
        verdict=exp.summary or {}, trace_sha256=run.trace_sha256, failing_trace=run.trace,
    )


def regression_zip(f: Finding) -> tuple[str, bytes]:
    """File name and bytes of the zip holding the case JSON, the pytest module and a short README."""
    case = build_case(f)
    if not case.target_checks:
        raise ProblemError(409, "Nothing to test", "This finding has no failed outcome check to turn into a test.")
    stem = safe_name("test_granite_" + f.id)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(f"{stem}.json", case.model_dump_json(indent=1))
        z.writestr(f"{stem}.py", render_pytest(case))
        z.writestr("README.txt", README.format(finding=f.id, module=case.workflow_module, stem=stem))
    return f"{stem}.zip", buf.getvalue()


__all__ = ["build_case", "regression_zip"]
