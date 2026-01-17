import requests
from .config import HF_API_KEY, HF_TTS_API_URL


def generate_speech(text: str) -> bytes:
    """
    Converts text to speech using Hugging Face TTS model.
    Returns raw audio bytes (WAV).
    """
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": text
    }

    response = requests.post(
        HF_TTS_API_URL,
        headers=headers,
        json=payload,
        timeout=120
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"TTS generation failed: {response.status_code} - {response.text}"
        )

    return response.content
