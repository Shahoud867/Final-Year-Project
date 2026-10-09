# Verification sequence

What happens when an analyst presses Verify on a hypothesis (`apps/api/granite_api/services/experiments.py` and `granite_core/experiment.py`).

```mermaid
sequenceDiagram
    actor A as Analyst
    participant UI as Web UI
    participant API as API
    participant J as Job runner
    participant X as run_experiment
    participant M as Model provider
    participant DB as Database

    A->>UI: Verify hypothesis (N replays, M controls)
    UI->>API: POST /api/hypotheses/{id}/experiments
    API->>API: refuse if no repair rule exists (422) or the state forbids it (409)
    API->>DB: finding status = verifying; create experiment (queued)
    API-->>UI: 202 with job id
    API->>J: submit job
    loop until the job has finished
        UI->>API: GET /api/jobs/{id}
        API-->>UI: progress k of N+M
    end
    J->>X: run_experiment(trace, step, N, M, seeds)
    loop N replays with the fix, then M controls without it
        X->>M: re-execute only the steps after the suspected step (earlier steps are copied, no model call)
        M-->>X: answers
        X->>X: re-run all checks; judge: target checks pass and nothing that passed now fails
        X-->>J: replay result
        J->>DB: store replay
    end
    X->>X: decide with VR-1 (k of N, c of M, Wilson interval)
    J->>DB: verdict, evidence records (verdict, replays, diff), finding status = confirmed, refuted or inconclusive
    UI->>API: GET /api/findings/{id}
    API-->>UI: status, verdict, evidence with hash check
```

A replay that could not finish (model unreachable, recording missing) is stored as unfinished; if any is unfinished the verdict is ERROR and the finding returns to "hypotheses ready" instead of showing a wrong verdict.
