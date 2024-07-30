import argparse
import csv
import os
import time
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from loguru import logger
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging to a single file with rotation
log_file_path = "logs/log_file.log"
logger.add(log_file_path, rotation="1 week", retention="2 weeks", level="INFO")


def configure_driver():
    """Configures and returns the Chrome WebDriver"""
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()))


def search_and_save_urls_selenium(driver, locations, output_file_path):
    """
    Searches Google for each location in the list, finds the URL of the first search result, and saves them to a CSV file using Selenium.

    Args:
    - driver: WebDriver object for browser management
    - locations: List of locations to be searched
    - output_file_path: Path to the output file where URLs are stored
    """
    with open(output_file_path, 'w', newline='', encoding='utf-8') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(['Index', 'Location', 'URL'])

        for i, location in enumerate(locations):
            search_url = f"https://www.google.com/search?q={location.replace(' ', '+')}"
            logger.info(f"Searching URL: {search_url}")
            time.sleep(0.5)  # Sleep to avoid hitting the server too quickly

            try:
                driver.get(search_url)
                logger.info(f"Page loaded: {driver.current_url}")
                time.sleep(3)  # Allow time for the page to fully load

                first_element = driver.find_element(By.CSS_SELECTOR, '.yuRUbf a')
                logger.info("First search result found")
                new_url = first_element.get_attribute('href')
                logger.success(f"Found URL: {new_url}")

                writer.writerow([i + 1, location, new_url])

            except NoSuchElementException as e:
                logger.error(f"Element not found while searching for location {location}: {e}")
            except TimeoutException as e:
                logger.error(f"Timeout occurred while searching for location {location}: {e}")
            except WebDriverException as e:
                logger.error(f"WebDriver error occurred while searching for location {location}: {e}")
            except Exception as e:
                logger.error(f"Unexpected error occurred while searching for location {location}: {e}") #test123

def search_and_save_urls_requests(locations, output_file_path):
    """
    Searches Google for each location in the list, finds the URL of the first search result, and saves them to a CSV file using requests.

    Args:
    - locations: List of locations to be searched
    - output_file_path: Path to the output file where URLs are stored
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    with open(output_file_path, 'w', newline='', encoding='utf-8') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(['Index', 'Location', 'URL'])

        for i, location in enumerate(locations):
            search_url = f"https://www.google.com/search?q={location.replace(' ', '+')}"
            logger.info(f"Searching URL: {search_url}")

            try:
                response = requests.get(search_url, headers=headers, timeout=10)
                response.raise_for_status()  # Raise an exception for HTTP errors

                soup = BeautifulSoup(response.text, 'html.parser')
                first_element = soup.select_one('.yuRUbf a')

                if first_element:
                    relative_url = first_element['href']
                    new_url = urljoin('https://www.google.com', relative_url)
                    logger.success(f"Found URL: {new_url}")
                    writer.writerow([i + 1, location, new_url])
                else:
                    logger.warning(f"No search result found for location {location}")

            except requests.HTTPError as http_err:
                error_status_messages = {
                    400: "Bad Request (400)",
                    401: "Unauthorized (401)",
                    403: "Forbidden (403)",
                    404: "Not Found (404)",
                    500: "Internal Server Error (500)",
                    503: "Service Unavailable (503)",
                }
                status_message = error_status_messages.get(http_err.response.status_code, f"HTTP error: {http_err}")
                logger.error(f"HTTP error occurred for location {location}: {status_message}")
            except requests.RequestException as req_err:
                logger.error(f"Request error occurred for location {location}: {req_err}")
            except Exception as e:
                logger.error(f"Unexpected error occurred for location {location}: {e}")


def check_url_status(url, output_file_path):
    """Checks the status code of the given URL and writes the result to a CSV file"""

    status_messages = {
        200: "Reachable",
        404: "Not Found (404)",
        500: "Internal Server Error (500)",
        503: "Service Unavailable (503)",
    }

    try:
        response = requests.get(url, timeout=10)
        status_code = response.status_code
        status_message = status_messages.get(status_code, f"Status Code {status_code}")

        if status_code == 200:
            logger.success(f"URL is reachable: {url}")
        elif status_code in [404, 500, 503]:
            logger.error(f"URL returned status code {status_code}: {url}")
        else:
            logger.warning(f"URL returned status code {status_code}: {url}")

    except requests.HTTPError as http_err:
        error_status_messages = {
            400: "Bad Request (400)",
            401: "Unauthorized (401)",
            403: "Forbidden (403)",
            404: "Not Found (404)",
            500: "Internal Server Error (500)",
            503: "Service Unavailable (503)",
        }

        status_code = "Error"
        status_message = error_status_messages.get(http_err.response.status_code, f"HTTP error: {http_err}")
        logger.error(f"HTTP error occurred while checking URL {url}: {http_err}")

    except requests.RequestException as req_err:
        status_code = "Error"
        status_message = f"Request error: {req_err}"
        logger.error(f"Request error occurred while checking URL {url}: {req_err}")

    except Exception as e:
        status_code = "Error"
        status_message = f"Unexpected error: {e}"
        logger.error(f"Unexpected error occurred while checking URL {url}: {e}")

    with open(output_file_path, 'a', newline='', encoding='utf-8') as output_file:
        writer = csv.writer(output_file, delimiter=' ')
        writer.writerow([url, status_code, status_message])


def check_urls_from_output(output_file_path, status_output_path):
    """Checks the status of URLs listed in the output CSV file and writes the results to another CSV file"""
    if not os.path.isfile(output_file_path):
        logger.error(f"The file {output_file_path} does not exist.")
        return  # Exits the function if the specified file does not exist

    with open(output_file_path, 'r', newline='', encoding='utf-8') as output_file:
        reader = csv.reader(output_file)
        next(reader)  # Skip header row

        with open(status_output_path, 'w', newline='', encoding='utf-8') as status_output_file:
            writer = csv.writer(status_output_file, delimiter=' ')
            writer.writerow(['URL', 'Status Code', 'Status'])  # Write header row

            for row in reader:
                url = row[2]  # Assuming URL is in the third column
                check_url_status(url, status_output_path)


def main():
    parser = argparse.ArgumentParser(description='Search for URLs using Google and save them to a file.')
    parser.add_argument('--method', choices=['selenium', 'requests'], default='requests',
                        help='Method to use for searching: "selenium" or "requests" (default: "requests")')
    parser.add_argument('--input_file', type=str, required=False,
                        help='Path to the CSV file containing the list of locations to be searched.')
    parser.add_argument('--output_file', type=str, required=False,
                        help='Path to the CSV file where the search results will be saved.')
    parser.add_argument('--check_url', type=str, required=False,
                        help='URL to check status independently.')
    parser.add_argument('--status_output', type=str, default='data/status_check.csv',
                        help='Path to the CSV file where URL status results will be saved.')
    parser.add_argument('--check_output_urls', action='store_true',
                        help='Check the status of URLs listed in the output file.')

    args = parser.parse_args()

    if args.check_url:
        check_url_status(args.check_url, args.status_output)
        return  # Stops the execution of the function if only a URL for status checking is provided

    if args.check_output_urls:
        if not args.output_file:
            parser.error('--output_file is required to check URLs from the output file.')
        check_urls_from_output(args.output_file, args.status_output)
        return  # Stops the execution of the function after checking the status of URLs from the output file

    if not args.input_file or not args.output_file:
        parser.error(
            '--input_file and --output_file are required unless --check_url or --check_output_urls is specified.')

    with open(args.input_file, 'r', newline='', encoding='utf-8') as input_file:
        reader = csv.reader(input_file)
        next(reader)  # Skip header row
        locations = [row[0] for row in reader]  # Assuming locations are in the first column

    if args.method == 'selenium':
        driver = configure_driver()
        search_and_save_urls_selenium(driver, locations, args.output_file)
        driver.quit()
    else:
        search_and_save_urls_requests(locations, args.output_file)


if __name__ == "__main__":
    main()
