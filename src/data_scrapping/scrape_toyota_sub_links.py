from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import os

class VehicleNames:
    def __init__(self):
        pass

    def run(self):
        self.scrapping_vehicle_names()

    @staticmethod
    def scrapping_vehicle_names():
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=options)

        url = 'https://www.toyota.com/all-vehicles/'
        driver.get(url)
        time.sleep(5)  

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        vehicle_cards = soup.find_all('div', class_='vehicle-card')

        vehicles = []
        for card in vehicle_cards:
            name = card.get('data-display-name')
            year = card.get('data-year')
            href = card.find('a', class_='explore-cta')
            link = f"https://www.toyota.com{href['href']}" if href else None

            vehicles.append({
                'name': name,
                'year': year,
                'link': link
            })

        df = pd.DataFrame(vehicles)
        os.makedirs('src/data/intermediate', exist_ok=True)  
        os.makedirs('src/data/final', exist_ok=True)  

        df.to_csv('src/data/intermediate/toyota_all_vehicle_names_links.csv', index=False)
        print("Data saved")

        driver.quit()


