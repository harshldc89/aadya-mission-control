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

# 🕯️ STAY AWAKE SCRIPT
components.html("<script>navigator.wakeLock.request('screen');</script>", height=0)

# 🎤 VOICE ENGINE
def speak(text):
    clean_text = text.replace("'", "").replace('"', "")
    components.html(f"""
        <button id="speakBtn" style="width:100%; padding:15px; background-color:#C0C0C0; color:#000000; border:4px solid #FFD700; border-radius:12px; font-weight:bold; cursor:pointer; font-size:18px; box-shadow: 2px 2px 5px rgba(0,0,0,0.3);">
            📢 HEAR MISSION BRIEFING
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

# REAL-LIFE CREATIVE MISSIONS
FAVORITES = {
    "Leopard": {
        "hook": "You are a wildlife photographer in the jungle. You just spotted a leopard hiding in the tall grass, watching a colorful bird. What happens next?",
        "video_prompt": "A realistic 3D Pixar style leopard crouching in tall jungle grass, blinking its eyes and twitching its tail, looking at a tropical bird, 5 seconds."
    },
    "Airplane": {
        "hook": "You are the pilot of a big airplane flying over a glowing city at night. You see millions of tiny lights below. Where are you landing your passengers?",
        "video_prompt": "A 3D animation of a pilot's view from a cockpit flying over a glowing city at night with city lights and stars, Pixar style, 5 seconds."
    },
    "Swimming": {
        "hook": "You are at the resort in Bali in the infinity pool. You decide to see how long you can float, and you notice something shiny at the bottom. What is it?",
        "video_prompt": "A realistic 3D scene of a beautiful infinity pool in Bali, water rippling, a small golden coin glowing at the bottom, Pixar style, 5 seconds."
    },
    "Chef": {
        "hook": "You are a head chef making a giant pizza for a street party. You have the dough and sauce, but you forgot one very special topping. What do you add?",
        "video_prompt": "A 3D cartoon chef tossing a giant pizza dough in the air in a sunny Italian kitchen, flour puffing, Pixar style, 5 seconds."
    }
}

# --- INITIALIZE ---
if 'current_topic' not in st.session_state:
    st.session_state.current_topic = random.choice(list(FAVORITES.keys()))
    st.session_state.mission_complete = False
    st.session_state.video_ready = None

# PRE-LOAD VIDEO
if st.session_state.video_ready is None:
    try:
        topic = st.session_state.current_topic
        video_res = client.models.generate_content(model='veo', contents=FAVORITES[topic]['video_prompt'])
        for part in video_res.parts:
            if part.inline_data:
                st.session_state.video_ready = part.inline_data.data
    except:
        pass

# --- 🎨 THE SILVER & GOLD THEME ---
st.markdown("""
    <style>
        /* Main Background */
        .stApp {
            background-color: #001f3f;
        }
        /* Top Logo Box - Silver Border, Golden Inside */
        .header-box {
            text-align: center; 
            padding: 20px; 
            background-color: #FFD700; /* Gold */
            border-radius: 15px; 
            border: 6px solid #C0C0C0; /* Silver */
            box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
        }
        /* Mission Card - Silver Border, Golden Inside */
        .mission-card {
            padding: 25px; 
            border-radius: 15px; 
            border: 6px solid #C0C0C0; /* Silver border */
            background-color: #FFD700; /* Gold background */
            margin-top: 25px;
            box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
        }
        .mission-header { color: #000000 !important; font-size: 26px; font-weight: bold; margin-bottom: 15px; text-decoration: underline; }
        .mission-text { color: #000000 !important; font-size: 22px; line-height: 1.4; font-weight: 500; }
        .step-num { color: #800000 !important; font-weight: bold; }
        
        /* File Uploader styling override */
        .stFileUploader {
            background-color: #FFD700;
            border: 3px solid #C0C0C0;
            border-radius: 10px;
            padding: 10px;
        }
    </style>
    
    <div class="header-box">
        <h1 style="color: #000000; margin: 0; font-family: sans-serif; letter-spacing: 2px;">🐾 MISSION CONTROL 🐾</h1>
    </div>
    """, unsafe_allow_html=True)

# --- THE MISSION CARD ---
topic = st.session_state.current_topic
story = FAVORITES[topic]

st.markdown(f"""
<div class="mission-card">
    <div class="mission-header">🌟 YOUR GOLDEN MISSION: {topic}</div>
    <p class="mission-text"><span class="step-num">Step 1. Imagine:</span> {story['hook']}</p>
    <br>
    <p class="mission-text"><span class="step-num">Step 2. Write:</span> Finish the story in your notebook with 2 sentences!</p>
</div>
""", unsafe_allow_html=True)

speak(f"Aadya, Mission Control here! Your golden mission is {topic}. Imagine this: {story['hook']}. Now, write the ending in your notebook. Good luck!")

# --- UPLOAD SECTION ---
st.write("")
st.markdown("<h4 style='color: #C0C0C0; text-align: center;'>📷 Take a photo of your notebook:</h4>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'])

if uploaded_file and not st.session_state.mission_complete:
    if st.button("🚀 UPLOAD TO MISSION CONTROL"):
        st.balloons()
        st.session_state.mission_complete = True
        st.rerun()

# --- REVEAL MOVIE REWARD ---
if st.session_state.mission_complete:
    st.markdown("<h3 style='color:#FFD700; text-align:center;'>🏆 MISSION ACCOMPLISHED! 🏆</h3>", unsafe_allow_html=True)
    
    # Reveal Button also follows Silver/Gold theme
    if st.button("🎬 WATCH YOUR GOLDEN MOVIE"):
        if st.session_state.video_ready:
            st.video(st.session_state.video_ready)
        else:
            with st.spinner("🎥 Developing your film..."):
                time.sleep(5)
                st.info("Tap again to play!")

    if st.button("🐾 Get New Mission"):
        st.session_state.current_topic = random.choice(list(FAVORITES.keys()))
        st.session_state.mission_complete = False
        st.session_state.video_ready = None
        st.rerun()
