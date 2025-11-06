#!/usr/bin/env python3
"""
Script to replace commas with tab spaces in files.

This script processes all .txt files in the "Data export_processed" folder 
and replaces commas (",") with tab characters ("\t").

Usage:
    python replace_commas_with_tabs.py [input_folder]
    
    If input_folder is not specified, defaults to "Data export_processed".
    
Example:
    python replace_commas_with_tabs.py
    python replace_commas_with_tabs.py "Data export_processed"
"""

import sys
import os
from pathlib import Path


def replace_commas_with_tabs(input_file, output_file=None, verbose=False):
    """
    Replace commas with tab characters in a file.
    
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
            content = f.read()
        
        if not content.strip():
            # Empty file - just copy it to output
            with open(output_file, 'w', encoding='utf-8') as f:
                pass  # Create empty file
            if verbose:
                print(f"Warning: File '{input_file}' is empty. Empty file created in output.")
            return True  # Not really an error, just an empty file
        
        # Replace commas with tabs
        modified_content = content.replace(',', '\t')
        
        # Write to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(modified_content)
        
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


def process_all_files_in_folder(input_folder="Data export_processed"):
    """
    Process all .txt files in the input folder and replace commas with tabs.
    
    Args:
        input_folder (str): Path to the input folder containing .txt files
    
    Returns:
        tuple: (success_count, total_count, failed_files)
    """
    input_path = Path(input_folder)
    
    # Check if input folder exists
    if not input_path.exists() or not input_path.is_dir():
        print(f"Error: Input folder '{input_folder}' not found or is not a directory.")
        return (0, 0, [])
    
    print(f"Processing files from: '{input_folder}'")
    print("Replacing commas with tab characters...")
    print("-" * 60)
    
    # Find all .txt files in the input folder (excluding subdirectories)
    txt_files = [f for f in input_path.iterdir() if f.is_file() and f.suffix.lower() == '.txt']
    
    if not txt_files:
        print(f"No .txt files found in '{input_folder}'")
        return (0, 0, [])
    
    success_count = 0
    failed_files = []
    
    for input_file in sorted(txt_files):
        print(f"Processing: {input_file.name}...", end=" ", flush=True)
        
        try:
            if replace_commas_with_tabs(str(input_file), str(input_file), verbose=False):
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
    input_folder = "Data export_processed"
    
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

