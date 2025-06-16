import os
import pandas as pd
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

class ToyotaRetriever:
    def __init__(self):
        load_dotenv()
        self.embedding = OpenAIEmbeddings()
        self.vectorstore = None
        self._load_and_index()

    def _load_and_index(self):
        specs = pd.read_csv("src/data/final/final_cleaned_toyota_specnew2.csv")
        faqs = pd.read_csv("src/data/final/toyota_vehicle_faqs.csv")

        spec_docs = [
            f"{row['vehicle_name_clean']} {row['model']} - {row['engine_specs']}, MSRP: {row['Mpg/Other/Price - Base MSRP']}, Seating: {row['seating']}"
            for _, row in specs.iterrows()
        ]
        faq_docs = [
            f"Q: {row['question']}\nA: {row['answer']}"
            for _, row in faqs.iterrows()
            if isinstance(row['answer'], str) and row['answer'].strip().lower() != "no content available"
        ]

        docs = [Document(page_content=txt) for txt in spec_docs + faq_docs]

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        split_docs = splitter.split_documents(docs)

        self.vectorstore = Chroma.from_documents(split_docs, self.embedding)

    def retrieve_context(self, query, k=4):
        matches = self.vectorstore.similarity_search(query, k=k)
        return "\n\n".join([doc.page_content for doc in matches])
