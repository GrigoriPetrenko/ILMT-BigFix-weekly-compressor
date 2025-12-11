#!/usr/bin/env python3
"""Annotate missing scan status in 020_all.csv based on 006_Missing Scan.csv."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


MISSING_SCAN_HEADER = "Missing Scan"
PRIMARY_REFERENCE_HEADER = "Failed Scan"
FALLBACK_REFERENCE_HEADER = "Delayed Data Upload"
YES_LABEL = "YES"
NO_LABEL = "NO"


def load_missing_scan_hosts(path: Path) -> set[str]:
    """Return the set of hostnames listed in the missing scan file."""

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


def tag_missing_scan_status(all_file: Path, missing_scan_file: Path) -> None:
    """Insert or update the missing scan status column in the all-file."""

    missing_hosts = load_missing_scan_hosts(missing_scan_file)

    if not all_file.exists():
        raise FileNotFoundError(f"File not found: {all_file}")

    with all_file.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle, delimiter="\t"))

    if not rows:
        print(f"Warning: File is empty, nothing to update: {all_file}")
        return

    header = rows[0]

    for candidate in (PRIMARY_REFERENCE_HEADER, FALLBACK_REFERENCE_HEADER):
        try:
            reference_index = header.index(candidate)
            break
        except ValueError:
            continue
    else:
        raise ValueError(
            f"Expected column {PRIMARY_REFERENCE_HEADER!r} or {FALLBACK_REFERENCE_HEADER!r} "
            f"not found in {all_file}"
        )

    desired_index = reference_index + 1

    if MISSING_SCAN_HEADER in header:
        current_index = header.index(MISSING_SCAN_HEADER)
        if current_index != desired_index:
            header.pop(current_index)
            header.insert(desired_index, MISSING_SCAN_HEADER)
            for row in rows[1:]:
                value = row.pop(current_index) if len(row) > current_index else ""
                if len(row) < desired_index:
                    row.extend([""] * (desired_index - len(row)))
                row.insert(desired_index, value)
        status_index = desired_index
    else:
        status_index = desired_index
        header.insert(status_index, MISSING_SCAN_HEADER)
        for row in rows[1:]:
            if len(row) < status_index:
                row.extend([""] * (status_index - len(row)))
            row.insert(status_index, "")

    for row in rows[1:]:
        if not row:
            continue
        computer_name = row[0].strip()
        status = YES_LABEL if computer_name in missing_hosts else NO_LABEL

        if len(row) <= status_index:
            row.extend([""] * (status_index - len(row) + 1))
        row[status_index] = status

    with all_file.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerows(rows)

    print(
        f"Updated '{all_file.name}' with {MISSING_SCAN_HEADER!r} column using "
        f"{len(missing_hosts)} missing scan hostnames."
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
        "missing_scan_file",
        nargs="?",
        type=Path,
        default=Path("Data export_processed") / "006_Missing Scan.csv",
        help=(
            "Path to the missing scan file "
            "(default: Data export_processed/006_Missing Scan.csv)"
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    tag_missing_scan_status(args.all_file, args.missing_scan_file)


if __name__ == "__main__":
    main()

