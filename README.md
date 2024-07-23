# URL Search Script

## Description

This script searches Google for each location listed in an input CSV file and saves the URL of the first search result to an output CSV file. The script supports two search methods: `Selenium` and `requests`.

- **Selenium**: Uses Chrome WebDriver for browsing and collecting results.
- **Requests**: Uses HTTP requests to search and collect results.

## Installation

**Clone the repository:**

```bash
git clone https://github.com/Muhamedsivic/URL_Check_Script
cd URL_Check_Script
```

### Create a virtual environment (optional but recommended):

```bash
   python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### Install dependencies:

```bash
  pip install -r requirements.txt
```

## Usage

Run the script with the following command:

```bash
python your_script.py --method [selenium|requests] --input_file PATH_TO_INPUT_FILE --output_file PATH_TO_OUTPUT_FILE
```

## Arguments:

- --method : Search method. Can be selenium or requests. Default is requests.
- --input_file : Path to the CSV file containing the list of locations to be searched.
- --output_file : Path to the CSV file where the search results will be saved.

## Example:

If using **_ Selenium _** and your files are in the same directory as the script:

```bash
python your_script.py --method selenium --input_file input_file.csv --output_file output_file.csv
```

If using **_ requests: _**

```bash
python your_script.py --method requests --input_file input_file.csv --output_file output_file.csv
```

## Input File Example

**_ input_file.csv _** should look like this:

```bash
Location
WEST RAPID STORAGE UNITS, 510 INDUSTRIAL AVE , SD, 33641
MATEO AVENUE MINI-STORAGE, 1162 SAN MATEO AVE , CA, 04441
SHIELDS MOUNTAIN MINI STORAGE, 2547 MCGILL ST , TN, 20345
BERWICK SELF STORAGE AT 560 PORTLAND ST, 560 PORTLAND ST ,ME, 64120
STORAGE ZONE SELF STORAGE AND BUSINESS CENTERS, 2240 PEACHTREE ST, FL, 57109
```

## Author

Muhamed Sivic muhamedsivic@gmail.com
