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
    "Wildlife Photographer": {
        "hook": "A cheetah is resting in the shade of a tree. It looks right at you with big yellow eyes! What do you do?",
        "selfie_prompt": "A friendly 3D Pixar style image of 6 year old Aadya smiling while taking a photo of a curious cheetah resting under a tree. Vibrant, happy, safe for kids."
    },
    "Pilot": {
        "hook": "Your plane is soaring through fluffy, rainbow clouds. Where are you landing your passengers today?",
        "selfie_prompt": "A happy 3D Pixar style image of 6 year old Aadya in a pilot uniform, sitting in the cockpit of a flying airplane, smiling and waving. Rainbow clouds outside."
    },
    "Architect": {
        "hook": "You are building a house made of glowing glass bricks in a forest. What does the secret room look like?",
        "selfie_prompt": "A joyful 3D Pixar style image of 6 year old Aadya holding a model of a glowing glass house in a magical forest at night. Safe and friendly."
    },
    "Chef": {
        "hook": "You are making a giant pizza for a street party. What is the very last ingredient you add to make it yummy?",
        "selfie_prompt": "A 3D Pixar style image of 6 year old Aadya wearing a chef hat, smiling while adding toppings to a massive pizza in a sunny Italian kitchen."
    }
}

# --- INITIALIZE THEME AND PRE-GENERATE IMAGE ---
if 'theme_cycle' not in st.session_state:
    st.session_state.theme_cycle = "Gold"
if 'current_topic' not in st.session_state:
    st.session_state.current_topic = random.choice(list(FAVORITES.keys()))
    st.session_state.mission_complete = False
    st.session_state.reward_image = None

# 🚀 PRE-LOAD SURPRISE IMAGE
if st.session_state.reward_image is None:
    try:
        topic = st.session_state.current_topic
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp', 
            contents=FAVORITES[topic]['selfie_prompt'], 
            config=types.GenerateContentConfig(response_modalities=['IMAGE'])
        )
        for part in response.parts:
            if part.inline_data:
                st.session_state.reward_image = part.as_image()
    except:
        pass

# --- 🎨 THEME ROTATION STYLING ---
if st.session_state.theme_cycle == "Gold":
    st_bg = "#001f3f"; st_card_bg = "#FFD700"; st_border = "#C0C0C0"; st_text = "#000000"
    header_title = "🌟 GOLDEN MISSION"
else:
    st_bg = "#f0f2f6"; st_card_bg = "linear-gradient(to right, #ff9999, #ffcc99, #ffff99, #ccff99, #99ffff, #99ccff, #cc99ff)"; st_border = "#ffffff"; st_text = "#1a1a1a"
    header_title = "🌈 RAINBOW MISSION"

st.markdown(f"""
    <style>
        .stApp {{ background-color: {st_bg}; }}
        .header-box {{ text-align: center; padding: 15px; background-color: #e21b22; border-radius: 15px; border: 5px solid {st_border}; }}
        .mission-card {{ 
            padding: 25px; border-radius: 15px; border: 6px solid {st_border}; 
            background: {st_card_bg}; margin-top: 25px; box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
        }}
        .mission-header {{ color: {st_text} !important; font-size: 26px; font-weight: bold; margin-bottom: 10px; }}
        .mission-text {{ color: {st_text} !important; font-size: 22px; line-height: 1.4; font-weight: 500; }}
    </style>
    <div class="header-box"><h1 style="color: white; margin: 0;">🐾 MISSION CONTROL 🐾</h1></div>
    """, unsafe_allow_html=True)

# --- THE MISSION CARD ---
topic = st.session_state.current_topic
story = FAVORITES[topic]

st.markdown(f"""
<div class="mission-card">
    <div class="mission-header">{header_title}: {topic}</div>
    <p class="mission-text"><b>Step 1. Imagine:</b> {story['hook']}</p>
    <p class="mission-text"><b>Step 2. Write:</b> Finish the story in your notebook with 2 sentences!</p>
</div>
""", unsafe_allow_html=True)

speak(f"Aadya, Mission Control here! Your mission is {topic}. Imagine this: {story['hook']}. Now, write the ending in your notebook!")

# --- UPLOAD ---
st.write("")
uploaded_file = st.file_uploader("📷 Upload your writing photo:", type=['png', 'jpg', 'jpeg'])

if uploaded_file and not st.session_state.mission_complete:
    if st.button("🚀 SUBMIT TO MISSION CONTROL"):
        st.balloons()
        st.session_state.mission_complete = True
        st.rerun()

# --- REVEAL SURPRISE ---
if st.session_state.mission_complete:
    st.markdown("<h3 style='color:white; text-align:center;'>🎉 MISSION ACCOMPLISHED!</h3>", unsafe_allow_html=True)
    
    # --- UPDATED BUTTON NAME ---
    if st.button("🌟 SHOW SURPRISE"):
        if st.session_state.reward_image:
            st.image(st.session_state.reward_image, caption="Aadya's Creative Adventure! 3D Pixar Style")
            st.success("Great writing today, Aadya!")
        else:
            with st.spinner("One moment, getting your surprise ready..."):
                time.sleep(3)
                st.info("Tap 'Show Surprise' again to see your picture!")

    if st.button("🐾 Next Mission"):
        # Cycle Theme
        st.session_state.theme_cycle = "Rainbow" if st.session_state.theme_cycle == "Gold" else "Gold"
        # Reset Mission
        st.session_state.current_topic = random.choice(list(FAVORITES.keys()))
        st.session_state.mission_complete = False
        st.session_state.reward_image = None
        st.rerun()
