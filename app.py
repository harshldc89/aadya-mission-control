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

# 🕯️ STAY AWAKE SCRIPT (Prevents Screen Lock)
components.html("""
    <script>
        let wakeLock = null;
        async function requestWakeLock() {
            try {
                wakeLock = await navigator.wakeLock.request('screen');
                console.log('Screen Wake Lock is active');
            } catch (err) {
                console.log('Wake Lock failed: ' + err.name);
            }
        }
        requestWakeLock();
        // Re-request when tab becomes visible again
        document.addEventListener('visibilitychange', async () => {
            if (wakeLock !== null && document.visibilityState === 'visible') {
                requestWakeLock();
            }
        });
    </script>
""", height=0)

# 🎤 THE IPAD-STABLE VOICE ENGINE
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

# MISSION DATA
FAVORITES = {
    "Leopard": "A fast leopard found a mysterious silver key in the jungle. He needs to know what the key opens!",
    "Whale": "A giant blue whale discovered a hidden underwater cave filled with glowing bubbles.",
    "Airplane": "Your airplane is flying through a cloud made of pink cotton candy! Where are you landing?",
    "Yoga": "You are a yoga master in a magical forest where the trees move with you.",
    "Swimming": "You are at the Bali resort in the infinity pool! Suddenly, a friendly dolphin waves at you.",
    "Skating": "You are skating on a slippery rainbow instead of ice! Where does it lead?",
    "Dancing": "You have magic shoes that only dance when you sing a special song.",
    "Ballet": "The stage is a giant lily pad on a pond and the frogs are watching you dance.",
    "Bus": "This school bus can fly! You just pushed a secret green button to go to space.",
    "Train": "The midnight train is made of chocolate and carries toys to the moon.",
    "Maldives": "The water is clear blue and you found a message in a bottle on the beach!",
    "Snorkeling": "Under the water, you found a fish wearing tiny glasses and reading a book!",
    "Peppa Pig": "Peppa found a muddy puddle that smells like strawberries. Who jumps in first?",
    "Numberblocks": "Number Ten is building a tower to the sun, but he needs one more block.",
    "Alphablocks": "The letter 'A' found an apple that makes people float like balloons!",
    "Sheriff Labrador": "Someone left a trail of cookie crumbs leading to the police station!",
    "Disney": "Mickey Mouse invited you to a castle that is floating in the sky!"
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

# --- STEP 1: CLEAR INSTRUCTIONS ---
topic = st.session_state.current_topic
story_hook = FAVORITES[topic]

st.markdown(f"""
<div style="padding:20px; border-radius:15px; border:3px solid #00529b; background-color:#ffffff; margin-bottom:10px;">
    <h2 style="color:#e21b22; margin-top:0; font-size:24px;">📋 Step-by-Step Mission:</h2>
    <div style="font-size:20px; color:#333; line-height:1.6;">
        <p><b>1. Tell Daddy:</b> How was your day? 👋</p>
        <p><b>2. Imagine:</b> {story_hook} ✨</p>
        <p><b>3. Write:</b> Finish the story in your notebook! ✍️</p>
    </div>
</div>
""", unsafe_allow_html=True)

mission_voice = f"Aadya, Mission Control here! Number one: Tell Daddy how your day was. Number two: Imagine {story_hook}. Number three: Write the end of the story in your notebook! All the best!"
speak(mission_voice)

# --- STEP 2: UPLOAD ---
st.write("---")
uploaded_file = st.file_uploader("📷 Mission finished? Take a photo!", type=['png', 'jpg', 'jpeg'])

if uploaded_file and not st.session_state.mission_complete:
    if st.button("🚀 SUBMIT TO MISSION CONTROL"):
        with st.spinner("🐾 Scanning your work..."):
            time.sleep(2) 
            congrats = f"Excellent work, Aadya! That {topic} story was wonderful. You have completed the mission!"
            st.success(congrats)
            speak(congrats)
            st.session_state.mission_complete = True
            st.rerun()

# --- STEP 3: REVEAL ---
if st.session_state.mission_complete:
    if st.button("🌟 GET YOUR SURPRISE"):
        st.balloons()
        with st.spinner("🎨 Creating your Pixar gift..."):
            try:
                safe_prompt = f"A cute 3D Disney Pixar style image of {topic} in a happy magical world. Safe for 6 year olds."
                response = client.models.generate_content(
                    model='gemini-2.0-flash-exp', 
                    contents=safe_prompt, 
                    config=types.GenerateContentConfig(response_modalities=['IMAGE'])
                )
                for part in response.parts:
                    if part.inline_data:
                        st.image(part.as_image())
            except:
                st.image(f"https://loremflickr.com/800/600/{topic},pixar")

    if st.button("🐾 Next Mission"):
        st.session_state.mission_complete = False
        st.session_state.current_topic = random.choice(list(FAVORITES.keys()))
        st.rerun()
