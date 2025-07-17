import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def extract_details(query):
    prompt = f"""
Extract the following fields from this insurance claim:
- age
- gender
- procedure
- location
- policy duration

Query: "{query}"

Return only a JSON object with those fields.
"""

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content
