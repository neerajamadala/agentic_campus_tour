import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings

# Load API key from .env
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Path to folder containing text files
DATA_FOLDER = "data"
PERSIST_DIR = "db"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

def ingest():
    documents = []

    # Loop through all .txt files in the data folder
    for file in os.listdir(DATA_FOLDER):
        if file.endswith(".txt"):
            loader = TextLoader(os.path.join(DATA_FOLDER, file), encoding="utf-8")
            docs = loader.load()

            # Add metadata to identify the source (e.g., 'library', 'courses', 'events')
            source_name = file.split(".")[0]
            for doc in docs:
                doc.metadata = {"source": source_name}

            documents.extend(docs)
            print(f"✅ Loaded {len(docs)} documents from {file}")

    # Split documents into chunks
    text_splitter = CharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    docs = text_splitter.split_documents(documents)
    print(f"✅ Split into {len(docs)} chunks")

    # Generate embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    # Store in Chroma vector database
    vectordb = Chroma.from_documents(docs, embeddings, persist_directory=PERSIST_DIR)
    vectordb.persist()
    print(f"✅ Ingestion complete! Knowledge base is ready in '{PERSIST_DIR}'")

if __name__ == "__main__":
    ingest()
