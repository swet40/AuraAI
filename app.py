import streamlit as st
from datetime import datetime
import os
from video_generator import generate_story, save_story_with_image_prompts, save_story
from keyword_identifier import extract_image_prompts
from image_generator import generate_images, save_images
from voiceover_generator import generate_voiceover, save_voiceover
from video_creator import create_video
from caption_generator import create_caption_images, add_captions_to_video

# Streamlit config
st.set_page_config(page_title="AuraAI Video Creator 🎥", page_icon="🎨", layout="wide")

# Custom CSS for pastel theme
st.markdown("""
    <style>
    .main { background-color: #f0f8ff; }
    h1, h2, h3 { color: #5a6d8a; }
    .stButton>button {
        background-color: #8ecae6;
        color: white;
        border-radius: 6px;
        height: 3em;
        font-weight: 600;
    }
    .stButton>button:hover { background-color: #219ebc; }
    .stTextInput>div>div>input { background-color: #ffffff; color: #333; }
    </style>
""", unsafe_allow_html=True)

# App heading
st.markdown("<h1 style='text-align: center;'>🎨 AuraAI Video Creator</h1>", unsafe_allow_html=True)
st.markdown("Create AI-generated videos from your custom topic with editable script and prompts.")

# Sidebar controls
st.sidebar.header("📋 Settings")
user_prompt = st.sidebar.text_input("🎬 Enter your video topic:")
add_captions = st.sidebar.checkbox("📑 Add captions to video", value=True)
words_per_caption = st.sidebar.slider("✏️ Words per caption image:", 3, 10, 5)

# Initialize session state variables
if "story" not in st.session_state:
    st.session_state.story = ""
if "image_prompts" not in st.session_state:
    st.session_state.image_prompts = []

# Generate story button
if st.sidebar.button("📝 Generate Story & Prompts"):
    if user_prompt.strip() == "":
        st.warning("Please enter a topic prompt.")
    else:
        with st.spinner("Generating story..."):
            story, final_prompt = generate_story(user_prompt)
            image_prompts = extract_image_prompts(story)

            st.session_state.story = story
            st.session_state.image_prompts = image_prompts

        st.success("Story and prompts generated!")

# Show generated story and prompts
if st.session_state.story:
    st.subheader("📜 Generated Story")
    st.session_state.story = st.text_area("Edit story if you like:", value=st.session_state.story, height=200)

    st.subheader("🖼️ Generated Image Prompts")

    prompts_to_delete = []

    for idx, prompt in enumerate(st.session_state.image_prompts):
        cols = st.columns([5, 1])
        with cols[0]:
            st.session_state.image_prompts[idx] = st.text_input(f"Prompt {idx+1}", value=prompt, key=f"prompt_{idx}")
        with cols[1]:
            if st.button("🗑️", key=f"delete_prompt_{idx}"):
                prompts_to_delete.append(idx)

    # Delete selected prompts
    for idx in sorted(prompts_to_delete, reverse=True):
        del st.session_state.image_prompts[idx]

    # Add new prompt option
    new_prompt = st.text_input("➕ Add a new image prompt:")
    if st.button("Add Prompt"):
        if new_prompt.strip():
            st.session_state.image_prompts.append(new_prompt)

    # Proceed to video generation
    proceed = st.radio("Do you want to proceed with these?", ("Yes", "No"), horizontal=True)

    if proceed == "Yes":
        if st.button("🎥 Generate Video"):
            with st.spinner("Generating video..."):
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                output_dir = f"outputs/{timestamp}"
                os.makedirs(output_dir, exist_ok=True)

                save_story(st.session_state.story)
                save_story_with_image_prompts(st.session_state.story, user_prompt, st.session_state.image_prompts)
                images = generate_images(st.session_state.image_prompts)
                save_images(images)
                voiceover = generate_voiceover(st.session_state.story)
                save_voiceover(voiceover, timestamp)
                create_video(images, voiceover, st.session_state.story, timestamp)

                video_path = f"{output_dir}/output_video_{timestamp}.mp4"

                if add_captions:
                    caption_images = create_caption_images(st.session_state.story, words_per_caption)
                    video_with_captions_path = f"{output_dir}/video_with_captions_{timestamp}.mp4"
                    add_captions_to_video(video_path, caption_images, video_with_captions_path)
                    final_video_path = video_with_captions_path
                else:
                    final_video_path = video_path

            st.success("✅ Video ready!")

            video_html = f"""
                <video width="600" height="340" controls>
                    <source src="{final_video_path}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            """
            st.markdown(video_html, unsafe_allow_html=True)

            with open(final_video_path, "rb") as f:
                st.download_button("📥 Download Video", data=f, file_name=f"AI_video_{timestamp}.mp4", mime="video/mp4")

# Footer credits
st.markdown("---")
st.markdown("<p style='text-align: center; color: #6c757d;'>Made with 💙 by AuraAI</p>", unsafe_allow_html=True)
