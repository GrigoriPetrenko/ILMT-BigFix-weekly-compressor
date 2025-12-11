#!/usr/bin/env python3
"""Annotate CMDB activity status in 020_all.csv based on 023_CMDB_active.csv."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


CMDB_STATUS_HEADER = "CMDB Status"
ACTIVE_LABEL = "In CMDB"
INACTIVE_LABEL = "Not in CMDB"


def load_cmdb_hostnames(path: Path) -> set[str]:
    """Return the set of hostnames that are active in the CMDB."""

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


def tag_cmdb_status(all_file: Path, cmdb_file: Path) -> None:
    """Insert or update the CMDB status column in the all-file."""

    cmdb_hostnames = load_cmdb_hostnames(cmdb_file)

    if not all_file.exists():
        raise FileNotFoundError(f"File not found: {all_file}")

    with all_file.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle, delimiter="\t"))

    if not rows:
        print(f"Warning: File is empty, nothing to update: {all_file}")
        return

    header = rows[0]

    status_header = "Not reporting to BigFix"

    try:
        reference_index = header.index(status_header)
    except ValueError:
        reference_index = 1
        header.insert(reference_index, status_header)
        for row in rows[1:]:
            if len(row) < reference_index:
                row.extend([""] * (reference_index - len(row)))
            row.insert(reference_index, "")

    desired_index = reference_index + 1

    if CMDB_STATUS_HEADER in header:
        current_index = header.index(CMDB_STATUS_HEADER)
        if current_index != desired_index:
            header.pop(current_index)
            header.insert(desired_index, CMDB_STATUS_HEADER)
            for row in rows[1:]:
                value = row.pop(current_index) if len(row) > current_index else ""
                if len(row) < desired_index:
                    row.extend([""] * (desired_index - len(row)))
                row.insert(desired_index, value)
        status_index = desired_index
    else:
        status_index = desired_index
        header.insert(status_index, CMDB_STATUS_HEADER)
        for row in rows[1:]:
            if len(row) < status_index:
                row.extend([""] * (status_index - len(row)))
            row.insert(status_index, "")

    for row in rows[1:]:
        if not row:
            continue
        computer_name = row[0].strip()
        status = ACTIVE_LABEL if computer_name in cmdb_hostnames else INACTIVE_LABEL

        if len(row) <= status_index:
            row.extend([""] * (status_index - len(row) + 1))
        row[status_index] = status

    with all_file.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerows(rows)

    print(
        f"Updated '{all_file.name}' with {CMDB_STATUS_HEADER!r} column using "
        f"{len(cmdb_hostnames)} active CMDB hostnames."
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
        "cmdb_file",
        nargs="?",
        type=Path,
        default=Path("Data export_processed") / "023_CMDB_active.csv",
        help=(
            "Path to the CMDB active file "
            "(default: Data export_processed/023_CMDB_active.csv)"
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tag_cmdb_status(args.all_file, args.cmdb_file)


if __name__ == "__main__":
    main()

