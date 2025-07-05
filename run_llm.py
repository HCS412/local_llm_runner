# local_llm_runner/run_llm.py

import subprocess

DEFAULT_MODEL = "tinyllama"

def run_llm(prompt: str, model: str = DEFAULT_MODEL) -> str:
    """
    Runs a local LLM using Ollama with the specified prompt.
    Defaults to TinyLlama.
    """
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"[LLM Error] {e.stderr.strip()}"
    except Exception as e:
        return f"[Unexpected Error] {str(e)}"

# Optional test
if __name__ == "__main__":
    prompt = "Tell me a fun fact about octopuses."
    output = run_llm(prompt)
    print(output)
