from src.data_scrapping.extract_seat_numbers import ToyotaSeatingScraper
from src.data_scrapping.create_csv_from_text import VehicleSpecsParser
from src.data_scrapping.faq_scraping import ToyotaFAQScraper
from src.voice_assistant.customer_promts import CustomerSimulator
from src.voice_assistant.retrieve_toyota import ToyotaRetriever
from src.voice_assistant.mic_input import  WhisperMic
from src.voice_assistant.text_to_speech import speak


retriever = ToyotaRetriever()
simulator = CustomerSimulator(retriever)

sales_rep_input = "hi hope you are doing well" \


customer_response = simulator.simulate(sales_rep_input)

print("\n--- TEST RESULT ---")
print("Sales Rep:", sales_rep_input)
print("Assistant Response:", customer_response)