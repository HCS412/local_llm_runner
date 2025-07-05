import os
import requests
from dotenv import load_dotenv

# ─── Load .env from local directory ─────────────────────────────────
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

# ─── API Config ─────────────────────────────────────────────────────
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

# ─── Determine prompt type ──────────────────────────────────────────
def classify_prompt_type(prompt: str) -> str:
    lowered = prompt.lower()
    if any(word in lowered for word in ["build", "design", "code", "implement", "api", "database", "python", "algorithm"]):
        return "technical"
    elif any(word in lowered for word in ["justice", "race", "gender", "equity", "identity", "culture", "marginalized"]):
        return "social"
    elif any(word in lowered for word in ["startup", "founder", "investor", "fund", "venture", "capital", "business"]):
        return "venture"
    return "default"

# ─── Map system prompts by type ─────────────────────────────────────
SYSTEM_PROMPTS = {
    "technical": "You are a precise, efficient technical assistant who gives clean, useful code and answers.",
    "social": "You are a soulful, reflective, and honest voice that challenges power with empathy and insight.",
    "venture": "You are a sharp, contrarian thinker who understands startups, capital flows, and edge.",
    "default": "You are thoughtful and clear, focused on delivering truth and reflection from many angles."
}

# ─── LLM Client Function ────────────────────────────────────────────
def call_local_llm(prompt: str, model="llama3", temperature=0.7, max_tokens=500) -> str:
    prompt_type = classify_prompt_type(prompt)
    system_prompt = SYSTEM_PROMPTS[prompt_type]

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    print(f"\n📡 Sending → {prompt_type.upper()} | {model} | {max_tokens} tokens")
    print(f"🔸 System Prompt:\n{system_prompt[:100]}...")

    try:
        response = requests.post(f"{OPENAI_API_BASE}/chat/completions", headers=headers, json=payload)
        response.raise_for_status()

        content = response.json()["choices"][0]["message"]["content"].strip()
        preview = content[:500] + ("... [Truncated]" if len(content) > 500 else "")
        print("\n📨 Response Preview:\n" + preview)

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
