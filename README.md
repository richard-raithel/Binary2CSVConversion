# Binary Data Processing Script

## Overview

This Python script processes binary data from a file and extracts relevant records into a CSV format. It decodes structured binary records, cleans the extracted fields, and handles unmatched flags gracefully. The result is a readable `.CSV` file ready for analysis or reporting.

---

## Features
- **Binary Data Parsing**: Extracts structured records from a binary file based on predefined flags and record formats.
- **CSV Output**: Saves parsed data into a `.CSV` file with specified field names (`name`, `discount`, `price`).
- **Logging**: Provides detailed logs for debugging and tracking unmatched flags.
- **Error Handling**: Handles file access issues and unexpected data formats gracefully.

---

## Requirements
- Python 3.x
- Standard library modules: `logging`, `csv`, `struct`

---

## Usage

### Input and Output Files
1. **Input**: `FPREIS_D381.BIN`  
   A binary file containing structured records to be parsed.
   
2. **Output**: `PRIJSXXX.csv`  
   The CSV file where parsed data will be saved.

### How to Run
1. Place the binary input file (`FPREIS_D381.BIN`) in the same directory as the script.
2. Run the script:
   ```bash
   python script_name.py
