from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import os.path
import csv
from loguru import logger  

def configure_driver():
    """Configures and resets the Chrome WebDriver"""
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()))

def search_and_save_urls(driver, locations, output_file_path):
    """
    It searches Google for each location in the list, finds the URL of the first search result, and saves them to a CSV file.
    
    Args:
    - driver: WebDriver object for browser management
    - locations: List of locations to be searched
    - output_file_path: Path to the output file where URLs are stored
    """
    try:
        with open(output_file_path, 'w', encoding='utf-8', newline='') as output_file:
            csv_writer = csv.writer(output_file)
            csv_writer.writerow(["Index", "Location", "URL"])  # Write the header

            for i, location in enumerate(locations):
                # We generate a URL for a Google search with the given location
                search_url = f"https://www.google.com/search?q={location.replace(' ', '+')}"
                logger.info(f"URL search: {search_url}")  
                time.sleep(0.5)  
                
                # We open the URL in the browser
                driver.get(search_url)
                logger.info(f"Page loaded: {driver.current_url}")  
                time.sleep(3)  

                try:
                    # We find the first search result using a CSS selector
                    first_element = driver.find_element(By.CSS_SELECTOR, '.LC20lb.MBeuO.DKV0Md')
                    logger.info("First search result found")  
                    first_element.click()  # Click on the first result
                    time.sleep(3)  

                    # We get the current URL after clicking on the first result
                    new_url = driver.current_url
                    logger.success(f"URL found: {new_url}")  

                    # We write the URL in the CSV file with a sequence number and location
                    csv_writer.writerow([i + 1, location, new_url])

                except Exception as e:
                    logger.error(f"An error occurred for the location {location}: {e}")

    except Exception as e:
        logger.error(f"An error occurred while working with the file: {e}")

def main():
    locations = [
        'Social Explorer' # Pretraga 
    ]
    output_file_path = r'C:\Users\User\.vscode\Projekti\URL_Check_Script\urls.csv'  # Absolute path to the output CSV file

    driver = configure_driver()  # Configure the WebDriver
    search_and_save_urls(driver, locations, output_file_path)  # Start searching and saving URLs
    driver.quit() 

if __name__ == "__main__":
    main()
