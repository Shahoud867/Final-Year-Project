# data

| Path | Holds |
|---|---|
| `raw/` | third-party datasets exactly as downloaded (read-only reference) |
| `seed/` | small curated, licence-attributed snapshots a workflow needs at runtime, e.g. the tau-bench retail truth snapshot (created on first use) |
| `benchmark/vN/` | Granite's generated benchmark, with a datasheet (created on first use) |
| [`datasets.md`](datasets.md) | register: licences, which datasets are active vs benched, and why |
| [`DOWNLOAD.md`](DOWNLOAD.md) | source, licence and retrieval command for each dataset |

Never grep `raw/` (about 1,100 files). It is still tracked in git; the decision to untrack it, and the GAIA redistribution concern, are described in `DOWNLOAD.md` and the master plan.
