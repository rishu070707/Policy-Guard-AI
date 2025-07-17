import chromadb
from utils import get_embedding, generate_decision


client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="insurance_claims")

def search_chunks(query, top_k=3):
    print(f"📨 Received query: {query}")
    
    query_embedding = get_embedding(query)
    if not query_embedding:
        raise ValueError("Invalid embedding.")

    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    chunks = results.get("documents", [[]])[0]

    print(f"✅ Top {len(chunks)} chunks found.")
    decision = generate_decision(query, chunks)
    return decision
