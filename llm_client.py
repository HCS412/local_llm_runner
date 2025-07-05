import os
import requests
from dotenv import load_dotenv

# ──────────────────────────────────────────────────────────────────────
# Load .env configuration from script's directory
# ──────────────────────────────────────────────────────────────────────
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
env_loaded = load_dotenv(dotenv_path)

print("\033[94m🔍 Loading .env...\033[0m")
print(f"✅ Loaded: {env_loaded}")
print(f"📁 CWD: {os.getcwd()}")
print(f"📄 Using .env: {dotenv_path}")

if os.path.exists(dotenv_path):
    with open(dotenv_path, "r") as f:
        print("📝 .env Contents:\n" + f.read())
else:
    print("❌ .env not found at expected path.")

# ──────────────────────────────────────────────────────────────────────
# Load API configuration
# ──────────────────────────────────────────────────────────────────────
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "http://localhost:1234/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "ollama")

print(f"\033[96m🌐 API Base:\033[0m {OPENAI_API_BASE}")
print(f"\033[96m🔐 API Key:\033[0m {OPENAI_API_KEY}")
print("🚦 Checking LLM connection...")

try:
    r = requests.get(OPENAI_API_BASE)
    print(f"✅ LLM reachable (status {r.status_code})")
except Exception as e:
    print(f"❌ LLM unreachable: {e}")

# ──────────────────────────────────────────────────────────────────────
# System prompt templates by mode
# ──────────────────────────────────────────────────────────────────────
SYSTEM_PROMPTS = {
    "soulful": "You are a soulful, honest, outsider-aware assistant that speaks from experience and reflection.",
    "strategic": "You are a sharp, practical, and high-signal strategist. Prioritize clarity, brevity, and real-world execution.",
    "neutral": "You are a helpful and insightful assistant who communicates clearly and concisely."
}

# ──────────────────────────────────────────────────────────────────────
# Call Local LLM
# ──────────────────────────────────────────────────────────────────────
def call_local_llm(prompt: str, model="llama3", temperature=0.7, max_tokens=500, mode="neutral") -> str:
    system_prompt = SYSTEM_PROMPTS.get(mode, SYSTEM_PROMPTS["neutral"])

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    payload = {
        "model": model,
        "messages": [
            { "role": "system", "content": system_prompt },
            { "role": "user", "content": prompt }
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    print("\n📡 Sending to LLM:")
    print(f"🔸 POST → {OPENAI_API_BASE}/chat/completions")
    print(f"🔸 Model: {model}")
    print(f"🔸 Max Tokens: {max_tokens}")
    print(f"🔸 Mode: {mode}")
    print(f"🔸 System Prompt: {system_prompt[:80]}...")

    try:
        response = requests.post(f"{OPENAI_API_BASE}/chat/completions", headers=headers, json=payload)
        response.raise_for_status()

        content = response.json()["choices"][0]["message"]["content"].strip()

        preview = content[:500] + ("... [Truncated]" if len(content) > 500 else "")
        print("\n📨 Response Preview:")
        print(preview)

        return content

    except requests.exceptions.ConnectionError as ce:
        print("❌ ConnectionError: Could not reach LLM endpoint.")
        return f"[ERROR] ConnectionError: {ce}"

    except requests.exceptions.HTTPError as he:
        print("❌ HTTPError: Invalid response from LLM.")
        return f"[ERROR] HTTPError: {response.text}"

    except Exception as e:
        print("❌ Unexpected Error:")
        return f"[ERROR] Unexpected Exception: {e}"
