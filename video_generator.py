import google.generativeai as genai
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

genai.configure(api_key=os.getenv("OPENAI_API_KEY"))


model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

def generate_story(prompt):
    while True:
        response = model.generate_content(prompt)
        story = response.text.strip()

        print("Generated Video:")
        print(story)
        
        # Ask the user whether they want to proceed, generate another story, or write their own story
        user_input = input("\nDo you want to proceed with this? (y/n/custom): ")
        if user_input.lower() == "y":
            return story, prompt  # Return both the story and the prompt used
        elif user_input.lower() == "n":
            prompt = input("\nEnter a new prompt: ")
        elif user_input.lower() == "custom":
            custom_story = input("Give your custom input: ")
            return custom_story, prompt  # Return the custom story and the original prompt
        else:
            print("Invalid input. Please enter 'y' to proceed with this , 'n' to generate another story, or 'custom' to write your own story.")

def save_story_with_image_prompts(story, prompt, image_prompts):
    with open(f"story_{timestamp}.txt", "w") as f:
        f.write(prompt + "\n" + story + "\n\nImage Prompts:\n")
        for idx, image_prompt in enumerate(image_prompts, start=1):
            f.write(f"{idx}: {image_prompt}\n")

def save_story(story):
    file_path = f"story_{timestamp}.txt"
    with open(file_path, "w") as f:
        f.write(story)
    return file_path  # Return the file path where the story is saved

