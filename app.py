import streamlit as st
from google import genai
from google.genai import types
import random
import time
from PIL import Image
import streamlit.components.v1 as components

# 1. API CONFIGURATION
# We use st.secrets for security so your key isn't public on GitHub
API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

st.set_page_config(page_title="Aadya's Mission Control", page_icon="🚀")

# 2. 🎤 VOICE FUNCTION (Browser-based TTS)
def speak(text):
    clean_text = text.replace("'", "").replace('"', "")
    components.html(f"""
        <script>
            var msg = new SpeechSynthesisUtterance("{clean_text}");
            msg.lang = 'en-US';
            window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

# 3. MISSION DATA (Aadya's Favorites)
FAVORITES = [
    "Leopard", "Whale", "Airplane", "Yoga", "Swimming", "Skating", 
    "Dancing", "Ballet", "Bus", "Train", "Maldives", "Snorkeling", 
    "Peppa Pig", "Numberblocks", "Alphablocks", "Sheriff Labrador", "Disney"
]

# 4. SESSION STATE
if 'reward_type' not in st.session_state:
    st.session_state.reward_type = "Image"
if 'current_topic' not in st.session_state:
    st.session_state.current_topic = random.choice(FAVORITES)
    st.session_state.has_spoken_mission = False
if 'mission_complete' not in st.session_state:
    st.session_state.mission_complete = False

st.title("🚀 Aadya's Mission Control")

# --- STEP 1: MISSION BRIEFING ---
mission_text = f"Today's Mission is {st.session_state.current_topic}. Write 1 or 2 sentences about this in your notebook. All the best, I will wait for the photo to be uploaded."

st.markdown(f"""
<div style="padding:20px; border-radius:15px; border:2px solid #FF4B4B; background-color:#ffffff;">
    <h3 style="color:#FF4B4B;">🔬 Subject: {st.session_state.current_topic}</h3>
    <p style="font-size:18px;">{mission_text}</p>
</div>
""", unsafe_allow_html=True)

# Add a manual button to trigger the voice if it doesn't auto-play
if st.button("🔊 Listen to Mission Control"):
    speak(mission_text)

if not st.session_state.has_spoken_mission:
    speak(mission_text)
    st.session_state.has_spoken_mission = True

# --- STEP 2: UPLOAD WRITING ---
st.write("---")
uploaded_file = st.file_uploader("📷 Take a photo of your writing", type=['png', 'jpg', 'jpeg'])

if uploaded_file and not st.session_state.mission_complete:
    image_bytes = uploaded_file.getvalue()
    vision_prompt = f"This is writing from 6-year-old Aadya. Be an encouraging 'Mission Control'. Praise her for writing about {st.session_state.current_topic}. Mention one specific thing like a nice capital letter or good spacing. Keep it to 2 sentences."
    
    with st.spinner("Mission Control is scanning your work..."):
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[vision_prompt, types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg')]
            )
            congrats_text = response.text
            st.success(congrats_text)
            speak(congrats_text) # Read the congrats message aloud
            st.session_state.mission_complete = True
        except:
            st.error("Mission Control had a tiny hiccup. Please try again!")

# --- STEP 3: REVEAL SURPRISE ---
if st.session_state.mission_complete:
    if st.button("🎁 REVEAL CLASSIFIED SURPRISE"):
        st.balloons()
        topic = st.session_state.current_topic
        
        if st.session_state.reward_type == "Image":
            with st.spinner("🎨 Creating your surprise..."):
                prompt = f"A fun, high-quality 3D animation style image of {topic} doing something silly. Vibrant colors, Disney style."
                img_resp = client.models.generate_content(model='gemini-2.0-flash-exp', contents=prompt, config=types.GenerateContentConfig(response_modalities=['IMAGE']))
                for part in img_resp.parts:
                    if part.inline_data:
                        st.image(part.as_image(), caption=f"Special Surprise for Aadya!")
            st.session_state.reward_type = "Video"
        else:
            with st.spinner("🎬 Making your secret video..."):
                st.info(f"Generating a magical {topic} video...")
                # Veo Placeholder
                st.video("https://www.w3schools.com/html/mov_bbb.mp4")
            st.session_state.reward_type = "Image"
        
        if st.button("Start New Mission"):
            st.session_state.has_spoken_mission = False
            st.session_state.mission_complete = False
            st.session_state.current_topic = random.choice(FAVORITES)
            st.rerun()
