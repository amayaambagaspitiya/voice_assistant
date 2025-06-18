from src.data_scrapping.scrape_toyota_sub_links import VehicleNames
from src.data_scrapping.extract_text_from_links import ToyotaSpecScraper
from src.data_scrapping.extract_text_from_filters import ToyotaVehicleScraper
from src.data_scrapping.extract_seat_numbers import ToyotaSeatingScraper
from src.data_scrapping.create_csv_from_text import VehicleSpecsParser
from src.data_scrapping.faq_scraping import ToyotaFAQScraper
from src.voice_assistant.customer_promts import CustomerSimulator
from src.voice_assistant.retrieve_toyota import ToyotaRetriever

def main():
    vehicle_scraper = VehicleNames()
    vehicle_scraper.run()

    spec_scraper = ToyotaSpecScraper()
    spec_scraper.extract_specs()

    category_scraper = ToyotaVehicleScraper()
    category_scraper.run()

    seating_scraper = ToyotaSeatingScraper()
    seating_scraper.run()

    spec_parser = VehicleSpecsParser()
    spec_parser.parse()

    scraper = ToyotaFAQScraper(load_more_clicks=80, output_csv="toyota_vehicle_faqs.csv", headless=False)
    scraper.run()





if __name__ == "__main__":
    main()


