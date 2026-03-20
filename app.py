import streamlit as st
import random
import time
import base64
from google import genai
from google.genai import types

# 1. API CONFIGURATION
API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

st.set_page_config(page_title="Aadya's Mission Control", page_icon="🐾")

# 🎤 THE RELIABLE AUDIO ENGINE
def speak_gemini(text):
    try:
        # Generate high-quality Puck voice
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Puck")
                    )
                )
            ),
            contents=text,
        )
        
        for part in response.parts:
            if part.inline_data:
                # This creates a standard iPad-compatible play bar
                st.audio(part.inline_data.data, format="audio/wav")
                st.caption("Tap the play button above to hear me!")
    except Exception as e:
        st.error("Mission Control is a bit quiet. Let's keep going anyway!")

# MISSION DATA
FAVORITES = ["Leopard", "Whale", "Airplane", "Yoga", "Swimming", "Skating", "Dancing", "Ballet", "Bus", "Train", "Maldives", "Snorkeling", "Peppa Pig", "Numberblocks", "Alphablocks", "Sheriff Labrador", "Disney"]

if 'current_topic' not in st.session_state:
    st.session_state.current_topic = random.choice(FAVORITES)
if 'mission_complete' not in st.session_state:
    st.session_state.mission_complete = False

# --- PAW PATROL STYLE LOGO ---
st.markdown("""
    <div style="text-align: center; padding: 15px; background-color: #e21b22; border-radius: 15px; border: 5px solid #f9d905; box-shadow: 10px 10px 0px #00529b;">
        <h1 style="color: white; font-family: 'Arial Black', sans-serif; text-transform: uppercase; letter-spacing: 2px; margin: 0; -webkit-text-stroke: 1px #00529b;">
            🐾 AADYA 🐾
        </h1>
        <h3 style="color: #f9d905; margin: 0; font-family: sans-serif;">MISSION CONTROL</h3>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# --- STEP 1: PERSONALIZED MISSION ---
topic = st.session_state.current_topic

if topic == "Swimming":
    personal_story = "There is a resort which we are going to in Bali where you love to swim around the beach facing infinity pool! How was your day? "
else:
    personal_story = f"I know how much you love {topic}! How was your day? "

mission_text = f"Aadya, your mission is {topic}. {personal_story} Write 1 or 2 sentences about this in your notebook. All the best, I will wait for the photo!"

st.markdown(f"""
<div style="padding:20px; border-radius:15px; border:2px solid #00529b; background-color:#ffffff; margin-bottom:10px;">
    <h3 style="color:#e21b22;">🐾 Mission: {topic}</h3>
    <p style="font-size:18px; color:#333;">{mission_text}</p>
</div>
""", unsafe_allow_html=True)

# Generate the Audio Player
if st.button("📢 Get Voice Briefing"):
    with st.spinner("Preparing briefing..."):
        speak_gemini(mission_text)

# --- STEP 2: UPLOAD ---
st.write("---")
uploaded_file = st.file_uploader("📷 Upload your writing", type=['png', 'jpg', 'jpeg'])

if uploaded_file and not st.session_state.mission_complete:
    if st.button("🚀 SCAN WRITING"):
        with st.spinner("🐾 Scanning..."):
            time.sleep(2) 
            congrats = f"Wow Aadya! You are a writing superstar! Click below for your surprise."
            st.success(congrats)
            speak_gemini(congrats)
            st.session_state.mission_complete = True
            st.rerun()

# --- STEP 3: REVEAL ---
if st.session_state.mission_complete:
    if st.button("🌟 CLICK FOR YOUR SURPRISE"):
        st.balloons()
        st.image(f"https://loremflickr.com/800/600/{topic},disney", caption=f"Great job Aadya!")

    if st.button("🐾 Start New Mission"):
        st.session_state.mission_complete = False
        st.session_state.current_topic = random.choice(FAVORITES)
        st.rerun()
