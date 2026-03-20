import streamlit as st
import random
import time
from google import genai
from google.genai import types
import streamlit.components.v1 as components

# 1. API CONFIGURATION
API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

st.set_page_config(page_title="Aadya's Mission Control", page_icon="🐾")

# 🎤 IMPROVED VOICE FUNCTION FOR IPAD
def speak(text):
    clean_text = text.replace("'", "").replace('"', "")
    components.html(f"""
        <button id="speakBtn" style="
            width: 100%; 
            padding: 15px; 
            background-color: #f9d905; 
            color: #00529b; 
            border: 4px solid #00529b; 
            border-radius: 12px; 
            font-size: 18px; 
            font-weight: bold; 
            cursor: pointer;
            box-shadow: 5px 5px 0px #e21b22;
        ">
            🔊 HEAR MISSION CONTROL
        </button>

        <script>
            document.getElementById('speakBtn').onclick = function() {{
                window.speechSynthesis.cancel();
                var msg = new SpeechSynthesisUtterance("{clean_text}");
                msg.lang = 'en-US';
                msg.rate = 0.8; 
                window.speechSynthesis.speak(msg);
            }};
        </script>
    """, height=80)

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
if topic == "Swimming":
    intro = f"Aadya, your mission today is Swimming! There is a resort we are going to in Bali where you love to swim in the infinity pool facing the beach! How was your day? "
else:
    intro = f"Aadya, your mission today is {topic}! I know how much you love this. How was your day? "

mission_text = intro + "Write 1 or 2 sentences in your notebook. All the best, I will wait for your photo!"

st.markdown(f"""
<div style="padding:20px; border-radius:15px; border:2px solid #00529b; background-color:#ffffff; margin-bottom:10px;">
    <h3 style="color:#e21b22;">🐾 Mission: {topic}</h3>
    <p style="font-size:18px; color:#333;">{mission_text}</p>
</div>
""", unsafe_allow_html=True)

# THE VOICE BUTTON
speak(mission_text)

# --- STEP 2: UPLOAD ---
st.write("---")
uploaded_file = st.file_uploader("📷 Upload writing photo", type=['png', 'jpg', 'jpeg'])

if uploaded_file and not st.session_state.mission_complete:
    # INSTANT WIN - No complex AI scan that causes hiccups
    if st.button("🚀 SCAN WRITING"):
        with st.spinner("🐾 Mission Control is scanning..."):
            time.sleep(2) 
            congrats = f"Wow Aadya! I see your sentences about {topic}. You are a writing superstar! Click below for your surprise."
            st.success(congrats)
            speak(congrats)
            st.session_state.mission_complete = True
            st.rerun()

# --- STEP 3: REVEAL ---
if st.session_state.mission_complete:
    if st.button("🌟 CLICK FOR YOUR SURPRISE"):
        st.balloons()
        topic = st.session_state.current_topic
        
        with st.spinner("🎨 Creating your safe surprise..."):
            try:
                # 🎨 THE FIX: Safety Prompt for Cartoon Images
                safe_cartoon_prompt = f"A fun, high-quality 3D Disney Pixar style image of {topic} having a party. Vibrant colors, friendly, safe for children, no scary elements."
                response = client.models.generate_content(
                    model='gemini-2.0-flash-exp', 
                    contents=safe_cartoon_prompt, 
                    config=types.GenerateContentConfig(response_modalities=['IMAGE'])
                )
                for part in response.parts:
                    if part.inline_data:
                        st.image(part.as_image())
            except:
                # Backup safe cartoon image
                st.warning("Just getting your safe surprise ready!")
                st.image(f"https://loremflickr.com/800/600/{topic},pixar", caption=f"Great job!")

    if st.button("🐾 Start New Mission"):
        st.session_state.mission_complete = False
        st.session_state.current_topic = random.choice(FAVORITES)
        st.rerun()
