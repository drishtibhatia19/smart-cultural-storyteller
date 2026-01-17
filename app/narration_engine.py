import os
import uuid
from openai import OpenAI

client = OpenAI()

AUDIO_DIR = "generated_audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

def generate_narration(text: str):
    """
    Converts story text into narrated audio (mp3)
    """
    filename = f"{uuid.uuid4()}.mp3"
    file_path = os.path.join(AUDIO_DIR, filename)

    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",   # calm, neutral storyteller voice
        input=text
    )

    with open(file_path, "wb") as f:
        f.write(response)

    return {
        "audio_url": f"/generated_audio/{filename}"
    }
