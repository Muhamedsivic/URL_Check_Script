import requests
import csv
import time
from loguru import logger
from bs4 import BeautifulSoup

def search_and_save_urls(locations, output_file_path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        with open(output_file_path, 'w', encoding='utf-8', newline='') as output_file:
            csv_writer = csv.writer(output_file)
            csv_writer.writerow(["Index", "Location", "URL"])  # Write the header

            for i, location in enumerate(locations):
                search_url = f"https://www.google.com/search?q={location.replace(' ', '+')}"
                logger.info(f"URL search: {search_url}")  
                
                # Perform the GET request to the search URL
                response = requests.get(search_url, headers=headers)
                logger.info(f"Page loaded: {search_url}")  
                time.sleep(3)  

                if response.status_code == 200:
                    try:
                        # Parse the response content with BeautifulSoup
                        soup = BeautifulSoup(response.content, 'html.parser')
                        first_element = soup.select_one('.LC20lb.MBeuO.DKV0Md')
                        
                        if first_element and first_element.parent.has_attr('href'):
                            new_url = first_element.parent['href']
                            logger.success(f"URL found: {new_url}")  

                            # Write the URL in the CSV file with a sequence number and location
                            csv_writer.writerow([i + 1, location, new_url])
                        else:
                            logger.error(f"No search result found for the location {location}")

                    except Exception as e:
                        logger.error(f"An error occurred for the location {location}: {e}")

                else:
                    logger.error(f"Failed to load the search page for the location {location}, status code: {response.status_code}")

    except Exception as e:
        logger.error(f"An error occurred while working with the file: {e}")

def main():
    locations = [
        'Social Explorer'  # Pretraga 
    ]
    output_file_path = r'C:\Users\User\.vscode\Projekti\URL_Check_Script\Requests_version\urls2.csv'  # Absolute path to the output CSV file

    search_and_save_urls(locations, output_file_path)  # Start searching and saving URLs

if __name__ == "__main__":
    main()