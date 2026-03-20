import streamlit as st
from google import genai
from google.genai import types
import random
import time
from PIL import Image
import io
import streamlit.components.v1 as components

# 1. API CONFIGURATION
API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=API_KEY)

st.set_page_config(page_title="Aadya's Mission Control", page_icon="🐾")

# 🎤 VOICE FUNCTION
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

# --- STEP 1: MISSION BRIEFING ---
mission_text = f"Today's Mission is {st.session_state.current_topic}. Write 1 or 2 sentences about this in your notebook. All the best, I will wait for the photo to be uploaded."

st.markdown(f"""
<div style="padding:20px; border-radius:15px; border:2px solid #00529b; background-color:#ffffff; margin-bottom:10px;">
    <h3 style="color:#e21b22;">🐾 Mission: {st.session_state.current_topic}</h3>
    <p style="font-size:18px; color:#333;">{mission_text}</p>
</div>
""", unsafe_allow_html=True)

if st.button("🔊 Wake Up Mission Control & Listen"):
    speak(mission_text)

# --- STEP 2: UPLOAD WRITING ---
st.write("---")
uploaded_file = st.file_uploader("📷 Take a photo of your writing", type=['png', 'jpg', 'jpeg'])

if uploaded_file and not st.session_state.mission_complete:
    # 📸 IMAGE COMPRESSION (To stop the 'Recharging' error)
    image = Image.open(uploaded_file)
    if image.mode in ("RGBA", "P"): image = image.convert("RGB")
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG', quality=60) # Compress to 60% quality
    final_bytes = img_byte_arr.getvalue()
    
    vision_prompt = f"Identify the handwriting. Be 'Mission Control' for 6-year-old Aadya. Give 2 sentences of high praise for writing about {st.session_state.current_topic}."
    
    with st.spinner("🐾 Scanning scientific data..."):
        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash",
                contents=[vision_prompt, types.Part.from_bytes(data=final_bytes, mime_type='image/jpeg')]
            )
            congrats_text = response.text
            st.success(congrats_text)
            speak(congrats_text) 
            st.session_state.mission_complete = True
            st.rerun() 
        except Exception as e:
            st.error("Mission Control is recharging! Please click the Browse button and try one more time.")

# --- STEP 3: REVEAL SURPRISE ---
if st.session_state.mission_complete:
    st.write("### 🎁 MISSION ACCOMPLISHED!")
    if st.button("🌟 CLICK FOR YOUR SURPRISE"):
        st.balloons()
        topic = st.session_state.current_topic
        with st.spinner("🎨 Creating your Paw Patrol style gift..."):
            try:
                prompt = f"A high-quality 3D Disney Pixar style image of {topic} wearing a Paw Patrol uniform and a crown. Vibrant colors, happy mood."
                img_resp = client.models.generate_content(
                    model='gemini-2.0-flash-exp', 
                    contents=prompt, 
                    config=types.GenerateContentConfig(response_modalities=['IMAGE'])
                )
                for part in img_resp.parts:
                    if part.inline_data:
                        st.image(part.as_image(), caption=f"A Special Surprise for Aadya!")
            except:
                st.warning("The gift is being wrapped! Click one more time!")

    if st.button("🐾 Start New Mission"):
        st.session_state.mission_complete = False
        st.session_state.current_topic = random.choice(FAVORITES)
        st.rerun()
