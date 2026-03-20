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
components.html("""
    <script>
        let wakeLock = null;
        async function requestWakeLock() {
            try {
                wakeLock = await navigator.wakeLock.request('screen');
            } catch (err) {}
        }
        requestWakeLock();
    </script>
""", height=0)

# 🎤 VOICE ENGINE
def speak(text):
    clean_text = text.replace("'", "").replace('"', "")
    components.html(f"""
        <button id="speakBtn" style="width:100%; padding:15px; background-color:#f9d905; color:#00529b; border:4px solid #00529b; border-radius:12px; font-weight:bold; cursor:pointer;">
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

# MISSION DATA & VIDEO REWARD PROMPTS
# The 'reward' field is the instruction for the 5-second video
FAVORITES = {
    "Leopard": {
        "hook": "A fast leopard found a mysterious silver key in the jungle. He needs to know what the key opens!",
        "reward": "A friendly cartoon leopard using a silver key to open a glowing wooden treasure chest in a lush green jungle, 3D Pixar style."
    },
    "Whale": {
        "hook": "A giant blue whale discovered a hidden underwater cave filled with glowing bubbles.",
        "reward": "A happy blue whale swimming into a cave filled with thousands of glowing rainbow bubbles, underwater cinematic Pixar style."
    },
    "Airplane": {
        "hook": "Your airplane is flying through a cloud made of pink cotton candy! Where are you landing?",
        "reward": "A colorful toy airplane landing softly on a giant mountain of pink cotton candy, sparkles everywhere, Pixar style."
    },
    "Yoga": {
        "hook": "You are a yoga master in a magical forest where the trees move with you.",
        "reward": "A 6-year-old girl doing a tree pose in a magical forest while the trees around her mimic her pose and wave their branches, Pixar style."
    },
    "Swimming": {
        "hook": "You are at the Bali resort in the infinity pool! Suddenly, a friendly dolphin waves at you.",
        "reward": "A friendly dolphin jumping happily out of the water next to an infinity pool at a Bali resort, sunset background, Pixar style."
    },
    "Skating": {
        "hook": "You are skating on a slippery rainbow instead of ice! Where does it lead?",
        "reward": "A girl skating fast across a bright glowing rainbow bridge that leads to a castle made of candy, 3D animation."
    },
    "Bus": {
        "hook": "This school bus can fly! You just pushed a secret green button to go to space.",
        "reward": "A bright yellow school bus with rocket boosters flying past the moon and stars in deep space, cartoon style."
    }
}

if 'current_topic' not in st.session_state:
    st.session_state.current_topic = random.choice(list(FAVORITES.keys()))
if 'mission_complete' not in st.session_state:
    st.session_state.mission_complete = False

# --- HEADER ---
st.markdown("""
    <div style="text-align: center; padding: 15px; background-color: #e21b22; border-radius: 15px; border: 5px solid #f9d905;">
        <h1 style="color: white; margin: 0;">🐾 AADYA MISSION CONTROL 🐾</h1>
    </div>
    """, unsafe_allow_html=True)

# --- INSTRUCTIONS ---
topic = st.session_state.current_topic
story_data = FAVORITES[topic]

st.markdown(f"""
<div style="padding:20px; border-radius:15px; border:3px solid #00529b; background-color:#ffffff; margin-top:20px;">
    <h2 style="color:#e21b22; margin-top:0;">📋 Mission Steps:</h2>
    <p style="font-size:20px;"><b>1. Tell Daddy:</b> How was your day? 👋</p>
    <p style="font-size:20px;"><b>2. Imagine:</b> {story_data['hook']} ✨</p>
    <p style="font-size:20px;"><b>3. Write:</b> Finish the story in your notebook! ✍️</p>
</div>
""", unsafe_allow_html=True)

speak(f"Aadya, Mission Control here! Tell Daddy about your day, then imagine this: {story_data['hook']}. Write the end in your notebook!")

# --- UPLOAD ---
st.write("---")
uploaded_file = st.file_uploader("📷 Upload writing photo", type=['png', 'jpg', 'jpeg'])

if uploaded_file and not st.session_state.mission_complete:
    if st.button("🚀 SUBMIT MISSION"):
        with st.spinner("🐾 Scanning..."):
            time.sleep(2) 
            st.success("Excellent work, Aadya! You are a creative superstar!")
            speak("Excellent work, Aadya! You have completed the mission! Click below for your movie surprise.")
            st.session_state.mission_complete = True
            st.rerun()

# --- REVEAL VIDEO REWARD ---
if st.session_state.mission_complete:
    if st.button("🎬 WATCH YOUR MOVIE SURPRISE"):
        st.balloons()
        with st.spinner("🎥 Mission Control is filming your story..."):
            try:
                # 🚀 CALLING VEO VIDEO MODEL
                video_prompt = story_data['reward']
                # This logic assumes the backend supports the video modality in the flash model or specific video tool
                # For this Streamlit setup, we'll call the generation
                st.info("Your 5-second movie is arriving!")
                # Note: In a live app, this would render the video component
                st.video("https://www.w3schools.com/html/mov_bbb.mp4") # Placeholder: Replace with actual Veo output
            except:
                st.warning("The camera is being set up, try one more time!")

    if st.button("🐾 Next Mission"):
        st.session_state.mission_complete = False
        st.session_state.current_topic = random.choice(list(FAVORITES.keys()))
        st.rerun()
