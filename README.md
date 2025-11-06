# BigFix and ILMT Analyzer Scripts

## Scripts Overview

### `remove_domain_suffix.py`
Removes domain suffixes from Computer Name column in tab-separated files.
- Processes all `.txt` files in `Data export` folder
- Removes everything after the first dot (e.g., `server165.domain.com` → `server165`)
- Saves processed files to `Data export_processed` folder

**Usage:**
```bash
python remove_domain_suffix.py
```

### `replace_commas_with_tabs.py`
Replaces commas with tab characters in files.
- Processes all `.txt` files in `Data export_processed` folder
- Converts comma-separated values to tab-separated format
- Modifies files in place

**Usage:**
```bash
python replace_commas_with_tabs.py
```

### `rename_txt_to_csv.py`
Renames all `.txt` files to `.csv` files.
- Processes all `.txt` files in `Data export_processed` folder
- Renames files from `.txt` to `.csv` extension
- Python version of `RenameTxtToCsv.bat`

**Usage:**
```bash
python rename_txt_to_csv.py
```

## Workflow

1. Run `remove_domain_suffix.py` to process files from `Data export` → `Data export_processed`
2. Run `replace_commas_with_tabs.py` to convert commas to tabs in processed files
3. Run `rename_txt_to_csv.py` to rename files from `.txt` to `.csv`

