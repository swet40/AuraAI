import moviepy.editor as mpy
from moviepy.editor import concatenate_videoclips
import os
from datetime import datetime

def create_video(images, voiceover_content, story, timestamp):
    # Create an output directory for this run
    output_dir = os.path.join("outputs", timestamp)
    os.makedirs(output_dir, exist_ok=True)

    # Save voiceover
    voiceover_filename = os.path.join(output_dir, f"voiceover_{timestamp}.mp3")
    with open(voiceover_filename, "wb") as f:
        f.write(voiceover_content)

    # Generate image file names based on the timestamp and the index
    image_filenames = [os.path.join(output_dir, f"image_{timestamp}_{idx}.png") for idx, _ in enumerate(images)]

    # Create video clips from images
    image_clips = [mpy.ImageClip(img).set_duration(5) for img in image_filenames]
    video_clip = concatenate_videoclips(image_clips, method="compose")

    # Set voiceover as audio
    video_clip = video_clip.set_audio(mpy.AudioFileClip(voiceover_filename))

    # Save final video
    video_filename = os.path.join(output_dir, f"output_video_{timestamp}.mp4")
    video_clip.write_videofile(video_filename, codec="libx264", fps=24)

    print(f"Video and assets saved to: {output_dir}")
