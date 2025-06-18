import os
import pandas as pd
import yaml
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

class ToyotaRetriever:
    def __init__(self, config_path="config.yaml"):
        load_dotenv()
        self.config = self._load_config(config_path)
        self.embedding = OpenAIEmbeddings()
        self.vectorstore = None
        self._load_and_index()

    def _load_config(self, path):
        with open(path, "r") as file:
            return yaml.safe_load(file)

    def _load_and_index(self):
        spec_path = self.config["paths"]["specs_csv"]
        faq_path = self.config["paths"]["faqs_csv"]
        chunk_size = self.config["embedding"]["chunk_size"]
        chunk_overlap = self.config["embedding"]["chunk_overlap"]

        specs = pd.read_csv(spec_path)
        faqs = pd.read_csv(faq_path)

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

        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        split_docs = splitter.split_documents(docs)

        self.vectorstore = Chroma.from_documents(split_docs, self.embedding)

    def retrieve_context(self, query, k=4):
        matches = self.vectorstore.similarity_search(query, k=k)
        return "\n\n".join([doc.page_content for doc in matches])
