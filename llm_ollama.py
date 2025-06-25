import requests

# URL for Ollama's REST API
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "deepseek-r1:8b"


def query_ollama(prompt: str, model: str = MODEL_NAME) -> str:
    """
    Sends `prompt` to Ollama and returns the raw text response.
    Raises on HTTP or JSON errors.
    """
    payload = {"model": model, "prompt": prompt, "stream": False}
    resp = requests.post(OLLAMA_URL, json=payload)
    resp.raise_for_status()
    data = resp.json()
    return data.get("response", "")