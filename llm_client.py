import os
import requests
from dotenv import load_dotenv

# ─── Explicitly load .env from script's directory ───────────────────────────────
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
env_loaded = load_dotenv(dotenv_path)

# ─── Debugging environment setup ────────────────────────────────────────────────
print("🔍 Loading environment variables from .env...")
print(f"✅ .env loaded: {env_loaded}")
print(f"📁 Current working directory: {os.getcwd()}")
print(f"📄 Looking for .env at: {dotenv_path}")

if os.path.exists(dotenv_path):
    print("📝 .env file found! Contents:")
    with open(dotenv_path, "r") as f:
        print(f.read())
else:
    print("❌ .env file not found!")

# ─── Get LLM connection info ────────────────────────────────────────────────────
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "http://localhost:1234/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "ollama")

print(f"🌐 OPENAI_API_BASE: {OPENAI_API_BASE}")
print(f"🔐 OPENAI_API_KEY: {OPENAI_API_KEY}")
print("🚦 Testing connection to LLM...")

try:
    health = requests.get(OPENAI_API_BASE)
    print(f"✅ LLM is reachable. Status: {health.status_code}")
except Exception as e:
    print(f"❌ Could not reach LLM at {OPENAI_API_BASE}: {e}")

# ─── LLM Client Function ────────────────────────────────────────────────────────
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

    print("\n📡 Sending request to LLM...")
    print(f"🔸 POST {OPENAI_API_BASE}/chat/completions")
    print(f"🔸 Headers: {headers}")
    print(f"🔸 Payload: {payload}")

    try:
        response = requests.post(f"{OPENAI_API_BASE}/chat/completions", headers=headers, json=payload)
        print(f"📬 Status Code: {response.status_code}")
        print(f"📨 Response Preview: {response.text[:300]}...")

        response.raise_for_status()
        result = response.json()["choices"][0]["message"]["content"].strip()
        print("✅ Parsed LLM response successfully.")
        return result

    except requests.exceptions.ConnectionError as ce:
        print("❌ ConnectionError: Failed to connect to LLM endpoint.")
        return f"[ERROR] ConnectionError while calling local LLM: {ce}"

    except requests.exceptions.HTTPError as he:
        print("❌ HTTPError: LLM returned an error response.")
        return f"[ERROR] HTTPError while calling local LLM: {he}"

    except Exception as e:
        print("❌ Unexpected error occurred.")
        return f"[ERROR] Unexpected exception during LLM call: {e}"
