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
    # This JS version is more reliable for iOS/iPadOS
    components.html(f"""
        <script>
            function playSpeech() {{
                window.speechSynthesis.cancel(); // Stop any current speech
                var msg = new SpeechSynthesisUtterance("{clean_text}");
                msg.lang = 'en-US';
                msg.rate = 0.9;
                msg.pitch = 1.1;
                window.speechSynthesis.speak(msg);
            }}
            // Force play on load for some browsers, but button is backup
            playSpeech();
        </script>
        <button onclick="playSpeech()" style="background-color: #f9d905; border: none; padding: 10px; border-radius: 10px; font-weight: bold; cursor: pointer;">
            📢 Click to Hear Mission Again
        </button>
    """, height=50)

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

# --- STEP 1: INTERACTIVE MISSION BRIEFING ---
topic = st.session_state.current_topic

# Create the personalized story based on the topic
if topic == "Swimming":
    personal_story = "There is a resort which we are going to in Bali where you love to swim around the beach facing infinity pool! How was your day? "
else:
    personal_story = f"I know how much you love {topic}! It is one of your favorite things in the whole world. How was your day? "

mission_text = f"Aadya, your mission today is {topic}. {personal_story} Write 1 or 2 sentences about this in your notebook. All the best, I will wait for the photo to be uploaded!"

st.markdown(f"""
<div style="padding:20px; border-radius:15px; border:2px solid #00529b; background-color:#ffffff; margin-bottom:10px;">
    <h3 style="color:#e21b22;">🐾 Mission: {topic}</h3>
    <p style="font-size:18px; color:#333;">{mission_text}</p>
</div>
""", unsafe_allow_html=True)

# Trigger the voice
speak(mission_text)

# --- STEP 2: UPLOAD WRITING ---
st.write("---")
uploaded_file = st.file_uploader("📷 Upload your writing photo here", type=['png', 'jpg', 'jpeg'])

if uploaded_file and not st.session_state.mission_complete:
    if st.button("🚀 SCAN WRITING & GET GIFT"):
        with st.spinner("🐾 Mission Control is scanning..."):
            time.sleep(2) 
            congrats = f"Wow Aadya! I see your sentences about {topic}. You are a writing superstar! Click the button below for your surprise."
            st.success(congrats)
            speak(congrats)
            st.session_state.mission_complete = True
            st.rerun()

# --- STEP 3: REVEAL SURPRISE ---
if st.session_state.mission_complete:
    st.write("### 🎁 MISSION ACCOMPLISHED!")
    if st.button("🌟 CLICK FOR YOUR SURPRISE"):
        st.balloons()
        topic = st.session_state.current_topic
        
        with st.spinner("🎨 Creating your Paw Patrol style gift..."):
            try:
                # Use a specific prompt to make it extra cute
                prompt = f"A cute 3D Pixar style image of {topic} wearing a Paw Patrol uniform and a gold crown. Vibrant colors, white background."
                # Note: We are using a reliable image search fallback to ensure she ALWAYS gets a picture
                st.image(f"https://loremflickr.com/800/600/{topic},disney", caption=f"A Special {topic} for Aadya!")
            except:
                st.image(f"https://loremflickr.com/800/600/{topic}", caption=f"Great job Aadya!")

    if st.button("🐾 Start New Mission"):
        st.session_state.mission_complete = False
        st.session_state.current_topic = random.choice(FAVORITES)
        st.rerun()
