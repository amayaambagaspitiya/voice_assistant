import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ToyotaVehicleScraper:
    def __init__(self, output_file="src/data/intermediate/toyota_vehicle_names_by_category.csv", headless=False):
        self.output_file = output_file
        self.base_url = "https://www.toyota.com/all-vehicles/"
        self.categories = ["Cars", "Crossovers", "SUVs", "Trucks", "Minivan"]
        self.electrified_vehicles = []
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

    def collect_electrified(self):
        try:
            self.driver.get(self.base_url)
            time.sleep(5)

            checkbox = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//span[contains(@class, "primary-label") and normalize-space(text())="Electrified"]')
            ))
            checkbox.click()
            print("Clicked filter: Electrified")

            try:
                apply_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.filters-apply')))
                apply_button.click()
                print("Clicked 'Apply Filters'")
                time.sleep(3)
            except:
                print("'Apply Filters' not found or not required")

            self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.vehicle-card')))
            cards = self.driver.find_elements(By.CSS_SELECTOR, 'div.vehicle-card div.title.heading-04')

            self.electrified_vehicles = [card.text.strip() for card in cards if card.text.strip()]
            print("Electrified Vehicles Collected:", self.electrified_vehicles)

        except Exception as e:
            print("Failed to collect 'Electrified' vehicles:", e)

    def collect_by_category(self):
        for category in self.categories:
            try:
                self.driver.get(self.base_url)
                time.sleep(5)

                checkbox = self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, f'//span[contains(@class, "primary-label") and normalize-space(text())="{category}"]')
                ))
                checkbox.click()
                print(f"Clicked filter: {category}")

                try:
                    apply_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.filters-apply')))
                    apply_button.click()
                    print("Clicked 'Apply Filters'")
                    time.sleep(3)
                except:
                    print("'Apply Filters' not found or not required")

                self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.vehicle-card')))
                cards = self.driver.find_elements(By.CSS_SELECTOR, 'div.vehicle-card div.title.heading-04')

                print(f"Vehicles under '{category}':")
                for card in cards:
                    name = card.text.strip()
                    if name:
                        print("-", name)
                        self.vehicle_data.append({
                            "Category": category,
                            "vehicle_name": name,
                            "Electrified": "Yes" if name in self.electrified_vehicles else "No"
                        })

            except Exception as e:
                print(f"Failed for category '{category}':", e)

    def save_to_csv(self):
        df = pd.DataFrame(self.vehicle_data).drop_duplicates()
        df.to_csv(self.output_file, index=False)
        print(f"CSV file saved: {self.output_file}")

    def run(self):
        self.setup_driver()
        self.collect_electrified()
        self.collect_by_category()
        self.driver.quit()
        self.save_to_csv()


