import google.generativeai as genai
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

# Configure Gemini API
genai.configure(api_key=os.getenv("OPENAI_API_KEY"))
model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

def generate_story(prompt):
    """Generates a story based on the provided prompt."""
    response = model.generate_content(prompt)
    story = response.text.strip().replace("**", "")
    return story, prompt  # No console input, just return generated story

def save_story_with_image_prompts(story, prompt, image_prompts):
    """Save the story with associated image prompts to a file."""
    file_path = f"story_{timestamp}.txt"
    with open(file_path, "w") as f:
        f.write(prompt + "\n" + story + "\n\nImage Prompts:\n")
        for idx, image_prompt in enumerate(image_prompts, start=1):
            f.write(f"{idx}: {image_prompt}\n")
    return file_path

def save_story(story):
    """Save only the story to a file."""
    file_path = f"story_{timestamp}.txt"
    with open(file_path, "w") as f:
        f.write(story)
    return file_path
