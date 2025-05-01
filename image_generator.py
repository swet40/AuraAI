import os
import requests
import base64
from datetime import datetime
import time

# Create a timestamp for this run
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

# Set output folder path
output_dir = os.path.join("outputs", timestamp)
os.makedirs(output_dir, exist_ok=True)  # Make sure the folder exists

# Fetch Stability API Key from environment variables
stability_api_key = os.getenv("STABILITY_API_KEY")

if not stability_api_key:
    raise ValueError("STABILITY_API_KEY environment variable not set.")

def generate_images(image_prompts):
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
            "height": 512,
            "width": 512,
            "samples": 1,
            "steps": 30
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            result = response.json()
            image_base64 = result['artifacts'][0]['base64']
            image_filename = os.path.join(output_dir, f"image_{timestamp}_{idx}.png")

            # Save image to file
            with open(image_filename, "wb") as img_file:
                img_file.write(base64.b64decode(image_base64))

            images.append(image_filename)
            print(f"Image saved to {image_filename}")

        else:
            print(f"Failed to generate image for prompt '{prompt}': {response.status_code} - {response.text}")

        time.sleep(1)  # Avoid hitting rate limits

    return images


def save_story_text(story_text):
    story_filename = os.path.join(output_dir, f"story_{timestamp}.txt")
    with open(story_filename, "w") as f:
        f.write(story_text)
    print(f"Story text saved to {story_filename}")
    return story_filename


def save_images(images):
    # Images are already saved during generation
    print(f"Images saved: {images}")


def download_image(url, filename):
    response = requests.get(url)
    with open(filename, "wb") as f:
        f.write(response.content)
