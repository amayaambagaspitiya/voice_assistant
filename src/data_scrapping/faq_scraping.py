import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ToyotaFAQScraper:
    def __init__(self, load_more_clicks=80, output_csv="src/data/final/toyota_vehicle_faqs.csv", headless=False):
        self.load_more_clicks = load_more_clicks
        self.output_csv = output_csv
        self.headless = headless
        self.driver = None
        self.wait = None
        self.faq_data = []

    def setup_driver(self):
        options = Options()
        options.add_argument("--start-maximized")
        if self.headless:
            options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def scrape_faqs(self):
        self.driver.get("https://support.toyota.com/s/?language=en_US")

        try:
            vehicles_link = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '/vehicles') and contains(@class, 'topicLink')]"))
            )
            vehicles_link.click()
        except Exception as e:
            print("Failed to click Vehicles link:", e)
            self.driver.quit()
            return

        for _ in range(self.load_more_clicks):
            try:
                load_more_btn = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "loadmore")))
                self.driver.execute_script("arguments[0].click();", load_more_btn)
                time.sleep(2)
            except:
                print("No more 'Load More' button.")
                break

        faq_links = self.driver.find_elements(By.CSS_SELECTOR, "li.article-item.selfServiceArticleListItem a")
        article_urls = list({link.get_attribute("href") for link in faq_links if link.get_attribute("href")})
        print(f"Found {len(article_urls)} article links.")

        for url in article_urls:
            try:
                self.driver.get(url)
                WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "article")))
                time.sleep(1)

                
                try:
                    question = self.driver.find_element(By.CSS_SELECTOR, "article.summary h2.article-head").text.strip()
                except:
                    question = "No question found"

                try:
                    answer = self.driver.find_element(
                        By.CSS_SELECTOR,
                        "span.test-id_field-value div.slds-rich-text-editor__output"
                    ).text.strip()
                except:
                    try:
                        answer = self.driver.find_element(
                            By.CSS_SELECTOR,
                            "article.content div.full.forcePageBlock.forceRecordLayout"
                        ).text.strip()
                    except:
                        answer = "No content available"

                self.faq_data.append({"question": question, "answer": answer})
                print(f"Scraped: {question[:60]}...")

            except Exception as e:
                print(f"Error at {url}: {e}")

        self.driver.quit()

    def preprocess_faqs(self):
        df = pd.DataFrame(self.faq_data)

        # Drop null or empty values
        df = df.dropna(subset=["question", "answer"])
        df = df[df["question"].str.strip() != ""]
        df = df[df["answer"].str.strip() != ""]

        placeholders = ["No question found", "No content available"]
        df = df[~df["question"].isin(placeholders)]
        df = df[~df["answer"].isin(placeholders)]

        df = df.drop_duplicates(subset=["question"])

        df["question"] = df["question"].str.strip().str.capitalize()
        df["answer"] = df["answer"].str.replace("\r", "", regex=False).str.strip()
        df["answer"] = df["answer"].apply(lambda x: re.sub(r"\s{2,}", " ", x))

        df = df[df["answer"].str.len() > 30]

        self.cleaned_df = df

    def save_to_csv(self):
        self.cleaned_df.to_csv(self.output_csv, index=False)
        print(f"Saved cleaned FAQ data to: {self.output_csv}")

    def run(self):
        self.setup_driver()
        self.scrape_faqs()
        self.preprocess_faqs()
        self.save_to_csv()


   
