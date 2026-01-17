import requests
from .config import HF_API_KEY, HF_TRANSLATION_API_URL


def translate_text(text: str, target_lang: str) -> str:
    """
    Translates English text to a target language using Hugging Face.
    target_lang examples: 'hi' (Hindi), 'gu' (Gujarati)
    """
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": text,
        "parameters": {
            "src_lang": "eng_Latn",
            "tgt_lang": _map_language_code(target_lang)
        }
    }

    response = requests.post(
        HF_TRANSLATION_API_URL,
        headers=headers,
        json=payload,
        timeout=120
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Translation failed: {response.status_code} - {response.text}"
        )

    result = response.json()

    if isinstance(result, list) and "translation_text" in result[0]:
        return result[0]["translation_text"]

    return str(result)


def _map_language_code(lang: str) -> str:
    """
    Maps simple language codes to NLLB language tags.
    """
    mapping = {
        "hi": "hin_Deva",   # Hindi
        "gu": "guj_Gujr",   # Gujarati
        "mr": "mar_Deva",   # Marathi (optional)
        "bn": "ben_Beng",   # Bengali (optional)
    }

    if lang not in mapping:
        raise ValueError(f"Unsupported language: {lang}")

    return mapping[lang]
