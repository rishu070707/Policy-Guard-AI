from sentence_transformers import SentenceTransformer
import numpy as np
import os
import requests

# Load embedding model once
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    try:
        return embedding_model.encode(text).tolist()
    except Exception as e:
        print("❌ Embedding error:", e)
        return None

def generate_decision(user_query, chunks):
    # Combine top retrieved chunks into context
    context = "\n".join(chunks)
    print("🔍 Retrieved Chunks:\n", context)

    # Construct prompt for decision-making
    prompt = f"""You are an expert insurance claims evaluator.

Context:
{context}

Question:
Is the following insurance claim allowed under the policy?
"{user_query}"

Respond with a simple yes or no and a short explanation."""

    # Call Groq API (or switch to OpenAI)
    try:
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {os.environ['GROQ_API_KEY']}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama3-8b-8192",  # Or use another Groq-supported model
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }
        response = requests.post(url, headers=headers, json=payload)
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        print("❌ Groq API error:", e)
        return "Error generating decision"
