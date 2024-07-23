import argparse
import csv
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from loguru import logger
from urllib.parse import urljoin

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
    try:
        with open(output_file_path, 'w', newline='', encoding='utf-8') as output_file:
            writer = csv.writer(output_file)
            writer.writerow(['Index', 'Location', 'URL'])

            for i, location in enumerate(locations):
                search_url = f"https://www.google.com/search?q={location.replace(' ', '+')}"
                logger.info(f"Searching URL: {search_url}")
                time.sleep(0.5)
                
                driver.get(search_url)
                logger.info(f"Page loaded: {driver.current_url}")
                time.sleep(3)

                try:
                    first_element = driver.find_element(By.CSS_SELECTOR, '.yuRUbf a')
                    logger.info("First search result found")
                    new_url = first_element.get_attribute('href')
                    logger.success(f"Found URL: {new_url}")

                    writer.writerow([i + 1, location, new_url])

                except Exception as e:
                    logger.error(f"An error occurred for the location {location}: {e}")

    except Exception as e:
        logger.error(f"An error occurred while working with the file: {e}")

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
    
    try:
        with open(output_file_path, 'w', newline='', encoding='utf-8') as output_file:
            writer = csv.writer(output_file)
            writer.writerow(['Index', 'Location', 'URL'])

            for i, location in enumerate(locations):
                search_url = f"https://www.google.com/search?q={location.replace(' ', '+')}"
                logger.info(f"Searching URL: {search_url}")
                
                try:
                    response = requests.get(search_url, headers=headers)
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
                
                except Exception as e:
                    logger.error(f"An error occurred for the location {location}: {e}")
                    
    except Exception as e:
        logger.error(f"An error occurred while working with the file: {e}")

def main():
    parser = argparse.ArgumentParser(description='Search for URLs using Google and save them to a file.')
    parser.add_argument('--method', choices=['selenium', 'requests'], default='requests',
                        help='Method to use for searching: "selenium" or "requests" (default: "requests")')
    parser.add_argument('--input_file', type=str, required=True, 
                        help='Path to the CSV file containing the list of locations to be searched.')
    parser.add_argument('--output_file', type=str, required=True,
                        help='Path to the CSV file where the search results will be saved.')
    args = parser.parse_args()
    
    locations = []

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
