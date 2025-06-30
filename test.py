from src.data_scrapping.extract_seat_numbers import ToyotaSeatingScraper
from src.data_scrapping.create_csv_from_text import VehicleSpecsParser
from src.data_scrapping.faq_scraping import ToyotaFAQScraper
from src.voice_assistant.customer_promts import CustomerSimulator
from src.voice_assistant.retrieve_toyota import ToyotaRetriever
from src.voice_assistant.mic_input import  WhisperMic
from src.voice_assistant.text_to_speech import speak
import pyttsx3


# engine = pyttsx3.init()
# voices = engine.getProperty("voices")
# for v in voices:
#     print(f"Name: {v.name}, ID: {v.id}")

def main():
    retriever = ToyotaRetriever()
    simulator = CustomerSimulator(retriever)

    while True:
        try:
            sales_rep_input = input("\nType your sales rep message (or type 'exit' to quit): ")
            if sales_rep_input.strip().lower() == "exit":
                break

            response = simulator.simulate(sales_rep_input)
            persona_name = simulator.current_persona  
            speak(response, persona_name)            

        except KeyboardInterrupt:
            print("\nExiting.")
            break

if __name__ == "__main__":
    main()
