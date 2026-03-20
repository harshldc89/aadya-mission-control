import streamlit as st
from google import genai
from google.genai import types
import random
import time
from PIL import Image
import streamlit.components.v1 as components

# 1. API CONFIGURATION
API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

st.set_page_config(page_title="Aadya's Mission Control", page_icon="🚀")

# 🎤 VOICE FUNCTION (Browser-based TTS)
def speak(text):
    clean_text = text.replace("'", "").replace('"', "")
    components.html(f"""
        <script>
            var msg = new SpeechSynthesisUtterance("{clean_text}");
            msg.lang = 'en-US';
            msg.rate = 0.9; 
            window.speechSynthesis.speak(msg);
        </script>
    """, height=0)

# MISSION DATA
FAVORITES = ["Leopard", "Whale", "Airplane", "Yoga", "Swimming", "Skating", "Dancing", "Ballet", "Bus", "Train", "Maldives", "Snorkeling", "Peppa Pig", "Numberblocks", "Alphablocks", "Sheriff Labrador", "Disney"]

if 'reward_type' not in st.session_state:
    st.session_state.reward_type = "Image"
if 'current_topic' not in st.session_state:
    st.session_state.current_topic = random.choice(FAVORITES)
if 'mission_complete' not in st.session_state:
    st.session_state.mission_complete = False

st.title("🚀 Aadya's Mission Control")

# --- STEP 1: MISSION BRIEFING ---
mission_text = f"Today's Mission is {st.session_state.current_topic}. Write 1 or 2 sentences about this in your notebook. All the best, I will wait for the photo to be uploaded."

st.markdown(f"""
<div style="padding:20px; border-radius:15px; border:2px solid #FF4B4B; background-color:#ffffff; margin-bottom:10px;">
    <h3 style="color:#FF4B4B;">🔬 Subject: {st.session_state.current_topic}</h3>
    <p style="font-size:18px;">{mission_text}</p>
</div>
""", unsafe_allow_html=True)

# 🔊 VOICE BUTTON (Fixes the "No Voice" issue)
if st.button("🔊 Play Mission Briefing"):
    speak(mission_text)

# --- STEP 2: UPLOAD WRITING ---
st.write("---")
uploaded_file = st.file_uploader("📷 Take a photo of your writing", type=['png', 'jpg', 'jpeg'])

if uploaded_file and not st.session_state.mission_complete:
    image_bytes = uploaded_file.getvalue()
    vision_prompt = f"This is writing from 6-year-old Aadya. Be an encouraging 'Mission Control'. Praise her for writing about {st.session_state.current_topic}. Mention one specific thing like a nice capital letter. Keep it to 2 sentences."
    
    with st.spinner("Mission Control is scanning..."):
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=[vision_prompt, types.Part.from_bytes(data=image_bytes, mime_type='image/jpeg')]
            )
            congrats_text = response.text
            st.success(congrats_text)
            speak(congrats_text) 
            st.session_state.mission_complete = True
            st.rerun() # Refresh to show the Reward Button
        except:
            st.error("Mission Control had a tiny hiccup. Please try again!")

# --- STEP 3: REVEAL SURPRISE ---
if st.session_state.mission_complete:
    st.write("### 🎉 MISSION COMPLETE!")
    if st.button("🎁 CLICK HERE FOR YOUR SURPRISE"):
        st.balloons()
        topic = st.session_state.current_topic
        
        with st.spinner("🎨 Creating your surprise gift..."):
            try:
                # Force image generation
                prompt = f"A fun, 3D Disney Pixar style image of a {topic} having a party. Vibrant colors, happy mood."
                img_resp = client.models.generate_content(
                    model='gemini-2.0-flash-exp', 
                    contents=prompt, 
                    config=types.GenerateContentConfig(response_modalities=['IMAGE'])
                )
                
                image_found = False
                for part in img_resp.parts:
                    if part.inline_data:
                        st.image(part.as_image(), caption=f"A Special {topic} for Aadya!")
                        image_found = True
                
                if not image_found:
                    st.warning("The gift is being wrapped! Try clicking the button again.")
            except Exception as e:
                st.error("The gift shop is busy! Try clicking 'REVEAL' one more time.")

    if st.button("Start New Mission"):
        st.session_state.mission_complete = False
        st.session_state.current_topic = random.choice(FAVORITES)
        st.rerun()
