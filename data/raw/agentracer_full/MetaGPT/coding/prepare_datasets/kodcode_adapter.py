"""
Adapter version of kodcode.py that skips the sandbox-fusion (Docker) reference-solution
validation step -- Docker Desktop is not available in this environment. Trusts
KodCode-Light-RL-10K's own published solutions/tests directly instead of re-verifying
them locally. Pulls hard+medium difficulty (public, ungated HF dataset) and downsamples
to a target count so that, combined with the 378-task MBPP+ adapter output, the total
task pool reaches ~2,000.
"""
import argparse
import pathlib

import datasets

# Same block-list as the original kodcode.py -- skip tasks whose reference solution or
# test needs a library unlikely to be available/runnable in this local setup.
block_libs = [
    "fake-useragent", "keras", "socket", "torch", "scipy", "sklearn", "cv2",
    "imageio", "sphinx-pyproject", "xgboost", "tweepy", "flask", "matplotlib",
    "pillow", "seaborn", "smtpd", "pandas", "bs4",
]

_EMPTY_RETURN_ = {
    "data_source": "kodcode",
    "task_id": None,
    "question": None,
    "test": None,
    "entry_point": None,
    "reference_solution": None,
}


def process_fn(example):
    reference_solution = example["solution"]
    test_code = "from solution import *\n" + example["test"].strip()
    if any(lib in reference_solution for lib in block_libs):
        return _EMPTY_RETURN_
    if any(lib in test_code for lib in block_libs):
        return _EMPTY_RETURN_
    question = (
        f"Please solve the programming task below in Python using a multi-agent "
        f"cooperation.\n\n{example['question'].strip()}"
    )
    test_declaration = example["test_info"][0]["function_declaration"].strip()
    if test_declaration:
        question += f"\n\nNote that the function declaration is {test_declaration}."
    return {
        "data_source": "kodcode",
        "task_id": example["question_id"],
        "question": question,
        "test": test_code,
        "entry_point": test_declaration,
        "reference_solution": reference_solution,
    }


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--save_dir", default="datasets/code/")
    argparser.add_argument(
        "--target", type=int, default=1622,
        help="rows to keep after difficulty filter + shuffle (378 mbppplus + this = ~2000)",
    )
    argparser.add_argument("--seed", type=int, default=42)
    args = argparser.parse_args()

    dataset = datasets.load_dataset("KodCode/KodCode-Light-RL-10K", split="train")
    dataset = dataset.filter(lambda x: x["gpt_difficulty"] in ("hard", "medium"))
    dataset = dataset.shuffle(seed=args.seed)

    dataset = dataset.map(
        function=process_fn, remove_columns=dataset.column_names
    ).filter(lambda x: x["task_id"] is not None)

    if len(dataset) > args.target:
        dataset = dataset.select(range(args.target))

    save_path = pathlib.Path(args.save_dir) / "kodcode-hardmedium.parquet"
    save_path.parent.mkdir(parents=True, exist_ok=True)
    dataset.to_parquet(save_path)
    print(f"Saved {len(dataset)} tasks to {save_path}")
