#!/usr/bin/env python3
"""Annotate delayed upload status in 020_all.csv based on 001_Delayed Data Upload.csv."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


DELAYED_STATUS_HEADER = "Delayed Data Upload"
REFERENCE_HEADER = "CMDB Status"
DELAYED_LABEL = "YES"
NOT_DELAYED_LABEL = "NO"


def load_delayed_hostnames(path: Path) -> set[str]:
    """Return the set of hostnames listed in the delayed upload file."""

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    hostnames: set[str] = set()
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle, delimiter="\t")
        next(reader, None)  # Skip header
        for row in reader:
            if not row:
                continue
            name = row[0].strip()
            if name:
                hostnames.add(name)
    return hostnames


def tag_delayed_status(all_file: Path, delayed_file: Path) -> None:
    """Insert or update the delayed upload status column in the all-file."""

    delayed_hostnames = load_delayed_hostnames(delayed_file)

    if not all_file.exists():
        raise FileNotFoundError(f"File not found: {all_file}")

    with all_file.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle, delimiter="\t"))

    if not rows:
        print(f"Warning: File is empty, nothing to update: {all_file}")
        return

    header = rows[0]

    try:
        reference_index = header.index(REFERENCE_HEADER)
    except ValueError as exc:
        raise ValueError(
            f"Expected column {REFERENCE_HEADER!r} not found in {all_file}"
        ) from exc

    desired_index = reference_index + 1

    if DELAYED_STATUS_HEADER in header:
        current_index = header.index(DELAYED_STATUS_HEADER)
        if current_index != desired_index:
            header.pop(current_index)
            header.insert(desired_index, DELAYED_STATUS_HEADER)
            for row in rows[1:]:
                value = row.pop(current_index) if len(row) > current_index else ""
                if len(row) < desired_index:
                    row.extend([""] * (desired_index - len(row)))
                row.insert(desired_index, value)
        status_index = desired_index
    else:
        status_index = desired_index
        header.insert(status_index, DELAYED_STATUS_HEADER)
        for row in rows[1:]:
            if len(row) < status_index:
                row.extend([""] * (status_index - len(row)))
            row.insert(status_index, "")

    for row in rows[1:]:
        if not row:
            continue
        computer_name = row[0].strip()
        status = DELAYED_LABEL if computer_name in delayed_hostnames else NOT_DELAYED_LABEL

        if len(row) <= status_index:
            row.extend([""] * (status_index - len(row) + 1))
        row[status_index] = status

    with all_file.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerows(rows)

    print(
        f"Updated '{all_file.name}' with {DELAYED_STATUS_HEADER!r} column using "
        f"{len(delayed_hostnames)} delayed hostnames."
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
        "delayed_file",
        nargs="?",
        type=Path,
        default=Path("Data export_processed") / "001_Delayed Data Upload.csv",
        help=(
            "Path to the delayed data upload file "
            "(default: Data export_processed/001_Delayed Data Upload.csv)"
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tag_delayed_status(args.all_file, args.delayed_file)


if __name__ == "__main__":
    main()

