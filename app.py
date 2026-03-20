import streamlit as st
import random
import time
from google import genai
from google.genai import types
import streamlit.components.v1 as components

# 1. API CONFIGURATION
API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

# Force a friendly theme
st.set_page_config(page_title="Aadya's Mission Control", page_icon="🐾")

# 🕯️ STAY AWAKE SCRIPT
components.html("<script>navigator.wakeLock.request('screen');</script>", height=0)

# 🎤 VOICE ENGINE
def speak(text):
    clean_text = text.replace("'", "").replace('"', "")
    components.html(f"""
        <button id="speakBtn" style="width:100%; padding:15px; background-color:#f9d905; color:#00529b; border:4px solid #00529b; border-radius:12px; font-weight:bold; cursor:pointer; font-size:18px;">
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
FAVORITES = {
    "Leopard": {
        "hook": "A fast leopard found a mysterious silver key in the jungle. He needs to know what the key opens!",
        "video_prompt": "A friendly 3D Pixar style leopard in a jungle using a silver key to open a treasure chest filled with gold, cinematic lighting, 5 seconds."
    },
    "Whale": {
        "hook": "A giant blue whale discovered a hidden underwater cave filled with glowing bubbles.",
        "video_prompt": "A happy 3D Pixar whale swimming through a cave of glowing rainbow bubbles, underwater magic, 5 seconds."
    },
    "Swimming": {
        "hook": "You are at the Bali resort in the infinity pool! Suddenly, a friendly dolphin waves at you.",
        "video_prompt": "A cute 3D dolphin jumping out of a beautiful infinity pool at a tropical Bali resort, sunset, Pixar style, 5 seconds."
    },
    "Numberblocks": {
        "hook": "Number Ten is building a giant tower to reach the sun, but he needs one more block!",
        "video_prompt": "A 3D Numberblock building a glowing tower that reaches up to a smiling sun, bright colors, Pixar style, 5 seconds."
    }
}

if 'current_topic' not in st.session_state:
    st.session_state.current_topic = random.choice(list(FAVORITES.keys()))
if 'mission_complete' not in st.session_state:
    st.session_state.mission_complete = False

# --- HEADER (Fixed for Dark Mode) ---
st.markdown("""
    <style>
        .mission-box {
            padding: 20px; 
            border-radius: 15px; 
            border: 3px solid #f9d905; 
            background-color: rgba(255, 255, 255, 0.1); 
            margin-top: 20px;
        }
        .step-text {
            color: white !important;
            font-size: 20px;
            margin-bottom: 10px;
        }
    </style>
    <div style="text-align: center; padding: 15px; background-color: #e21b22; border-radius: 15px; border: 5px solid #f9d905;">
        <h1 style="color: white; margin: 0;">🐾 AADYA MISSION CONTROL 🐾</h1>
    </div>
    """, unsafe_allow_html=True)

# --- MISSION STEPS ---
topic = st.session_state.current_topic
story = FAVORITES[topic]

st.markdown(f"""
<div class="mission-box">
    <h2 style="color:#f9d905; margin-top:0;">📋 Mission Steps:</h2>
    <p class="step-text"><b>1. Tell Daddy:</b> How was your day? 👋</p>
    <p class="step-text"><b>2. Imagine:</b> {story['hook']} ✨</p>
    <p class="step-text"><b>3. Write:</b> Finish the story in your notebook! ✍️</p>
</div>
""", unsafe_allow_html=True)

speak(f"Aadya, Mission Control here! Tell Daddy about your day, then imagine this: {story['hook']}. Write the end in your notebook!")

# --- UPLOAD ---
st.write("---")
uploaded_file = st.file_uploader("📷 Upload writing photo", type=['png', 'jpg', 'jpeg'])

if uploaded_file and not st.session_state.mission_complete:
    if st.button("🚀 SUBMIT MISSION"):
        with st.spinner("🐾 Scanning..."):
            time.sleep(2) 
            st.balloons()
            st.session_state.mission_complete = True
            st.rerun()

# --- REVEAL MOVIE REWARD ---
if st.session_state.mission_complete:
    st.markdown("<h3 style='color:#f9d905;'>🎉 MISSION COMPLETE!</h3>", unsafe_allow_html=True)
    if st.button("🎬 WATCH YOUR MOVIE SURPRISE"):
        with st.spinner("🎥 Filming your story ending..."):
            try:
                # Generate Video using Veo
                # In this specific implementation, we use the generate_content for video
                video_res = client.models.generate_content(
                    model='veo', 
                    contents=story['video_prompt']
                )
                # Render the generated video
                for part in video_res.parts:
                    if part.inline_data:
                        st.video(part.inline_data.data)
            except:
                st.info("The movie is being developed! Tap again in 5 seconds.")

    if st.button("🐾 Next Mission"):
        st.session_state.mission_complete = False
        st.session_state.current_topic = random.choice(list(FAVORITES.keys()))
        st.rerun()
