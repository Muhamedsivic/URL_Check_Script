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
    args = parser.parse_args()
    
    locations = [
    'WEST RAPID STORAGE UNITS, 510 INDUSTRIAL AVE , SD, 33641',
    'MATEO AVENUE MINI-STORAGE, 1162 SAN MATEO AVE , CA, 04441',
    'SHIELDS MOUNTAIN MINI STORAGE, 2547 MCGILL ST , TN, 20345',
    'BERWICK SELF STORAGE AT 560 PORTLAND ST, 560 PORTLAND ST ,ME, 64120',
    'STORAGE ZONE SELF STORAGE AND BUSINESS CENTERS, 2240 PEACHTREE ST, FL, 57109',
    'East Longmeadow Self Storage, LLC , 91 Industrial Dr , MA, 44680',
    'Agate Road Mini Storage & Rv, 1620 E Agate Rd , WA, 65154',
    'Park 150 Self Service Storage, 1602 E University Ave ,IL, 65068',
    'STORAGE WORLD, 350 SWEDESBORO AVE ,NJ, 26371',
    'Mountain Mini Storage, 31280 US Highway 2",MT, 54149',
    'Lufkin Climate Controlled Storage, 3540 US Hwy 69 ,TX, 66516',
    'PUBLIC STORAGE, 2629 S RANGELINE RD ,MO, 20867',
    'Lake Park Self Storage, 806 Highway 10 ,MN, 54125',
    'Power Self Storage - Kuakini, 76-6201 Walua Rd ,HI, 41355',
    'Extra Space Storage, 885 Centre St , MA, 44020',
    'Devon Self Storage, LLC - Devon Self Storage - DCT, 810 Gladstell St, TX, 74297',
    'Tmg Storage Units, 427 S Harrison St,IL, 30295',
    'Comstor Self Storage  Russells Point, 6964 OH-235, OH, 39410',
    'HEIGHTS SELF STORAGE,W 18TH ST, TX, 46306',
    'HIGHWAY 63 MINI STORAGE, 2200 US HWY 63, AR, 55363', # Search query
    ]
    output_file_path = r'C:\Users\User\.vscode\Projekti\URL_Check_Script\urls.csv'
    
    if args.method == 'selenium':
        driver = configure_driver()
        search_and_save_urls_selenium(driver, locations, output_file_path)
        driver.quit()
    else:
        search_and_save_urls_requests(locations, output_file_path)

if __name__ == "__main__":
    main()
