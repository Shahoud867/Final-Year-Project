"""Create runs and execute them in the background."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from granite_core.runner import run_workflow
from pydantic import ValidationError
from sqlalchemy.orm import Session, sessionmaker

from ..config import Settings
from ..db import session_scope
from ..errors import ProblemError
from ..jobs import JobHandle
from ..llm_factory import build_provider, resolve_mode
from ..models import Project, Run, new_id
from ..registry import WORKFLOWS, WorkflowEntry
from .analysis import persist_outcome
from .common import audit

RECORDED_HINT = (
    " Recorded mode can only replay the saved example tasks; start Ollama (or set a hosted endpoint) "
    "and use live mode to run your own task."
)


def entry_for(key: str) -> WorkflowEntry:
    """The registry entry of a workflow, or a 404 problem."""
    entry = WORKFLOWS.get(key)
    if entry is None:
        raise ProblemError(404, "Unknown workflow", f"No workflow named '{key}'. Available: {', '.join(WORKFLOWS)}.")
    return entry


def ensure_project(session: Session, entry: WorkflowEntry) -> Project:
    """Return the workflow's project, creating it on first use."""
    pid = f"prj_{entry.key}"
    project = session.get(Project, pid)
    if project is None:
        project = Project(id=pid, name=entry.title, workflow_key=entry.key, description=entry.description)
        session.add(project)
        session.flush()
    return project


def _plain(message: str) -> str:
    """Turn a validator message into a sentence for the form ("Value error, must look like" -> "Must look like")."""
    message = message.removeprefix("Value error, ").replace("String should have", "Enter")
    return message[:1].upper() + message[1:]


def create_run(
    session: Session, settings: Settings, workflow_key: str, task_input: dict[str, Any], fault: str | None,
    seed: int, mode: str | None, actor: str = "analyst",
) -> Run:
    """Validate the task and fault, resolve the model mode and store a queued run."""
    entry = entry_for(workflow_key)
    try:
        clean = entry.validate_task(task_input)
    except ValidationError as exc:
        errors = [{"field": ".".join(str(p) for p in e["loc"]), "message": _plain(str(e["msg"]))} for e in exc.errors()]
        raise ProblemError(422, "Invalid task input", "The task does not match this workflow.", errors=errors) from None
    if fault and fault != "none" and fault not in entry.fault_types:
        raise ProblemError(422, "Unknown fault", f"Available faults: {', '.join(entry.fault_types)}.")
    project = ensure_project(session, entry)
    run = Run(
        id=new_id("run"), project_id=project.id, workflow_key=entry.key, status="queued",
        llm_mode=resolve_mode(settings, mode), model=settings.model, seed=seed,
        fault_type=None if fault in (None, "none") else fault, task_input=clean,
    )
    session.add(run)
    session.flush()
    audit(session, actor, "run_created", "run", run.id, workflow=entry.key, fault=run.fault_type, mode=run.llm_mode)
    return run


def run_job(factory: sessionmaker[Session], settings: Settings, run_id: str) -> Callable[[JobHandle], None]:
    """Return the job that executes the run and stores its analysis."""
    def job(handle: JobHandle) -> None:
        handle.progress(0, 1, "running workflow")
        with session_scope(factory) as s:
            run = s.get(Run, run_id)
            assert run is not None
            run.status = "running"
            entry = entry_for(run.workflow_key)
            mode, task, seed, fault_name, model = run.llm_mode, run.task_input, run.seed, run.fault_type, run.model
        defn = entry.build(model)
        provider = build_provider(settings, mode)
        outcome = run_workflow(
            defn, task, provider, fault=entry.make_fault(fault_name), seed=seed, external_id=run_id
        )
        with session_scope(factory) as s:
            run = s.get(Run, run_id)
            assert run is not None
            persist_outcome(s, run, defn, outcome)
            if run.status == "errored" and "never recorded" in run.error:
                run.error += RECORDED_HINT
        handle.progress(1, 1, "done")

    return job
