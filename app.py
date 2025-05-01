import streamlit as st
from datetime import datetime
from video_generator import generate_story, save_story_with_image_prompts, save_story
from keyword_identifier import extract_image_prompts
from image_generator import generate_images, save_images
from voiceover_generator import generate_voiceover, save_voiceover
from video_creator import create_video
from caption_generator import create_caption_images, add_captions_to_video

# Page config
st.set_page_config(page_title="🎨 AI Video Generator", page_icon="🎥", layout="wide")

# Styling
st.markdown("""
    <style>
    .main { background-color: #FFFFFF; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1, h2, h3 { color: #4A90E2; }
    .stButton>button {
        background-color: #50E3C2;
        color: white;
        border-radius: 8px;
        height: 3em;
        font-weight: 600;
    }
    .stButton>button:hover {
        background-color: #45D1B5;
        color: white;
    }
    .stDownloadButton>button {
        background-color: #4A90E2;
        color: white;
        border-radius: 8px;
        height: 3em;
        font-weight: 600;
    }
    .stDownloadButton>button:hover {
        background-color: #3F7CCF;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center;'>🎥 AI Video Generator</h1>", unsafe_allow_html=True)
st.write("Create a video from your AI-generated or custom script, images, and voiceover.")

# Sidebar settings
st.sidebar.markdown("## 🎛️ Settings")
video_prompt = st.sidebar.text_input("🎬 Enter your video topic or prompt:")
words_per_caption = st.sidebar.slider("📝 Words per caption image:", min_value=3, max_value=10, value=5)
add_captions_option = st.sidebar.checkbox("📑 Add captions to video")

# Session State to hold generated script and prompts
if 'story' not in st.session_state:
    st.session_state.story = ""
if 'prompts' not in st.session_state:
    st.session_state.prompts = []

# Step 1: Generate script
if st.sidebar.button("✍️ Generate Script"):
    if video_prompt.strip() == "":
        st.error("Please enter a video prompt.")
    else:
        story, final_prompt = generate_story(video_prompt)
        st.session_state.story = story
        st.session_state.prompts = extract_image_prompts(story)
        st.success("✅ Script and prompts generated successfully!")

# Display and allow editing of generated story and prompts
if st.session_state.story:
    st.markdown("## 📜 Generated Script")
    updated_story = st.text_area("You can edit the script before proceeding:", value=st.session_state.story, height=250)

    st.markdown("## 🎨 Generated Image Prompts")
    updated_prompts = st.text_area("You can edit the image prompts (comma-separated):", value=", ".join(st.session_state.prompts), height=150)

    # Confirm to proceed button
    if st.button("✅ Proceed to Video Generation"):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        # Convert updated prompts back to list
        prompt_list = [p.strip() for p in updated_prompts.split(",")]

        st.info("🖼️ Generating images...")
        images = generate_images(prompt_list)
        save_images(images)
        st.success("✅ Images generated.")

        st.info("🎙️ Generating voiceover...")
        voiceover = generate_voiceover(updated_story)
        save_voiceover(voiceover, timestamp)
        st.success("✅ Voiceover created.")

        st.info("🎥 Creating video...")
        create_video(images, voiceover, updated_story, timestamp)
        video_path = f"output_video_{timestamp}.mp4"
        st.success("✅ Video created!")

        final_video_path = video_path

        if add_captions_option:
            st.info("📝 Generating captions...")
            caption_images = create_caption_images(updated_story, words_per_caption)
            video_with_captions_path = f"video_with_captions_{timestamp}.mp4"
            add_captions_to_video(video_path, caption_images, video_with_captions_path)
            final_video_path = video_with_captions_path
            st.success("✅ Captions added.")

        # Show video
        st.video(final_video_path)

        # Download button
        with open(final_video_path, "rb") as video_file:
            st.download_button(
                label="📥 Download Your Video",
                data=video_file,
                file_name=f"AI_video_{timestamp}.mp4",
                mime="video/mp4"
            )

# Footer / Credits
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'>Made with 💙 by Your AI Video Generator</p>", unsafe_allow_html=True)
