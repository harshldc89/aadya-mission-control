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

# 🎤 THE "IPAD-TOUCH" VOICE ENGINE
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

# MISSION DATA & STORY HOOKS
FAVORITES = {
    "Leopard": "A fast leopard found a mysterious silver key in the jungle. He needs to know what the key opens! Can you help him?",
    "Whale": "A giant blue whale discovered a hidden underwater cave filled with glowing bubbles. What is inside the cave?",
    "Airplane": "Your airplane is flying through a cloud made of pink cotton candy! Where are you landing today?",
    "Yoga": "You are a yoga master in a magical forest where the trees move with you. Which animal pose are you doing today?",
    "Swimming": "You are at the Bali resort in the infinity pool! Suddenly, you see a friendly dolphin waving at you from the beach. What happens next?",
    "Skating": "You are skating on a rainbow instead of ice! The colors are slippery and fast. Where are you skating to?",
    "Dancing": "You have magic shoes that only dance when you sing a special song. What does the dance look like?",
    "Ballet": "The stage is a giant lily pad on a pond! All the frogs are watching you dance. How do you start your performance?",
    "Bus": "This school bus can fly over the mountains! You just pushed a secret green button. Where is the bus taking everyone?",
    "Train": "The midnight train is made of chocolate and carries toys to the moon. What is your favorite toy on the train?",
    "Maldives": "The sand is white and the water is clear blue. You found a message in a bottle on the beach! What does the message say?",
    "Snorkeling": "Under the water, you found a fish wearing tiny glasses and reading a book! What is the fish learning about?",
    "Peppa Pig": "Peppa found the biggest muddy puddle in the world, but it smells like strawberries! Who is jumping in first?",
    "Numberblocks": "Number Ten is building a giant tower out of star-blocks, but he needs one more block to reach the sun. Which number helps him?",
    "Alphablocks": "The letter 'A' found an apple that makes people float like balloons! What happens when 'B' takes a bite?",
    "Sheriff Labrador": "A mystery! Someone left a trail of cookie crumbs leading to the police station. Who is the cookie thief?",
    "Disney": "Mickey Mouse invited you to a party at the castle, but the castle is floating in the sky! How do you get up there?"
}

if 'current_topic' not in st.session_state:
    st.session_state.current_topic = random.choice(list(FAVORITES.keys()))
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

# --- STEP 1: THE STORY MISSION ---
topic = st.session_state.current_topic
story_hook = FAVORITES[topic]

mission_text = f"Aadya, your mission today is {topic}! {story_hook} Write 1 or 2 sentences in your notebook to finish the story. All the best!"

st.markdown(f"""
<div style="padding:20px; border-radius:15px; border:2px solid #00529b; background-color:#ffffff; margin-bottom:10px;">
    <h3 style="color:#e21b22;">🐾 Mission: {topic}</h3>
    <p style="font-size:18px; color:#333; font-style: italic;">"{story_hook}"</p>
    <p style="font-size:16px; color:#555;">How was your day? Write the end of the story in your notebook!</p>
</div>
""", unsafe_allow_html=True)

# THE VOICE BUTTON
speak(mission_text)

# --- STEP 2: UPLOAD ---
st.write("---")
uploaded_file = st.file_uploader("📷 Upload writing photo", type=['png', 'jpg', 'jpeg'])

if uploaded_file and not st.session_state.mission_complete:
    if st.button("🚀 SCAN WRITING"):
        with st.spinner("🐾 Mission Control is scanning..."):
            time.sleep(2) 
            congrats = f"Wow Aadya! That was an amazing ending to the {topic} story! You are a creative superstar! Click below for your surprise."
            st.success(congrats)
            speak(congrats)
            st.session_state.mission_complete = True
            st.rerun()

# --- STEP 3: REVEAL ---
if st.session_state.mission_complete:
    if st.button("🌟 CLICK FOR YOUR SURPRISE"):
        st.balloons()
        topic = st.session_state.current_topic
        with st.spinner("🎨 Creating your Pixar-style gift..."):
            try:
                # SAFE PIXAR CARTOON PROMPT
                safe_prompt = f"A high-quality 3D Disney Pixar style image of {topic} in a magical setting. Vibrant colors, friendly, happy, safe for 6 year olds."
                response = client.models.generate_content(
                    model='gemini-2.0-flash-exp', 
                    contents=safe_prompt, 
                    config=types.GenerateContentConfig(response_modalities=['IMAGE'])
                )
                for part in response.parts:
                    if part.inline_data:
                        st.image(part.as_image())
            except:
                st.image(f"https://loremflickr.com/800/600/{topic},pixar", caption=f"Great job Aadya!")

    if st.button("🐾 New Mission"):
        st.session_state.mission_complete = False
        st.session_state.current_topic = random.choice(list(FAVORITES.keys()))
        st.rerun()
