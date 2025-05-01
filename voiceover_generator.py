import requests
import os
from dotenv import load_dotenv

load_dotenv()

def generate_voiceover(story, save_file=False, output_dir=None):
    headers = {
        "xi-api-key": os.getenv("ELEVENLABS_API_KEY"),
        "Content-Type": "application/json",
        "accept": "audio/mpeg"
    }
    data = {
        "text": story + "..Comment with your favorite fact...",
        "voice_settings": {"stability": 0.3, "similarity_boost": 0.3}
    }
    response = requests.post(
        "https://api.elevenlabs.io/v1/text-to-speech/AZnzlk1XvdvUeBnXmlld",
        headers=headers, json=data
    )

    if response.status_code == 200:
        if save_file and output_dir:
            os.makedirs(output_dir, exist_ok=True)
            voiceover_filename = os.path.join(output_dir, "voiceover.mp3")
            with open(voiceover_filename, "wb") as f:
                f.write(response.content)
            print(f"Voiceover saved to {voiceover_filename}")
        return response.content
    else:
        print(f"Error while generating voiceover with status code {response.status_code}")
        return None

def save_voiceover(voiceover_content, timestamp):
    output_dir = os.path.join("outputs", str(timestamp))  # ← fixed
    os.makedirs(output_dir, exist_ok=True)
    voiceover_filename = os.path.join(output_dir, f"voiceover_{timestamp}.mp3")
    with open(voiceover_filename, "wb") as f:
        f.write(voiceover_content)
    print(f"Voiceover saved to {voiceover_filename}")

