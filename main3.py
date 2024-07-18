from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import os

locations = [
    'Storage Werks Cedarburg 8545 WI-60 Trunk, Cedarburg, WI 53012, USA',
    'State Storage Workshops 13001 S Belcher Rd, Largo, FL 33773, USA',
    'Diamond RV &amp; Heated Storage 60 Schouweiler Tract Rd W, Elma, WA 98541, USA',
    'P Allan Storage 466 Co Rd 11, Bellefontaine, OH 43311, USA',
    'Windsor Depot RV Boat & Storage 600 Railroad St, Windsor, MO 65360, USA',
    'Crockers Lockers - Lompoc 224 North A Street, Lompoc, CA 93436, USA',
    'Jeffs Attic @ Plaza Dr	6870 Plaza Dr, Niagara Falls, NY 14304, USA',
    'Southwood Commons 946 Commercial Ave SW, New Philadelphia, OH 44663, USA',
    'Goshen Properties Storage 1740 N Water St Ext, Uhrichsville, OH 44683, USA',
    'Awesome Self Storage 6489 US-441 E, Okeechobee, FL 34974, USA',
    'Prestige Storage - Fort Worth	8032 White Settlement Rd, White Settlement, TX 76108, USA',
    'The Storage Center	1540 Lindberg Dr, Slidell, LA 70458, USA',
    'A+ Storage	1006 US-33, Weston, WV 26452, USA',
    'Space Center Self Storage 1100 Highway 71 South, Mena, AR 71953, USA',
    'Golden Storage	32265 Azure Rd, Cushing, MN 56443, USA',
    'StorageMart 2715 S 28th St, Milwaukee, WI 53215, USA',
    'Daniels Climate Control Storage 1851 Mo-72, Rolla, MO 65401, USA', # Ne radi
    'Lok-Safe Storage 1410 Mid Valley Dr, De Pere, WI 54115, USA',
    'Days Inn by Wyndham Bishop	724 W Line St, Bishop, CA 93514, USA',
    'CubeSmart Self Storage	13722 Fm1764, Santa Fe, TX 77517, USA'
]

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

output_file_path = r'C:\Users\User\Desktop\Selenium\output\urls.txt'

output_folder = os.path.dirname(output_file_path)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for i, location in enumerate(locations):
        search_url = f"https://www.google.com/search?q={location.replace(' ', '+')}"
        time.sleep(0.5)
        driver.get(search_url)
        time.sleep(3)

        try:
            first_element = driver.find_element(By.CSS_SELECTOR, '.LC20lb.MBeuO.DKV0Md')
            first_element.click()
            time.sleep(3)

            new_url = driver.current_url

            output_file.write(f"{i + 1}. {new_url}\n")

        except Exception as e:
            print(f"An error occurred for location {location}: {e}")

driver.quit()