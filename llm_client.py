import os
import requests
from dotenv import load_dotenv

# ─── Load .env ──────────────────────────────────────────────
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

# ─── Config ─────────────────────────────────────────────────
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "http://localhost:1234/v1")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "ollama")
DEFAULT_MODEL = os.getenv("LLM_MODEL", "llama3")

# ─── System Prompt Templates ───────────────────────────────
SYSTEM_PROMPTS = {
    "technical": "You're a precise, efficient technical assistant. Respond clearly with helpful answers or working code.",
    "social": "You're a soulful, reflective outsider who brings truth, clarity, and cultural depth to your answers.",
    "venture": "You're a sharp, contrarian thinker. Offer practical insight and real-world startup savvy.",
    "default": "You're clear, honest, and helpful. Answer with integrity and relevance."
}

# ─── LLM Client ─────────────────────────────────────────────
def call_local_llm(prompt: str, prompt_type: str = "default", model: str = DEFAULT_MODEL, temperature: float = 0.7, max_tokens: int = 500) -> str:
    system_prompt = SYSTEM_PROMPTS.get(prompt_type, SYSTEM_PROMPTS["default"])

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

    try:
        response = requests.post(f"{OPENAI_API_BASE}/chat/completions", headers=headers, json=payload)
        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"].strip()

    except requests.exceptions.ConnectionError as ce:
        return f"[ERROR] ConnectionError: Could not reach LLM endpoint. Details: {ce}"

    except requests.exceptions.HTTPError as he:
        return f"[ERROR] HTTPError: {response.text}"

    except Exception as e:
        return f"[ERROR] Unexpected Exception: {e}"
