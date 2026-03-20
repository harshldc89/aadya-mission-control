import streamlit as st
import random
import time
import streamlit.components.v1 as components

st.set_page_config(page_title="Aadya's Mission Control", page_icon="🐾")

# 🎤 THE "IPAD-TOUCH" VOICE ENGINE
def speak_button(text, button_label="🔊 HEAR MISSION"):
    clean_text = text.replace("'", "").replace('"', "")
    # This creates a button that triggers the browser's voice ONLY when touched
    components.html(f"""
        <button id="speakBtn" style="
            width: 100%; 
            padding: 20px; 
            background-color: #f9d905; 
            color: #00529b; 
            border: 4px solid #00529b; 
            border-radius: 15px; 
            font-size: 20px; 
            font-weight: bold; 
            cursor: pointer;
            box-shadow: 5px 5px 0px #e21b22;
        ">
            {button_label}
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
    """, height=100)

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

# --- STEP 1: PERSONALIZED STORY ---
topic = st.session_state.current_topic
if topic == "Swimming":
    story = "Aadya, your mission is Swimming! There is a resort we are going to in Bali where you love to swim in the infinity pool facing the beach! How was your day? "
else:
    story = f"Aadya, your mission is {topic}! I know how much you love this. How was your day? "

mission_text = story + "Write 1 or 2 sentences in your notebook. I will wait for your photo!"

st.markdown(f"""
<div style="padding:20px; border-radius:15px; border:2px solid #00529b; background-color:#ffffff; margin-bottom:10px;">
    <h3 style="color:#e21b22;">🐾 Mission: {topic}</h3>
    <p style="font-size:18px; color:#333;">{mission_text}</p>
</div>
""", unsafe_allow_html=True)

# THE BIG YELLOW VOICE BUTTON
speak_button(mission_text)

# --- STEP 2: UPLOAD ---
st.write("---")
uploaded_file = st.file_uploader("📷 Upload writing photo", type=['png', 'jpg', 'jpeg'])

if uploaded_file and not st.session_state.mission_complete:
    if st.button("🚀 SCAN WRITING"):
        with st.spinner("🐾 Scanning..."):
            time.sleep(2) 
            congrats = f"Wow Aadya! You are a writing superstar! Click below for your surprise."
            st.success(congrats)
            speak_button(congrats, "🔊 HEAR CONGRATS")
            st.session_state.mission_complete = True
            st.rerun()

# --- STEP 3: REVEAL ---
if st.session_state.mission_complete:
    if st.button("🌟 CLICK FOR YOUR SURPRISE"):
        st.balloons()
        st.image(f"https://loremflickr.com/800/600/{topic},kids", caption=f"Great job Aadya!")

    if st.button("🐾 New Mission"):
        st.session_state.mission_complete = False
        st.session_state.current_topic = random.choice(FAVORITES)
        st.rerun()
