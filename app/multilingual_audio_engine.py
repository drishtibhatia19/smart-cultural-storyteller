from pathlib import Path

from .models import Story
from .translation_client import translate_text
from .tts_client import generate_speech


def generate_audio_for_language(story: Story, lang: str) -> Story:
    """
    Generates narration audio for each scene in a target language.
    - Translates English text
    - Converts translated text to speech
    - Saves audio files
    - Attaches them to scene.translated_audio
    """
    base_dir = Path(__file__).resolve().parent.parent
    audio_dir = base_dir / "static" / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    for scene in story.scenes:
        try:
            translated_text = translate_text(scene.text, lang)

            audio_bytes = generate_speech(translated_text)

            audio_filename = f"scene_{scene.id}_{lang}.wav"
            audio_path = audio_dir / audio_filename

            with open(audio_path, "wb") as f:
                f.write(audio_bytes)

            if scene.translated_audio is None:
                scene.translated_audio = {}

            scene.translated_audio[lang] = f"static/audio/{audio_filename}"

        except Exception as e:
            print(
                f"[WARN] Multilingual audio generation failed "
                f"for scene {scene.id}, lang={lang}: {e}"
            )

    return story
