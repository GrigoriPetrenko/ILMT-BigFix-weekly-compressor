#!/usr/bin/env python3
"""Remove double quotes from the CMDB export file."""

from __future__ import annotations

import argparse
from pathlib import Path


def strip_quotes(file_path: Path) -> None:
    """Remove all double-quote characters from the given file in place."""

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    original_text = file_path.read_text(encoding="utf-8")
    cleaned_text = original_text.replace('"', "")
    file_path.write_text(cleaned_text, encoding="utf-8")

    print(f"Removed double quotes from '{file_path}'.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "file",
        nargs="?",
        type=Path,
        default=Path("Data export") / "023_CMDB_active.txt",
        help="Path to the CMDB export file (default: Data export/023_CMDB_active.txt)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    strip_quotes(args.file)


if __name__ == "__main__":
    main()
