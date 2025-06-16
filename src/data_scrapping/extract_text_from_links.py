import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ToyotaSpecScraper:
    def __init__(self, csv_path="src/data/intermediate/toyota_all_vehicle_names_links.csv", output_dir="src/data/intermediate/specs_output_text", headless=True):
        self.csv_path = csv_path
        self.output_dir = output_dir
        self.headless = headless
        os.makedirs(self.output_dir, exist_ok=True)

    def load_vehicle_links(self):
        df = pd.read_csv(self.csv_path)
        return df[df['link'].notnull()]

    def setup_driver(self):
        options = Options()
        if self.headless:
            options.add_argument("--headless")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        driver = webdriver.Chrome(options=options)
        return driver

    def extract_specs(self):
        vehicle_df = self.load_vehicle_links()
        driver = self.setup_driver()
        wait = WebDriverWait(driver, 15)

        for _, row in vehicle_df.iterrows():
            name = row['name'].replace(" ", "_").lower()
            year = str(row['year'])
            url = row['link'].rstrip('/') + "/features/mpg_other_price/"
            print(f"Visiting: {url}")

            try:
                driver.get(url)
                time.sleep(5)

                # Expand all collapsible sections
                toggles = driver.find_elements(By.CSS_SELECTOR, "div.feature-accordions button.tcom-accordion-header")
                print(f"Found {len(toggles)} collapsible sections")

                for toggle in toggles:
                    try:
                        if toggle.get_attribute("aria-expanded") == "false":
                            driver.execute_script("arguments[0].click();", toggle)
                            time.sleep(0.8)
                    except Exception as e:
                        print("Error expanding section:", e)

                time.sleep(1.5)

                # Extract full container text
                container = driver.find_element(By.CSS_SELECTOR, "div.app-content-container")
                full_text = container.text.strip()

                output_path = os.path.join(self.output_dir, f"{year}_{name}_specs.txt")
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(full_text)

                print(f"Saved to {output_path}")

            except Exception as e:
                print(f"Error processing {url}: {e}")

        driver.quit()



