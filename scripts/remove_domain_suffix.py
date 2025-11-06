#!/usr/bin/env python3
"""
Script to remove domain suffix from Computer Name column in tab-separated files.

This script processes all .txt files in the "Data export" folder and removes everything 
after the first dot in the Computer Name column (first column). For example:
- "server165.domain.com" becomes "server165"
- "server168" remains "server168" (no change if no dot exists)

The processed files are saved to a new folder "Data export_processed".

Usage:
    python remove_domain_suffix.py [input_folder]
    
    If input_folder is not specified, defaults to "Data export".
    
Example:
    python remove_domain_suffix.py
    python remove_domain_suffix.py "Data export"
"""

import sys
import os
import csv
from pathlib import Path


SKIP_DOMAIN_FILES = {
    "023_CMDB_active.txt",
}


def remove_domain_suffix_from_computer_name(input_file, output_file=None, verbose=False):
    """
    Remove domain suffix from Computer Name column in a tab-separated file.
    
    Args:
        input_file (str): Path to the input file
        output_file (str, optional): Path to the output file. If None, modifies input_file in place.
        verbose (bool): If True, print detailed messages. Default False for batch processing.
    
    Returns:
        bool: True if successful, False otherwise
    """
    # If no output file specified, use input file
    if output_file is None:
        output_file = input_file
    
    # Check if input file exists
    if not os.path.exists(input_file):
        if verbose:
            print(f"Error: Input file '{input_file}' not found.")
        return False
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        if not content:
            if verbose:
                print(f"Warning: File '{input_file}' is empty.")
            # Ensure empty file exists at destination
            with open(output_file, 'w', encoding='utf-8') as f:
                pass
            return True

        lines = content.splitlines()

        delimiter = '\t' if '\t' in lines[0] else ','
        reader = csv.reader(lines, delimiter=delimiter)
        rows = list(reader)

        if not rows:
            if verbose:
                print(f"Warning: File '{input_file}' contains no rows.")
            with open(output_file, 'w', encoding='utf-8') as f:
                pass
            return True

        for idx, row in enumerate(rows):
            if idx == 0 or not row:
                continue
            computer_name = row[0].strip()
            if computer_name and '.' in computer_name:
                computer_name = computer_name.split('.')[0]
            row[0] = computer_name

        with open(output_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, delimiter=delimiter, lineterminator='\n')
            writer.writerows(rows)
        
        if verbose:
            print(f"Successfully processed file: '{input_file}'")
            if output_file != input_file:
                print(f"Output saved to: '{output_file}'")
            else:
                print(f"File modified in place.")
        
        return True
    
    except Exception as e:
        if verbose:
            print(f"Error processing file: {e}")
        return False


def process_all_files_in_folder(input_folder="Data export", output_folder_suffix="_processed"):
    """
    Process all .txt files in the input folder and save processed files to a new folder.
    
    Args:
        input_folder (str): Path to the input folder containing .txt files
        output_folder_suffix (str): Suffix to append to input folder name for output folder
    
    Returns:
        tuple: (success_count, total_count, failed_files)
    """
    input_path = Path(input_folder)
    
    # Check if input folder exists
    if not input_path.exists() or not input_path.is_dir():
        print(f"Error: Input folder '{input_folder}' not found or is not a directory.")
        return (0, 0, [])
    
    # Create output folder name
    output_folder = input_path.parent / f"{input_path.name}{output_folder_suffix}"
    
    # Create output folder if it doesn't exist
    output_folder.mkdir(exist_ok=True)
    print(f"Processing files from: '{input_folder}'")
    print(f"Output folder: '{output_folder}'")
    print("-" * 60)
    
    # Find all .txt files in the input folder (excluding subdirectories)
    txt_files = [f for f in input_path.iterdir() if f.is_file() and f.suffix.lower() == '.txt']
    
    if not txt_files:
        print(f"No .txt files found in '{input_folder}'")
        return (0, 0, [])
    
    success_count = 0
    failed_files = []
    
    for input_file in sorted(txt_files):
        output_file = output_folder / input_file.name
        print(f"Processing: {input_file.name}...", end=" ", flush=True)

        if input_file.name in SKIP_DOMAIN_FILES:
            try:
                output_file.write_text(input_file.read_text(encoding="utf-8"), encoding="utf-8")
                success_count += 1
                print("(copied) ✓")
                continue
            except Exception as copy_exc:
                failed_files.append(input_file.name)
                print(f"✗ ERROR copying: {copy_exc}")
                continue
        
        try:
            if remove_domain_suffix_from_computer_name(str(input_file), str(output_file), verbose=False):
                success_count += 1
                print("✓")
            else:
                failed_files.append(input_file.name)
                print("✗ FAILED")
        except Exception as e:
            failed_files.append(input_file.name)
            print(f"✗ ERROR: {e}")
    
    print("-" * 60)
    print(f"Processing complete: {success_count}/{len(txt_files)} files processed successfully")
    
    if failed_files:
        print(f"Failed files: {', '.join(failed_files)}")
    
    return (success_count, len(txt_files), failed_files)


def main():
    """Main function to handle command line arguments."""
    # Default input folder
    input_folder = "Data export"
    
    # Allow custom input folder as argument
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help', 'help']:
            print(__doc__)
            sys.exit(0)
        input_folder = sys.argv[1]
    
    success_count, total_count, failed_files = process_all_files_in_folder(input_folder)
    
    # Exit with error code if any files failed
    sys.exit(0 if success_count == total_count else 1)


if __name__ == "__main__":
    main()
