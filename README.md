# URL Search and Status Checker

This script allows you to search for URLs using Google and save them to a file. It also supports checking the status of a specific URL independently.

## Features

- **Search for URLs**: Uses Google to search for locations and saves the first search result URL to a CSV file.
- **Check URL Status**: Checks the status code of a specific URL and logs the result to a CSV file.
- **Logging**: Logs all activities and errors to a single log file with rotation.

## Requirements

- Python 3.6 or higher
- `requests==2.31.0`
- `beautifulsoup4==4.12.2`
- `selenium==4.21.0`
- `webdriver-manager==4.7.0`
- `loguru==0.7.0`

## Installation

1. Clone the repository:

   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

### Search for URLs

To search for URLs and save them to a file, use:

```sh
python main.py --method <method> --input_file <input_csv> --output_file <output_csv>
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
