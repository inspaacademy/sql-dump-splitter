#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = "Davyd Maker"
__version__ = "1.2"

import os
import argparse
import time
import re

DEFAULT_SQL_CONDITIONS = ["DROP TABLE", "CREATE TABLE IF NOT EXISTS", "CREATE VIEW", "CREATE FUNCTION", "CREATE PROCEDURE"]

def extract_name(line):
    # Regex patterns to match table/view/function/procedure names
    patterns = [
        r'CREATE TABLE (\w+)',  # Match CREATE TABLE statements
        r'CREATE VIEW (\w+)',   # Match CREATE VIEW statements
        r'CREATE FUNCTION (\w+)',  # Match CREATE FUNCTION statements
        r'CREATE PROCEDURE (\w+)',  # Match CREATE PROCEDURE statements
        r'DROP TABLE (\w+)',  # Match DROP TABLE statements
    ]
    
    for pattern in patterns:
        match = re.search(pattern, line)
        if match:
            return match.group(1)
    return None

def save_file(content, directory, file_name):
    try:
        file_path = os.path.join(directory, f'{file_name}.sql')
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(''.join(content))
    except IOError as e:
        print(f"Error writing file {file_path}: {e}")

def prepare_directory(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

def should_split(line, sql_conditions, condition_hit_count, trigger_count):
    if any(condition in line for condition in sql_conditions):
        condition_hit_count += 1
        if condition_hit_count >= trigger_count:
            return True, condition_hit_count
    return False, condition_hit_count

def handle_line(line, ignore_blank_lines):
    if ignore_blank_lines and not line.strip():
        return None
    return line

def process_file(input_file_path, output_dir, trigger_count, ignore_blank_lines, sql_conditions):
    prepare_directory(output_dir)
    file_count = 0
    current_content = []
    current_file_name = None
    condition_hit_count = 0

    start_time = time.time()
    
    try:
        with open(input_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                processed_line = handle_line(line, ignore_blank_lines)
                if processed_line is None:
                    continue

                name = extract_name(processed_line)
                split, condition_hit_count = should_split(processed_line, sql_conditions, condition_hit_count, trigger_count)
                
                if split:
                    if current_content:
                        # Save the current content to the previous file name
                        save_file(current_content, output_dir, current_file_name)
                        file_count += 1
                    
                    # Set the new file name based on the extracted name
                    current_file_name = name if name else f"file_{file_count}"  # Fallback if name extraction fails
                    current_content = []  # Reset current content for the new file
                    condition_hit_count = 0  # Reset hit count

                current_content.append(processed_line)

            # Save any remaining content in the last file
            if current_content and current_file_name:
                save_file(current_content, output_dir, current_file_name)
                file_count += 1
                
    except Exception as e:
        print(f"Error reading file {input_file_path}: {e}")

    return time.time() - start_time, file_count

def main():
    parser = argparse.ArgumentParser(description="Splits an SQL file into parts based on specific conditions, a count of occurrences of those conditions, and the option to ignore blank lines.")
    parser.add_argument("-i", "--input-file", required=True, help="Path to the SQL file to be processed.")
    parser.add_argument("-o", "--output-dir", default=None, help="Directory where the split files will be saved. If not provided, a directory with the name of the input file is created.")
    parser.add_argument("-t", "--trigger-count", type=int, default=1, help="Number of occurrences of the SQL conditions before saving a file (default: 1).")
    parser.add_argument("-b", "--ignore-blank-lines", action='store_true', help="Ignore blank lines in the file (default: False).")
    parser.add_argument("-c", "--sql-conditions", nargs='+', default=DEFAULT_SQL_CONDITIONS, help="List of SQL conditions that trigger the file division. Example: --sql-conditions 'DROP TABLE' 'ALTER TABLE'")
    parser.add_argument("-r", "--report", action='store_true', help="Display a summary report at the end of the execution.")

    args = parser.parse_args()

    if not args.output_dir:
        base_name = os.path.splitext(os.path.basename(args.input_file))[0]
        args.output_dir = os.path.join(os.getcwd(), base_name)

    elapsed_time, total_files = process_file(args.input_file, args.output_dir, args.trigger_count, args.ignore_blank_lines, args.sql_conditions)

    if args.report:
        print("\nExecution Summary:")
        print(f"Time elapsed: {elapsed_time:.2f} seconds")
        print(f"Input file: {args.input_file}")
        print(f"Output directory: {args.output_dir}")
        print(f"Total files generated: {total_files}")
        print(f"Ignore blank lines: {args.ignore_blank_lines}")
        print(f"SQL conditions used: {', '.join(args.sql_conditions)}")

if __name__ == "__main__":
    main()
