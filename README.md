# voice_assistant
 This project builds a voice-based assistant for Toyota sales representatives to simulate conversations with different customer personas and answer questions using real vehicle specs and FAQs. Below is the end-to-end workflow:

1. Data Collection
Toyota Specs: Scraped vehicle specification pages  using Selenium.
 FAQs: Scraped and cleaned frequently asked questions using BeautifulSoup and custom logic.

2. Data Preprocessing
Parsed unstructured spec data from .txt files into structured .csv format.

Cleaned and formatted FAQ data.

Combined vehicle info (engine, MSRP, seating, etc.) into dense retrievable text chunks.

3. Vector Store & Retrieval Setup (RAG)
Used LangChain to embed vehicle specs and FAQs using OpenAIEmbeddings.

Stored embeddings in a local vector store chroma.

Implemented a retriever to fetch relevant information based on user queries.

4. Prompt Engineering
Designed 5 distinct customer personas with different tones and question styles.

Created prompt templates for each persona.

Logic to randomly select a prompt per conversation session.

5. Voice Input (Speech-to-Text)
Used Whisper (open-source STT model by OpenAI) to convert user speech to text.

Handled microphone recording and audio saving using sounddevice and scipy.

6. GPT Response Generation
Injected sales rep response into a selected persona prompt.

Queried OpenAI GPT model  with prompt + retriever context.

Generated a natural language reply based on the persona.

7. Voice Output (Text-to-Speech)
Converted GPT-generated text back to speech using pyttsx3.

Played the audio response to complete the voice interaction loop.



