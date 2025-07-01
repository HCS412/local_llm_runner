# llm_client.py

import requests

def call_local_llm(prompt: str, model="local-model", temperature=0.7, max_tokens=1000) -> str:
    headers = {"Content-Type": "application/json"}
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
        response = requests.post("http://localhost:1234/v1/chat/completions", headers=headers, json=payload)
        return response.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[ERROR] Local LLM call failed: {e}"
