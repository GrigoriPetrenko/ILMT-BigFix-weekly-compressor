# BigFix and ILMT Analyzer Scripts

## Scripts Overview

The processing scripts live in the `scripts/` directory—run them from the project
root using `python scripts/<script_name>.py`. The orchestration helper `run_all.py`
resides in the project root.

### `scripts/remove_domain_suffix.py`
Removes domain suffixes from Computer Name column in tab-separated files.
- Processes all `.txt` files in `Data export` folder
- Removes everything after the first dot (e.g., `server165.domain.com` → `server165`)
- Saves processed files to `Data export_processed` folder

**Usage:**
```bash
python scripts/remove_domain_suffix.py
```

### `scripts/replace_commas_with_tabs.py`
Replaces commas with tab characters in files.
- Processes all `.txt` files in `Data export_processed` folder
- Converts comma-separated values to tab-separated format
- Modifies files in place

**Usage:**
```bash
python scripts/replace_commas_with_tabs.py
```

### `scripts/rename_txt_to_csv.py`
Renames all `.txt` files to `.csv` files.
- Processes all `.txt` files in `Data export_processed` folder
- Renames files from `.txt` to `.csv` extension
- Python version of `RenameTxtToCsv.bat`

**Usage:**
```bash
python scripts/rename_txt_to_csv.py
```

### `scripts/tag_not_reporting.py`
Tags each computer in `020_all.csv` as reporting or not reporting to BigFix.
- Compares computer names between `020_all.csv` and `021_notrep.csv`
- Inserts/updates the column `Not reporting to BigFix` immediately after `Computer Name`
- Marks matching hosts as `Not Reporting`, others as `Reporting`

**Usage:**
```bash
python scripts/tag_not_reporting.py
```

### `scripts/strip_quotes_cmdb.py`
Removes double-quote characters from the CMDB export (`023_CMDB_active.txt`).
- Cleans the source file in `Data export/`
- Helps downstream scripts that expect plain comma-separated values

**Usage:**
```bash
python scripts/strip_quotes_cmdb.py
```

### `run_all.py`
Runs the three scripts above in sequence with a 2-second pause between each step.

**Usage:**
```bash
python run_all.py
```

## Workflow

0. (Optional) Run `scripts/strip_quotes_cmdb.py` to clean `023_CMDB_active.txt`
1. Run `scripts/remove_domain_suffix.py`