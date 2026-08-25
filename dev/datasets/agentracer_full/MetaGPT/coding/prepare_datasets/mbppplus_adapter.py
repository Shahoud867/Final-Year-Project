"""
Adapter: reshape the project's already-downloaded MBPP+ (378 tasks, evalplus/mbppplus)
into the parquet schema run_rollout.py expects (data_source/task_id/question/test/
entry_point/reference_solution). Bypasses kodcode.py's sandbox-fusion (Docker) validation
step entirely -- MBPP+'s own reference solutions and tests are already trusted/verified
upstream by EvalPlus, so no local re-validation is performed here.
"""
import argparse
import pathlib
import re

import pyarrow as pa
import pyarrow.ipc as ipc
import pyarrow.parquet as pq


def extract_entry_point(code: str) -> str:
    match = re.search(r"^def (\w+)\(", code, re.MULTILINE)
    return match.group(1) if match else ""


def process_row(row: dict) -> dict:
    entry_point = extract_entry_point(row["code"])
    question = (
        f"Please solve the programming task below in Python using a multi-agent cooperation.\n\n"
        f"{row['prompt'].strip()}"
    )
    if entry_point:
        question += f"\n\nNote that the function name must be `{entry_point}`."
    test_imports = row["test_imports"] or []
    test_code = "\n".join(test_imports) + "\n" + row["test"]
    return {
        "data_source": "mbppplus",
        "task_id": str(row["task_id"]),
        "question": question,
        "test": test_code,
        "entry_point": entry_point,
        "reference_solution": row["code"],
    }


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "--source_dir",
        default=str(
            pathlib.Path(__file__).resolve().parents[4] / "mbppplus"
        ),
    )
    argparser.add_argument("--save_dir", default="datasets/code/")
    args = argparser.parse_args()

    arrow_path = pathlib.Path(args.source_dir) / "test" / "data-00000-of-00001.arrow"
    with pa.memory_map(str(arrow_path), "r") as source:
        table = ipc.open_stream(source).read_all()
    rows = table.to_pylist()

    out_rows = [process_row(r) for r in rows]
    out_table = pa.Table.from_pylist(out_rows)

    save_path = pathlib.Path(args.save_dir) / "mbppplus-full.parquet"
    save_path.parent.mkdir(parents=True, exist_ok=True)
    pq.write_table(out_table, save_path)
    print(f"Saved {len(out_rows)} tasks to {save_path}")
