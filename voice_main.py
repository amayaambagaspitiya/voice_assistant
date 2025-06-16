from src.data_scrapping.scrape_toyota_sub_links import VehicleNames
from src.data_scrapping.extract_text_from_links import ToyotaSpecScraper
from src.data_scrapping.extract_text_from_filters import ToyotaVehicleScraper
from src.data_scrapping.extract_seat_numbers import ToyotaSeatingScraper
from src.data_scrapping.create_csv_from_text import VehicleSpecsParser
from src.data_scrapping.faq_scraping import ToyotaFAQScraper
from src.voice_assistant.customer_promts import CustomerSimulator
from src.voice_assistant.retrieve_toyota import ToyotaRetriever
from src.voice_assistant.mic_input import WhisperMic
from src.voice_assistant.text_to_speech import speak


def main():
    retriever = ToyotaRetriever()
    simulator = CustomerSimulator(retriever)
    whisper_mic = WhisperMic("base")


    while True:
            input("\nPress Enter to record your question (or Ctrl+C to exit)...")
            
            audio_path = whisper_mic.record(duration=6)
            
            sales_rep_input = whisper_mic.transcribe(audio_path)

            response = simulator.simulate(sales_rep_input)

            speak(response)

if __name__ == "__main__":
    main()

