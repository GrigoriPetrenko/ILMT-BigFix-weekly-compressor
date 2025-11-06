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
from pathlib import Path


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
        # Read the file
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if not lines:
            # Empty file - just copy it to output
            with open(output_file, 'w', encoding='utf-8') as f:
                pass  # Create empty file
            if verbose:
                print(f"Warning: File '{input_file}' is empty. Empty file created in output.")
            return True  # Not really an error, just an empty file
        
        # Process lines
        result = []
        for i, line in enumerate(lines):
            if i == 0:
                # Keep header line as is
                result.append(line)
            else:
                # Process data lines
                if line.strip():  # Skip empty lines
                    parts = line.split('\t')
                    if len(parts) > 0:
                        # Get first part (Computer Name) and remove everything after first dot
                        computer_name = parts[0]
                        if '.' in computer_name:
                            computer_name = computer_name.split('.')[0]
                        parts[0] = computer_name
                        result.append('\t'.join(parts))
                    else:
                        result.append(line)
                else:
                    result.append(line)
        
        # Write to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(result)
        
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

