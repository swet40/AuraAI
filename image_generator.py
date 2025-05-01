from io import BytesIO
from PIL import Image
import requests
import base64
import os
from datetime import datetime
import time
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Create output directory with timestamp
def get_output_dir():
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_dir = os.path.join("outputs", timestamp)
    os.makedirs(output_dir, exist_ok=True)
    return output_dir, timestamp

# Load API Key
stability_api_key = os.getenv("STABILITY_API_KEY")

if not stability_api_key:
    raise ValueError("STABILITY_API_KEY environment variable not set.")


# Main image generation function
def generate_images(image_prompts, output_dir, timestamp):
    images = []

    for idx, prompt in enumerate(image_prompts):
        print(f"Generating image for prompt: {prompt}")

        url = "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image"
        headers = {
            "Authorization": f"Bearer {stability_api_key}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = {
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 7,
            "clip_guidance_preset": "FAST_BLUE",
            "height": 768,
            "width": 1280,
            "samples": 1,
            "steps": 30
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            result = response.json()
            image_base64 = result['artifacts'][0]['base64']

            image_data = base64.b64decode(image_base64)
            image = Image.open(BytesIO(image_data))

            # Save image to file
            image_path = os.path.join(output_dir, f"image_{timestamp}_{idx}.png")
            image.save(image_path)
            images.append(image_path)

            print(f"Image {idx+1} saved at {image_path}")

        else:
            print(f"Failed to generate image for prompt '{prompt}': {response.status_code} - {response.text}")

        time.sleep(1)

    return images

# Story text save
def save_story_text(story_text):
    output_dir, timestamp = get_output_dir()
    story_filename = os.path.join(output_dir, f"story_{timestamp}.txt")
    with open(story_filename, "w") as f:
        f.write(story_text)
    print(f"Story text saved to {story_filename}")
    return story_filename

# Image saving log helper (optional)
def save_images(images):
    print(f"Images saved: {images}")

# Direct image download helper
def download_image(url, filename):
    response = requests.get(url)
    with open(filename, "wb") as f:
        f.write(response.content)
