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

# MISSIONS
FAVORITES = {
    "Leopard": {"hook": "You are a wildlife photographer. You spotted a leopard in the tall grass watching a bird. What happens next?", "v_prompt": "3D Pixar style leopard in jungle grass, 5s."},
    "Airplane": {"hook": "You are a pilot flying over a city at night. Where are you landing your passengers?", "v_prompt": "3D Pixar pilot cockpit view over city lights, 5s."},
    "Swimming": {"hook": "You are in a Bali infinity pool and find something shiny at the bottom. What is it?", "v_prompt": "3D Pixar Bali infinity pool, glowing coin at bottom, 5s."},
    "Architecture": {"hook": "You are an architect building a glass house with a secret library. What is inside?", "v_prompt": "3D Pixar modern glass house in forest, cozy lights, 5s."}
}

# --- INITIALIZE THEME ROTATION ---
if 'theme_cycle' not in st.session_state:
    st.session_state.theme_cycle = "Gold" # Starts with Gold
if 'current_topic' not in st.session_state:
    st.session_state.current_topic = random.choice(list(FAVORITES.keys()))
    st.session_state.mission_complete = False
    st.session_state.video_ready = None

# PRE-LOAD VIDEO
if st.session_state.video_ready is None:
    try:
        topic = st.session_state.current_topic
        video_res = client.models.generate_content(model='veo', contents=FAVORITES[topic]['v_prompt'])
        for part in video_res.parts:
            if part.inline_data:
                st.session_state.video_ready = part.inline_data.data
    except: pass

# --- 🎨 THEME LOGIC ---
if st.session_state.theme_cycle == "Gold":
    bg_color = "#001f3f"      # Navy
    card_bg = "#FFD700"       # Gold
    border_color = "#C0C0C0"  # Silver
    text_color = "#000000"    # Black
    header_text = "🌟 GOLDEN MISSION"
else:
    bg_color = "#f0f2f6"      # Soft White
    card_bg = "linear-gradient(to right, #ff9999, #ffcc99, #ffff99, #ccff99, #99ffff, #99ccff, #cc99ff)" # Rainbow
    border_color = "#ffffff"  # White
    text_color = "#1a1a1a"    # Deep Charcoal
    header_text = "🌈 RAINBOW MISSION"

st.markdown(f"""
    <style>
        .stApp {{ background-color: {bg_color}; }}
        .header-box {{ text-align: center; padding: 20px; background-color: #e21b22; border-radius: 15px; border: 5px solid #f9d905; }}
        .mission-card {{ 
            padding: 25px; border-radius: 15px; border: 6px solid {border_color}; 
            background: {card_bg}; margin-top: 25px; box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
        }}
        .mission-header {{ color: {text_color} !important; font-size: 26px; font-weight: bold; margin-bottom: 15px; }}
        .mission-text {{ color: {text_color} !important; font-size: 22px; line-height: 1.4; font-weight: 500; }}
    </style>
    <div class="header-box"><h1 style="color: white; margin: 0;">🐾 MISSION CONTROL 🐾</h1></div>
    """, unsafe_allow_html=True)

topic = st.session_state.current_topic
story = FAVORITES[topic]

st.markdown(f"""
<div class="mission-card">
    <div class="mission-header">{header_text}: {topic}</div>
    <p class="mission-text"><b>Step 1. Imagine:</b> {story['hook']}</p>
    <p class="mission-text"><b>Step 2. Write:</b> Finish the story in your notebook!</p>
</div>
""", unsafe_allow_html=True)

speak(f"Aadya, Mission Control here! Today is a {st.session_state.theme_cycle} mission. Imagine this: {story['hook']}. Write the ending now!")

st.write("")
uploaded_file = st.file_uploader("📷 Upload writing photo", type=['png', 'jpg', 'jpeg'])

if uploaded_file and not st.session_state.mission_complete:
    if st.button("🚀 SUBMIT TO MISSION CONTROL"):
        st.balloons()
        st.session_state.mission_complete = True
        st.rerun()

if st.session_state.mission_complete:
    st.markdown(f"<h3 style='color:white; text-align:center;'>🎉 MISSION ACCOMPLISHED!</h3>", unsafe_allow_html=True)
    if st.button("🎬 WATCH YOUR MOVIE"):
        if st.session_state.video_ready:
            st.video(st.session_state.video_ready)
        else:
            with st.spinner("🎥 Movie is arriving..."):
                time.sleep(5); st.info("Tap again to play!")

    if st.button("🐾 Next Mission"):
        # TOGGLE THEME FOR NEXT TIME
        st.session_state.theme_cycle = "Rainbow" if st.session_state.theme_cycle == "Gold" else "Gold"
        st.session_state.current_topic = random.choice(list(FAVORITES.keys()))
        st.session_state.mission_complete = False
        st.session_state.video_ready = None
        st.rerun()
