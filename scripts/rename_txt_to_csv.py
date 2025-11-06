#!/usr/bin/env python3
"""
Script to rename .txt files to .csv files.

This script renames all .txt files in the "Data export_processed" folder to .csv files.

Usage:
    python rename_txt_to_csv.py [input_folder]
    
    If input_folder is not specified, defaults to "Data export_processed".
    
Example:
    python rename_txt_to_csv.py
    python rename_txt_to_csv.py "Data export_processed"
"""

import sys
import os
from pathlib import Path


def rename_txt_to_csv(input_folder="Data export_processed"):
    """
    Rename all .txt files to .csv files in the specified folder.
    
    Args:
        input_folder (str): Path to the folder containing .txt files
    
    Returns:
        tuple: (success_count, total_count, failed_files)
    """
    input_path = Path(input_folder)
    
    # Check if input folder exists
    if not input_path.exists() or not input_path.is_dir():
        print(f"Error: Folder '{input_folder}' not found or is not a directory.")
        return (0, 0, [])
    
    print(f"Renaming .txt files to .csv in: '{input_folder}'")
    print("-" * 60)
    
    # Find all .txt files in the input folder (excluding subdirectories)
    txt_files = [f for f in input_path.iterdir() if f.is_file() and f.suffix.lower() == '.txt']
    
    if not txt_files:
        print(f"No .txt files found in '{input_folder}'")
        return (0, 0, [])
    
    success_count = 0
    failed_files = []
    
    for txt_file in sorted(txt_files):
        # Create new name with .csv extension
        csv_file = txt_file.with_suffix('.csv')
        
        print(f"Renaming: {txt_file.name}...", end=" ", flush=True)
        
        try:
            # Remove existing .csv file so the rename always succeeds with fresh content
            if csv_file.exists():
                csv_file.unlink()
            txt_file.rename(csv_file)
            success_count += 1
            print("✓")
        except Exception as e:
            failed_files.append(txt_file.name)
            print(f"✗ ERROR: {e}")
    
    print("-" * 60)
    print(f"Renaming complete: {success_count}/{len(txt_files)} files renamed successfully")
    
    if failed_files:
        print(f"Failed files: {', '.join(failed_files)}")
    
    return (success_count, len(txt_files), failed_files)


def main():
    """Main function to handle command line arguments."""
    # Default input folder
    input_folder = "Data export_processed"
    
    # Allow custom input folder as argument
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help', 'help']:
            print(__doc__)
            sys.exit(0)
        input_folder = sys.argv[1]
    
    success_count, total_count, failed_files = rename_txt_to_csv(input_folder)
    
    # Exit with error code if any files failed
    sys.exit(0 if success_count == total_count else 1)


if __name__ == "__main__":
    main()
