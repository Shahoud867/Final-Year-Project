# research/eval

Evaluation of Granite against its baselines (master plan section 27.5). Created now so the structure never changes later; empty until the evaluation design is frozen.

Planned contents (names fixed):
- `prereg-vN.md`: pre-registration (metrics, baselines, thresholds), committed with its date **before** any run
- evaluation scripts sharing one statistics module
- `results/`: one CSV or JSON per run, recording the commit hash
- `ablations/`

Exploratory experiments stay in [`../spikes/`](../spikes/).

## Contents now

- [`prereg-v1.md`](prereg-v1.md): pre-registration of the Mid-1 feasibility validation (written before the run)
- [`validate_refund_desk.py`](validate_refund_desk.py): the study script (resumable; records every model answer)
- [`results/`](results/): raw JSON, generated summary and [notes on how to read them](results/2026-10-07_refund-desk-feasibility-notes.md); `run.log` is the console log
