from pathlib import Path
from .models import Story



MUSIC_LIBRARY = {
    "Stillness": "stillness.mp3",
    "Hope": "hope.mp3",
    "Reflection": "reflection.mp3",
    "Resilience": "resilience.mp3",
    "Renewal": "renewal.mp3"
}


def attach_music_to_story(story: Story) -> Story:
    """
    Attaches background music paths to each scene
    based on the scene's music mood.
    """
    base_dir = Path(__file__).resolve().parent.parent
    music_dir = base_dir / "static" / "music"
    music_dir.mkdir(parents=True, exist_ok=True)

    for scene in story.scenes:
        mood = scene.music_mood

        music_file = MUSIC_LIBRARY.get(mood, "stillness.mp3")

        scene.background_music = f"static/music/{music_file}"

    return story
