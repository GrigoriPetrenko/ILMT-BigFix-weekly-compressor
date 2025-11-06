#!/usr/bin/env python3
"""Run all data-processing scripts sequentially with a short delay."""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path


def run_scripts_with_delay(delay_seconds: int = 2) -> int:
    """Run the processing scripts sequentially with a delay between each one."""

    root_dir = Path(__file__).resolve().parent
    scripts_dir = root_dir / "scripts"
    scripts = [
        ("remove_domain_suffix.py", []),
        ("replace_commas_with_tabs.py", []),
        ("rename_txt_to_csv.py", []),
    ]

    for index, (script_name, extra_args) in enumerate(scripts):
        script_path = scripts_dir / script_name
        if not script_path.exists():
            print(f"Error: Script not found: {script_path}")
            return 1

        command = [sys.executable, str(script_path), *extra_args]
        print(f"Running: {' '.join(command)}")

        result = subprocess.run(command, check=False)
        if result.returncode != 0:
            print(f"Script failed with exit code {result.returncode}: {script_name}")
            return result.returncode

        if index < len(scripts) - 1:
            time.sleep(delay_seconds)

    print("All scripts completed successfully.")
    return 0


def main() -> None:
    """Entry point when executed as a script."""
    sys.exit(run_scripts_with_delay(delay_seconds=2))


if __name__ == "__main__":
    main()
