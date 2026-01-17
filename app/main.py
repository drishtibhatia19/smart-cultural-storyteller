from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from dotenv import load_dotenv
from fastapi import Body
from uuid import uuid4
from pathlib import Path


load_dotenv()

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent.parent

app.mount(
    "/frontend",
    StaticFiles(directory=BASE_DIR / "frontend", html=True),
    name="frontend"
)

app.mount(
    "/generated_images",
    StaticFiles(directory=BASE_DIR / "generated_images"),
    name="generated_images"
)

app.mount(
    "/generated_audio",
    StaticFiles(directory=BASE_DIR / "generated_audio"),
    name="generated_audio"
)

@app.get("/")
def serve_index():
    return FileResponse(BASE_DIR / "frontend" / "index.html")


from .models import StoryRequest
from .story_engine import generate_story_pipeline


@app.post("/api/generate-story")
def generate_story(req: StoryRequest):
    """
    Generates:
    - Story text
    - Images (OpenAI)
    - Audio narration (OpenAI)
    """
    result = generate_story_pipeline(req)
    return result

@app.post("/api/generate-narration")
def generate_narration(payload: dict = Body(...)):
    """
    Generates narration audio for a single scene.
    Returns a URL to the generated MP3 file.
    """

    text = payload.get("text")
    title = payload.get("title", "scene")

    if not text:
        return {"error": "No text provided"}

    audio_dir = BASE_DIR / "generated_audio"
    audio_dir.mkdir(exist_ok=True)

    filename = f"{title.replace(' ', '_')}_{uuid4().hex[:6]}.mp3"
    audio_path = audio_dir / filename

    from openai import OpenAI
    client = OpenAI()

    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    ) as response:
        response.stream_to_file(audio_path)

    return {
        "audio_url": f"/generated_audio/{filename}"
    }

from fastapi import Body
from uuid import uuid4
from pathlib import Path

@app.post("/api/generate-image")
def generate_image(payload: dict = Body(...)):
    """
    Generates an image for a single scene using Hugging Face (Stable Diffusion).
    Returns a URL to the generated image.
    """

    from huggingface_hub import InferenceClient
    from PIL import Image

    text = payload.get("text")
    title = payload.get("title", "scene")

    if not text:
        return {"error": "No text provided"}

    image_dir = BASE_DIR / "generated_images"
    image_dir.mkdir(exist_ok=True)

    filename = f"{title.replace(' ', '_')}_{uuid4().hex[:6]}.png"
    image_path = image_dir / filename

    import os
    client = InferenceClient(model="stabilityai/stable-diffusion-xl-base-1.0",token=os.getenv("HF_API_TOKEN"))

    print("HF TOKEN FOUND:", os.getenv("HF_API_TOKEN"))



    prompt = f"""
    Cinematic mythological illustration.
    Scene title: {title}
    Scene description: {text}
    Highly detailed, epic lighting, cultural authenticity.
    """

    image = client.text_to_image(prompt)
    image.save(image_path)

    return {
        "image_url": f"/generated_images/{filename}"
    }

app.mount(
    "/generated_videos",
    StaticFiles(directory=BASE_DIR / "generated_videos"),
    name="generated_videos"
)

@app.post("/api/generate-video")
def generate_video(payload: dict = Body(...)):
    """
    Combines generated image + narration into a video (MP4).
    """

    from moviepy.editor import ImageClip, AudioFileClip
    from uuid import uuid4

    title = payload.get("title", "scene")
    image_url = payload.get("image_url")
    audio_url = payload.get("audio_url")

    if not image_url or not audio_url:
        return {"error": "image_url and audio_url required"}

    image_path = BASE_DIR / image_url.lstrip("/")
    audio_path = BASE_DIR / audio_url.lstrip("/")

    video_dir = BASE_DIR / "generated_videos"
    video_dir.mkdir(exist_ok=True)

    filename = f"{title.replace(' ', '_')}_{uuid4().hex[:6]}.mp4"
    video_path = video_dir / filename

    audio = AudioFileClip(str(audio_path))

    clip = (
        ImageClip(str(image_path))
        .set_duration(audio.duration)
        .set_audio(audio)
        .resize(width=1280)
    )

    clip.write_videofile(
        str(video_path),
        fps=24,
        codec="libx264",
        audio_codec="aac",
        threads=4
    )

    return {
        "video_url": f"/generated_videos/{filename}"
    }


