"""Summarize message labels in a CSV file and save a run report."""

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import platform
import sys


def describe(input_path):
    raw = input_path.read_bytes()
    rows = csv.DictReader(io.StringIO(raw.decode("utf-8"), newline=""))
    if rows.fieldnames != ["message_id", "text", "label"]:
        raise ValueError("Expected columns: message_id,text,label.")

    counts = {"ham": 0, "spam": 0}
    seen_ids = set()
    for number, row in enumerate(rows, start=1):
        if None in row or any(not value or not value.strip() for value in row.values()):
            raise ValueError(f"Record {number}: missing or extra field.")
        if row["message_id"] in seen_ids:
            raise ValueError(f"Record {number}: duplicate message_id.")
        if row["label"] not in counts:
            raise ValueError(f"Record {number}: label must be ham or spam.")
        seen_ids.add(row["message_id"])
        counts[row["label"]] += 1

    if not seen_ids:
        raise ValueError("The file contains no messages.")

    return {
        "input_file": str(input_path.resolve()),
        "input_sha256": hashlib.sha256(raw).hexdigest(),
        "total_messages": sum(counts.values()),
        "label_counts": counts,
        "runtime": {
            "python_executable": sys.executable,
            "python_version": platform.python_version(),
            "working_directory": str(Path.cwd()),
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True, help="Input CSV file")
    parser.add_argument("--out", type=Path, required=True, help="Output JSON report")
    args = parser.parse_args()
    if args.data.resolve() == args.out.resolve():
        parser.error("The report must be a different file from the input data.")

    try:
        report = describe(args.data)
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        parser.exit(1, f"Error: {error}\n")

    print(f"Report saved: {args.out.resolve()}")
    print(f"Messages: {report['total_messages']}; labels: {report['label_counts']}")


if __name__ == "__main__":
    main()
