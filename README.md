# SQL Dump Splitter

## Description
The SQL Dump Splitter is a Python tool designed to split large SQL dump files into smaller files based on specific conditions such as 'DROP TABLE' and 'CREATE TABLE IF NOT EXISTS'. This tool is useful for managing large SQL databases where dumps can be excessively large for efficient handling.

## Features
- Splits large SQL files into multiple smaller files.
- Supports customizable conditions to trigger a new split.
- Option to ignore blank lines.
- Generates a summary report of the splitting process.

## Prerequisites
To use this script, you will need Python 3.6 or higher. No additional external libraries are required.

## Installation
No formal installation is necessary. The script can be cloned directly from the repository and run from the command line.

```bash
git clone https://github.com/davydmaker/sql-dump-splitter.git
cd sql-dump-splitter
```

## Usage
To use the SQL Dump Splitter, run the script from the command line with the required parameters. Here is an example of how to use the script:

```bash
python3 sql_dump_splitter.py --input-file 'path/to/your/dump.sql' --output-dir 'path/to/output' --trigger-count 1 --ignore-blank-lines --report
```

### Arguments
- `--input-file`: Path to the SQL file you want to split.
- `--output-dir`: Directory where the split files will be saved. If not provided, a directory with the name of the input file is created.
- `--trigger-count`: Number of occurrences of the SQL conditions before saving a file (default: 1).
- `--ignore-blank-lines`: Ignore blank lines in the file (default: False).
- `--sql-conditions`: List of SQL conditions that trigger the file split.
- `--report`: Display a summary report at the end of the execution.

## Contributing
Contributions are always welcome! If you have suggestions for improving the script or adding new features, feel free to fork the repository and submit a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
