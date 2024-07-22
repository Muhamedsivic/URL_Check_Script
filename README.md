# URL Search and Save Script

## Project Overview

This project is a Python script that automates the process of searching for URLs using Google and saving the first result's URL to a specified file. It uses the Selenium library for browser automation and Loguru for logging.

## Prerequisites

Before you can run this script, ensure you have the following installed:

- Python 3.x
- Selenium
- WebDriver Manager for Python
- Google Chrome browser
- Loguru

You can install the required Python libraries using pip:

```bash
pip install selenium webdriver-manager loguru
```

## How to Run

**Prepare Your Locations**: Edit the **locations** list in the **main()** function to include the locations you want to search for.

```bash
locations = [
    'Social Explorer',  # Example location
    # Add more locations here
]
```

Set Output File Path: Update the **output_file_path** variable in the **main()** function to specify where you want to save the URLs.

```bash
output_file_path = r'C:\path\to\your\output_file.txt'
```

**Execute the Script**: Run the script using Python. Open your terminal and execute:

```bash
python main_script.py
```

## What to Expect

- The script will perform Google searches for each location in the locations list.
- For each search, it will find and click on the first search result.
- It will then save the URL of the clicked result to the urls.txt file.
- The urls.txt file will be created or overwritten at the specified location with the URLs of the search results.

## Logging

The script uses the Loguru library to log various actions and events:

- URLs being searched.
- Loaded page URLs.
- Success or error messages for finding and saving URLs.

## Error Handling

- If an error occurs during the search or file operations, it will be logged with details about the issue.
