# URL Check Script

This script searches Google for each location from a list, finds the URL of the first search result, and saves them to a CSV file. The script can use either `requests` or `selenium` for searching, with `requests` being the default method.

## Requirements

- Python 3.x
- The following Python libraries:
  - `argparse`
  - `csv`
  - `time`
  - `requests`
  - `beautifulsoup4`
  - `selenium`
  - `webdriver_manager`
  - `loguru`
  - `urllib`

You can install them using the `pip` command:

```sh
pip install argparse csv time requests beautifulsoup4 selenium webdriver_manager loguru urllib3
```

## Usage

### Configure WebDriver

The **configure_driver()** function sets up the Chrome WebDriver using WebDriver Manager to handle the driver installation automatically.

### Search and Save URLs

**_ Using selenium _**
The **_ search_and_save_urls_selenium(driver, locations, output_file_path) _** function:

- Accepts a WebDriver object, a list of locations to search for, and the path to the output file.
- Iterates over the list of locations, performs a Google search for each, and saves the URL of the first search result.

**_ Using requests _**
The **_ search_and_save_urls_requests(locations, output_file_path) _** function:

- Accepts a list of locations to search for and the path to the output file.
- Iterates over the list of locations, performs a Google search for each using HTTP requests, and saves the URL of the first search result.

### Main Function

The **_ main() _** function initializes the list of locations to search for and the path to the output file, configures the WebDriver if the selenium method is chosen, and calls the appropriate function to search and save URLs.

### Running the Script

To run the script, use the following command in your terminal:

#### Using requests (default method)

```bash
 python main_script.py
```

#### Using selenium

```bash
 python main_script.py --method selenium
```

### Additional Notes

- Ensure you have all required libraries installed.
- Adjust the output_file_path in the main() function according to your system.
- The requests method is the default due to its speed and efficiency, but selenium can be useful for more complex searches that require JavaScript execution.
