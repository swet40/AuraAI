import moviepy.editor as mpy
from moviepy.editor import concatenate_videoclips
import os
from datetime import datetime
import numpy as np
from io import BytesIO

def create_video(image_arrays, voiceover_content, story, timestamp):

    output_dir = os.path.join("outputs", timestamp)
    os.makedirs(output_dir, exist_ok=True)


    voiceover_filename = os.path.join(output_dir, f"voiceover_{timestamp}.mp3")
    with open(voiceover_filename, "wb") as f:
        f.write(voiceover_content)


    image_clips = [mpy.ImageClip(img).set_duration(5) for img in image_arrays]
    if not image_clips:
            raise ValueError("No image clips available to create the video.")
            
    if not image_clips:
        raise ValueError("No image clips available to create the video. Please check your image generation step.")

    video_clip = concatenate_videoclips(image_clips, method="compose")


    video_clip = video_clip.set_audio(mpy.AudioFileClip(voiceover_filename))

    video_filename = os.path.join(output_dir, f"output_video_{timestamp}.mp4")
    video_clip.write_videofile(video_filename, codec="libx264", fps=24)

    print(f"Video and assets saved to: {output_dir}")