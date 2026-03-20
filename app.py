import streamlit as st
import random
import time
import base64
from google import genai
from google.genai import types
import streamlit.components.v1 as components

# 1. API CONFIGURATION
API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

st.set_page_config(page_title="Aadya's Mission Control", page_icon="🐾")

# 🎤 ROBUST GEMINI VOICE FUNCTION
def speak_gemini(text):
    try:
        # Generate the high-quality speech
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
                audio_base64 = base64.b64encode(part.inline_data.data).decode('utf-8')
                # Custom HTML to force play on iPad
                components.html(f"""
                    <script>
                        var audio = new Audio("data:audio/wav;base64,{audio_base64}");
                        audio.play();
                    </script>
                """, height=0)
    except Exception as e:
        st.error("Mission Control voice is recharging, but I'm still here!")

# MISSION DATA
FAVORITES = ["Leopard", "Whale", "Airplane", "Yoga", "Swimming", "Skating", "Dancing", "Ballet", "Bus", "Train", "Maldives", "Snorkeling", "Peppa Pig", "Numberblocks", "Alphablocks", "Sheriff Labrador", "Disney"]

if 'current_topic' not in st.session_state:
    st.session_state.current_topic = random.choice(FAVORITES)
if 'mission_complete' not in st.session_state:
    st.session_state.mission_complete = False

# --- PAW PATROL STYLE LOGO HEADER ---
st.markdown("""
    <div style="text-align: center; padding: 15px; background-color: #e21b22; border-radius: 15px; border: 5px solid #f9d905; box-shadow: 10px 10px 0px #00529b;">
        <h1 style="color: white; font-family: 'Arial Black', sans-serif; text-transform: uppercase; letter-spacing: 2px; margin: 0; -webkit-text-stroke: 1px #00529b;">
            🐾 AADYA 🐾
        </h1>
        <h3 style="color: #f9d905; margin: 0; font-family: sans-serif;">MISSION CONTROL</h3>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# --- STEP 1: INTERACTIVE BALI MISSION ---
topic = st.session_state.current_topic

# PERSONALIZED LOGIC
if topic == "Swimming":
    intro = f"Aadya, your mission today is Swimming! There is a resort we are going to in Bali where you love to swim in the infinity pool facing the beach! How was your day? "
else:
    intro = f"Aadya, your mission today is {topic}! I know how much you love this. How was your day? "

mission_text = intro + "Write 1 or 2 sentences about this in your notebook. All the best, I will wait for the photo to be uploaded!"

st.markdown(f"""
<div style="padding:20px; border-radius:15px; border:2px solid #00529b; background-color:#ffffff; margin-bottom:10px;">
    <h3 style="color:#e21b22;">🐾 Mission: {topic}</h3>
    <p style="font-size:18px; color:#333;">{mission_text}</p>
</div>
""", unsafe_allow_html=True)

if st.button("📢 Listen to Mission Control"):
    with st.spinner("Preparing briefing..."):
        speak_gemini(mission_text)

# --- STEP 2: UPLOAD ---
st.write("---")
uploaded_file = st.file_uploader("📷 Upload writing photo", type=['png', 'jpg', 'jpeg'])

if uploaded_file and not st.session_state.mission_complete:
    if st.button("🚀 SCAN WRITING"):
        with st.spinner("🐾 Scanning..."):
            time.sleep(2) 
            congrats = f"Wow Aadya! I see your sentences about {topic}. You are a writing superstar!"
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
