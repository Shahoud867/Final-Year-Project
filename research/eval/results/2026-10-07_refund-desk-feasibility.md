# Refund Desk feasibility validation, 2026-10-07

Protocol: `research/eval/prereg-v1.md` (SHA-256 `63fd0a25a5c1e1dd`). Model llama3.2:3b. HEAD `46a591165e`, working tree dirty: True.

| Metric | Result |
|---|---|
| M1 detection (faulty runs) | 10/10 (100%, 95% CI 72%-100%) |
| M2 clean runs with a finding | 1/10 (10%, 95% CI 2%-40%) |
| M3 attribution top-1 | 10/10 (100%, 95% CI 72%-100%) |
| M3 attribution top-3 | 10/10 (100%, 95% CI 72%-100%) |
| M4 origin CONFIRMED | 9/10 (90%, 95% CI 60%-98%) |
| M5 innocent step REFUTED | 10/10 (100%, 95% CI 72%-100%) |
| M6 runs completed | 20/20 (100%, 95% CI 84%-100%) |

## Per task

| Order | Clean run findings | Faulty: ranking | Origin verdict | Innocent verdict |
|---|---|---|---|---|
| #W1023987 | 0 | s2, s4, s1, s3, s5 | confirmed 5/5 | refuted 0/5 |
| #W1052399 | 0 | s2, s1, s3, s4, s5 | confirmed 5/5 | refuted 0/5 |
| #W1067251 | 0 | s2, s1, s3, s4, s5 | confirmed 5/5 | refuted 0/5 |
| #W1166549 | 0 | s2, s1, s3, s4, s5 | confirmed 5/5 | refuted 0/5 |
| #W1326557 | 0 | s2, s1, s3, s4, s5 | refuted 0/5 | refuted 0/5 |
| #W1335809 | 1 | s2, s4, s1, s3, s5 | confirmed 5/5 | refuted 0/5 |
| #W1341845 | 0 | s2, s1, s3, s4, s5 | confirmed 5/5 | refuted 0/5 |
| #W1504875 | 0 | s2, s1, s3, s4, s5 | confirmed 5/5 | refuted 0/5 |
| #W1519594 | 0 | s2, s1, s3, s4, s5 | confirmed 5/5 | refuted 0/5 |
| #W1523776 | 0 | s2, s1, s3, s4, s5 | confirmed 5/5 | refuted 0/5 |
