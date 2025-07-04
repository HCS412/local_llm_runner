import os
import requests
from dotenv import load_dotenv

# ──────────────────────────────────────────────
# DEBUG: Load .env and inspect environment setup
# ──────────────────────────────────────────────
print("🔍 Loading environment variables from .env...")
env_loaded = load_dotenv()
print(f"✅ .env loaded: {env_loaded}")

print(f"📁 Current working directory: {os.getcwd()}")
if os.path.exists(".env"):
    print("📝 .env file found! Contents:")
    with open(".env", "r") as f:
        print(f.read())
else:
    print("❌ .env file not found in this directory!")

# ──────────────────────────────────────────────
# Extract + show environment values
# ──────────────────────────────────────────────
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "http://localhost:1234/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "ollama")

print(f"🌐 OPENAI_API_BASE: {OPENAI_API_BASE}")
print(f"🔐 OPENAI_API_KEY: {OPENAI_API_KEY}")
print("🚦 Confirming if URL is reachable...")

try:
    health_check = requests.get(OPENAI_API_BASE)
    print(f"✅ Base URL reachable — status code: {health_check.status_code}")
except Exception as e:
    print(f"❌ Could not reach base URL: {e}")

# ──────────────────────────────────────────────
# LLM call function with complete trace logging
# ──────────────────────────────────────────────
def call_local_llm(prompt: str, model="llama3", temperature=0.7, max_tokens=1000) -> str:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are a soulful, honest, outsider-aware assistant that speaks from experience and reflection."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    print("\n📡 Sending request to LLM...")
    print(f"🔸 POST to: {OPENAI_API_BASE}/chat/completions")
    print(f"🔸 Headers: {headers}")
    print(f"🔸 Payload:\n{payload}")

    try:
        response = requests.post(f"{OPENAI_API_BASE}/chat/completions", headers=headers, json=payload)
        print(f"📬 Response status code: {response.status_code}")
        print(f"📨 Response body: {response.text[:500]}...")  # print first 500 chars max

        response.raise_for_status()

        result = response.json()["choices"][0]["message"]["content"].strip()
        print("✅ LLM response parsed successfully.\n")
        return result

    except requests.exceptions.ConnectionError as ce:
        print("❌ ConnectionError: Could not connect to the LLM endpoint.")
        print(str(ce))
        return "[ERROR] ConnectionError while calling local LLM."

    except requests.exceptions.HTTPError as he:
        print("❌ HTTPError: Response error from LLM endpoint.")
        print(str(he))
        return f"[ERROR] HTTPError while calling local LLM: {response.text}"

    except Exception as e:
        print("❌ Unexpected error:")
        print(str(e))
        return f"[ERROR] Unexpected failure during LLM call: {e}"
