#!/usr/bin/env python3
"""Run all main processing scripts in sequence."""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path


def run_main_scripts(delay_seconds: int = 2) -> int:
    """Execute the main processing scripts sequentially."""

    root_dir = Path(__file__).resolve().parent / "scripts"
    scripts = [
        ("005_tag_not_reporting.py", []),
        ("010_tag_cmdb_status.py", []),
        ("015_tag_delayed_upload.py", []),
        ("020_tag_failed_scan.py", []),
        ("025_tag_missing_scan.py", []),
        ("030_tag_scan_not_uploaded.py", []),
        ("035_tag_no_scan_data.py", []),
        ("040_tag_no_vm_manager_data.py", []),
        ("045_tag_outdated_vm_manager_data.py", []),
        ("050_tag_outdated_scan.py", []),
    ]

    for index, (script_name, extra_args) in enumerate(scripts):
        script_path = root_dir / script_name
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

    print("All main scripts completed successfully.")
    return 0


def main() -> None:
    sys.exit(run_main_scripts())


if __name__ == "__main__":
    main()

