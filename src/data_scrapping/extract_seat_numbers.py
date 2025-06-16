import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ToyotaSeatingScraper:
    def __init__(self, seat_options=None, output_file="src/data/intermediate/seats_toyota_vehicle_names_by_category.csv", headless=False):
        self.seat_options = seat_options or ["4", "5", "7", "8"]
        self.output_file = output_file
        self.base_url = "https://www.toyota.com/all-vehicles/"
        self.vehicle_data = []
        self.driver = None
        self.wait = None
        self.headless = headless

    def setup_driver(self):
        options = Options()
        options.add_argument("--start-maximized")
        if self.headless:
            options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 15)

    def collect_by_seating(self):
        for seat in self.seat_options:
            try:
                self.driver.get(self.base_url)
                time.sleep(5)

                checkbox_input = self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, f'//input[@type="checkbox" and @name="seating" and @value="{seat}"]')
                ))
                self.driver.execute_script("arguments[0].click();", checkbox_input)
                print(f"Clicked seating filter: {seat}")

                try:
                    apply_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.filters-apply')))
                    apply_button.click()
                    print("Clicked 'Apply Filters'")
                    time.sleep(3)
                except:
                    print("'Apply Filters' not found or not required")

                self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.vehicle-card')))
                cards = self.driver.find_elements(By.CSS_SELECTOR, 'div.vehicle-card div.title.heading-04')

                print(f"Vehicles with {seat} seats:")
                for card in cards:
                    name = card.text.strip()
                    if name:
                        print("-", name)
                        self.vehicle_data.append({"seating": seat, "vehicle_name": name})

            except Exception as e:
                print(f"Failed for seating '{seat}':", e)

    def save_to_csv(self):
        df = pd.DataFrame(self.vehicle_data).drop_duplicates()
        df.to_csv(self.output_file, index=False)
        print(f"CSV file saved: {self.output_file}")

    def run(self):
        self.setup_driver()
        self.collect_by_seating()
        self.driver.quit()
        self.save_to_csv()

