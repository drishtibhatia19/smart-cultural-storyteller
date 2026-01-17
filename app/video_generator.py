from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, vfx
import os

IMAGE_DIR = "images"  # Directory where the images are stored
AUDIO_DIR = "audio"  # Directory where the audio files are stored
OUTPUT_FILE = "story_video.mp4"  # Final video output file

def generate_video_from_scenes():
    scene_files = sorted([
        f for f in os.listdir(IMAGE_DIR)
        if f.endswith(".png")
    ])

    clips = []

    for scene in scene_files:
        scene_number = scene.replace("scene_", "").replace(".png", "")
        image_path = os.path.join(IMAGE_DIR, scene)
        audio_path = os.path.join(AUDIO_DIR, f"scene_{scene_number}.mp3")

        audio_clip = AudioFileClip(audio_path)

        image_clip = (
            ImageClip(image_path)
            .set_duration(audio_clip.duration)
            .set_audio(audio_clip)
            .fx(vfx.fadein, 0.5)
            .fx(vfx.fadeout, 0.5)
        )

        clips.append(image_clip)

    final_video = concatenate_videoclips(clips, method="compose")

    final_video.write_videofile(
        OUTPUT_FILE,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )

    return OUTPUT_FILE  # Return the name of the generated video file

