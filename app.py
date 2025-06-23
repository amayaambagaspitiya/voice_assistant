from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os

from src.voice_assistant.customer_promts import CustomerSimulator
from src.voice_assistant.retrieve_toyota import ToyotaRetriever
from src.voice_assistant.mic_input import WhisperMic
from src.voice_assistant.text_to_speech import speak

load_dotenv(dotenv_path="src/voice_assistant/.env")

app = FastAPI()

retriever = ToyotaRetriever()
simulator = CustomerSimulator(retriever)
whisper_mic = WhisperMic("base")


@app.get("/")
def read_root():
    return {"message": "Toyota voice assistant is running."}


@app.post("/chat")
def chat_with_customer(request: Request):
    try:
        sales_rep_input = request.query_params.get("query")
        if not sales_rep_input:
            return JSONResponse(content={"error": "Query missing"}, status_code=400)

        response = simulator.simulate(sales_rep_input)
        return {"response": response}

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
