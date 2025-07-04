import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "http://localhost:11434/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "ollama")

def call_local_llm(prompt: str, model="llama3", temperature=0.7, max_tokens=1000) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a soulful, honest, outsider-aware assistant that speaks from experience and reflection."},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    try:
        response = requests.post(f"{OPENAI_API_BASE}/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[ERROR] Local LLM call failed: {e}"
