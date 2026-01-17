import requests
from .config import HF_API_KEY, HF_IMAGE_API_URL


def generate_image(prompt: str) -> bytes:
    """
    Calls Hugging Face image generation model
    and returns raw image bytes.
    """
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Accept": "image/png"
    }

    payload = {
        "inputs": prompt
    }

    response = requests.post(
        HF_IMAGE_API_URL,
        headers=headers,
        json=payload,
        timeout=120
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Image generation failed: {response.status_code} - {response.text}"
        )

    return response.content
