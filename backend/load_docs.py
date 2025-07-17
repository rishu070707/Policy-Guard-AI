import os
from PyPDF2 import PdfReader
from utils import get_embedding
import chromadb
from chromadb.config import Settings

client = chromadb.PersistentClient(path="./vector_store")

collection = client.get_or_create_collection(name="insurance_claims")

def extract_text_from_pdf(filepath):
    reader = PdfReader(filepath)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def chunk_text(text, chunk_size=150):
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

def save_all_to_vector_db(file_path):
    if not file_path.lower().endswith(".pdf"):
        print(f"❌ Skipping non-PDF file: {file_path}")
        return

    print(f"📄 Processing PDF: {file_path}")
    full_text = extract_text_from_pdf(file_path)
    chunks = chunk_text(full_text)

    for i, chunk in enumerate(chunks):
        embedding = get_embedding(chunk)
        if embedding:
            collection.add(
                documents=[chunk],
                embeddings=[embedding],
                ids=[f"{os.path.basename(file_path)}_{i}"]
            )
    print(f"✅ Stored {len(chunks)} chunks from {file_path}")


