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

# 🎤 VOICE ENGINE (iPad Stable)
def speak(text):
    clean_text = text.replace("'", "").replace('"', "")
    components.html(f"""
        <button id="speakBtn" style="width:100%; padding:15px; background-color:#f9d905; color:#00529b; border:4px solid #00529b; border-radius:12px; font-weight:bold; cursor:pointer; font-size:18px;">
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
        "hook": "You are the pilot of a big airplane. You are flying over a city at night and see millions of tiny lights below. Where are you landing your passengers?",
        "video_prompt": "A 3D animation of a pilot's view from a cockpit flying over a glowing city at night with city lights and stars, Pixar style, 5 seconds."
    },
    "Swimming": {
        "hook": "You are at the Bali resort in the infinity pool. You decide to see how long you can float, and you notice something shiny at the bottom of the pool. What is it?",
        "video_prompt": "A realistic 3D scene of a beautiful infinity pool in Bali, water rippling, a small golden coin glowing at the bottom, Pixar style, 5 seconds."
    },
    "Architecture": {
        "hook": "You are an architect building a house made entirely of glass and wood. It has a secret room that only you know about. What is in the secret room?",
        "video_prompt": "A beautiful 3D modern glass house in a forest, the lights inside turn on, showing a cozy secret library, Pixar style, 5 seconds."
    }
}

# --- INITIALIZE SESSION ---
if 'current_topic' not in st.session_state:
    st.session_state.current_topic = random.choice(list(FAVORITES.keys()))
if 'mission_complete' not in st.session_state:
    st.session_state.mission_complete = False

# --- DARK MODE STYLING ---
st.markdown("""
    <style>
        .mission-box {
            padding: 25px; border-radius: 15px; border: 3px solid #f9d905; 
            background-color: rgba(255, 255, 255, 0.15); margin-top: 20px;
        }
        .step-text { color: white !important; font-size: 22px; margin-bottom: 15px; line-height: 1.4; }
    </style>
    <div style="text-align: center; padding: 15px; background-color: #e21b22; border-radius: 15px; border: 5px solid #f9d905;">
        <h1 style="color: white; margin: 0;">🐾 MISSION CONTROL 🐾</h1>
    </div>
    """, unsafe_allow_html=True)

# --- THE MISSION ---
topic = st.session_state.current_topic
story = FAVORITES[topic]

st.markdown(f"""
<div class="mission-box">
    <h2 style="color:#f9d905; margin-top:0;">🌟 Your Mission:</h2>
    <p class="step-text"><b>Step 1. Imagine:</b> {story['hook']}</p>
    <p class="step-text"><b>Step 2. Write:</b> Finish the story in your notebook with 2 sentences!</p>
</div>
""", unsafe_allow_html=True)

speak(f"Aadya, Mission Control here! Imagine this: {story['hook']}. Now, write the ending in your notebook. I can't wait to see!")

# --- UPLOAD ---
st.write("---")
uploaded_file = st.file_uploader("📷 Mission finished? Take a photo!", type=['png', 'jpg', 'jpeg'])

if uploaded_file and not st.session_state.mission_complete:
    if st.button("🚀 SUBMIT TO MISSION CONTROL"):
        st.balloons()
        st.session_state.mission_complete = True
        st.rerun()

# --- REVEAL MOVIE ---
if st.session_state.mission_complete:
    st.markdown("<h3 style='color:#f9d905; text-align:center;'>🎉 MISSION ACCOMPLISHED!</h3>", unsafe_allow_html=True)
    
    if st.button("🎬 WATCH YOUR STORY MOVIE"):
        with st.spinner("🎥 Mission Control is filming your story ending..."):
            try:
                # Generate video ONLY when button is clicked to avoid startup errors
                video_res = client.models.generate_content(
                    model='veo', 
                    contents=story['video_prompt']
                )
                for part in video_res.parts:
                    if part.inline_data:
                        st.video(part.inline_data.data)
            except:
                st.info("The movie camera is warming up. Tap one more time!")

    if st.button("🐾 Next Mission"):
        st.session_state.current_topic = random.choice(list(FAVORITES.keys()))
        st.session_state.mission_complete = False
        st.rerun()
