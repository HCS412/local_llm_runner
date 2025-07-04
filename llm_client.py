import os
import requests
from dotenv import load_dotenv

# DEBUG: Load .env file and confirm it works
print("🔍 Loading environment variables from .env...")
env_loaded = load_dotenv()
print(f"✅ .env loaded: {env_loaded}")

# DEBUG: Print current working directory and file contents
print(f"📁 Current working directory: {os.getcwd()}")
if os.path.exists(".env"):
    print("📝 .env file found! Contents:")
    with open(".env", "r") as f:
        print(f.read())
else:
    print("❌ .env file not found in this directory!")

# Get environment variables
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "http://localhost:1234/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "ollama")

# DEBUG: Show what values are being used
print(f"🌐 Using LLM API base: {OPENAI_API_BASE}")
print(f"🔐 Using API key: {OPENAI_API_KEY}")

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
        print("📡 Sending request to LLM...")
        response = requests.post(f"{OPENAI_API_BASE}/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()["choices"][0]["message"]["content"].strip()
        print("✅ Received response from LLM.")
        return result
    except Exception as e:
        print(f"❌ Error while calling LLM: {e}")
        return f"[ERROR] Local LLM call failed: {e}"
