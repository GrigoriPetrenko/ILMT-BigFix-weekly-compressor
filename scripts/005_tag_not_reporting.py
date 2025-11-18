#!/usr/bin/env python3
"""Annotate reporting status in 020_all.csv based on 021_notrep.csv."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


STATUS_HEADER = "Not reporting to BigFix"
NOT_REPORTING_LABEL = "Not Reporting"
REPORTING_LABEL = "Reporting"


def load_computer_names(path: Path) -> set[str]:
    """Return the set of computer names from the first column of the file."""

    names: set[str] = set()
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        next(reader, None)  # skip header
        for row in reader:
            if not row:
                continue
            name = row[0].strip()
            if name:
                names.add(name)
    return names


def tag_reporting_status(all_file: Path, not_reporting_file: Path) -> None:
    """Insert or update the reporting status column in the all-file."""

    not_reporting_names = load_computer_names(not_reporting_file)

    if not all_file.exists():
        raise FileNotFoundError(f"File not found: {all_file}")

    with all_file.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle, delimiter="\t"))

    if not rows:
        print(f"Warning: File is empty, nothing to update: {all_file}")
        return

    header = rows[0]

    if STATUS_HEADER in header:
        status_index = header.index(STATUS_HEADER)
    else:
        header.insert(1, STATUS_HEADER)
        status_index = 1
        for row in rows[1:]:
            row.insert(status_index, "")

    for row in rows[1:]:
        if not row:
            continue
        name = row[0].strip()
        status = NOT_REPORTING_LABEL if name in not_reporting_names else REPORTING_LABEL

        # Ensure row has enough columns (in case original row was shorter)
        if len(row) <= status_index:
            row.extend([""] * (status_index - len(row) + 1))
        row[status_index] = status

    with all_file.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerows(rows)

    print(
        f"Updated '{all_file.name}' with {STATUS_HEADER!r} column using "
        f"{len(not_reporting_names)} reference computer names."
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "all_file",
        nargs="?",
        type=Path,
        default=Path("Data export_processed") / "020_all.csv",
        help="Path to the all-computers file (default: Data export_processed/020_all.csv)",
    )
    parser.add_argument(
        "not_reporting_file",
        nargs="?",
        type=Path,
        default=Path("Data export_processed") / "021_notrep.csv",
        help="Path to the not-reporting file (default: Data export_processed/021_notrep.csv)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tag_reporting_status(args.all_file, args.not_reporting_file)


if __name__ == "__main__":
    main()
