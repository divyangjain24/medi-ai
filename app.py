import streamlit as st
import requests
from PIL import Image

# === CONFIG ===
API_KEY = st.secrets["OPENROUTER_API_KEY"]
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-3.5-turbo"

# === PAGE SETTINGS ===
st.set_page_config(page_title="MedMind AI", layout="wide", initial_sidebar_state="expanded")

# === GLOBAL STYLES ===
st.markdown("""
    <style>
    html, body, [class*="css"] {
        background-color: #121212;
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }
    .block-container {
        padding: 2rem;
        background-color: #1c1c1c;
        border-radius: 12px;
        box-shadow: 0 0 20px rgba(0,0,0,0.3);
    }
    .stButton>button {
        background-color: #00e0ff;
        color: black;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    .stTextInput>div>div>input, .stTextArea textarea {
        background-color: #2a2a2a;
        color: white;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# === HEADER ===
st.title("💼 MedMind AI Assistant")

try:
    image = Image.open("ai-doctor.jpg")
    st.image(image, caption="AI Doctor", use_container_width=True)
except:
    st.image(
        "https://img.freepik.com/free-photo/ai-robot-doctor-hologram-futuristic-hospital-concept_23-2151021679.jpg",
        caption="AI Doctor", use_container_width=True
    )

st.markdown("Your smart AI doctor for illness info, remedies, psychology, and live consultations.")

# === SIDEBAR WITH AUTO COLLAPSE ===
query_params = st.experimental_get_query_params()
default_section = query_params.get("section", ["🩺 Illness Diagnosis"])[0]

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3771/3771429.png", width=60)
    st.markdown("### Navigation")
    section = st.radio("Choose a service:", [
        "🩺 Illness Diagnosis",
        "💊 Medicine Details",
        "💉 Illness to Medicines",
        "🧘 Mental Health",
        "🌿 Natural Remedies",
        "🤖 Talk to Doctor AI",
        "🧪 Symptom Checker"
    ], index=[
        "🩺 Illness Diagnosis",
        "💊 Medicine Details",
        "💉 Illness to Medicines",
        "🧘 Mental Health",
        "🌿 Natural Remedies",
        "🤖 Talk to Doctor AI",
        "🧪 Symptom Checker"
    ].index(default_section))

    st.experimental_set_query_params(section=section)

# === Collapse Sidebar for Chatbot ===
if section == "🤖 Talk to Doctor AI":
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        [data-testid="collapsedControl"] {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)

# === API CALL ===
def call_openrouter(prompt, system_role):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_role},
            {"role": "user", "content": prompt}
        ]
    }
    res = requests.post(API_URL, headers=headers, json=body)
    if res.status_code == 200:
        return res.json()["choices"][0]["message"]["content"]
    else:
        return f"❌ Error {res.status_code}: {res.text}"

# === INPUT LAYOUT ===
def render_input(label, placeholder, button_label):
    col1, col2 = st.columns([4, 1])
    with col1:
        value = st.text_input(label, placeholder)
    with col2:
        submit = st.button(button_label)
    return value, submit

# === SECTION HANDLERS ===
if section == "🩺 Illness Diagnosis":
    st.header("🩺 Diagnose Illness")
    illness, go = render_input("Enter illness name:", "", "Get Info")
    if go and illness:
        prompt = f"""Provide professional medical info on "{illness}" with:
1. Definition & cause
2. Symptoms
3. Diagnosis & tests
4. Medical treatment
5. Home/natural remedies
6. Diet & nutrition
7. Lifestyle changes"""
        st.markdown(call_openrouter(prompt, "You are a medical expert and certified doctor."))

elif section == "💊 Medicine Details":
    st.header("💊 Medicine Information")
    med, go = render_input("Enter medicine name:", "", "Get Info")
    if go and med:
        prompt = f"""Provide details for the medicine "{med}" including:
1. What it treats
2. Active ingredients
3. Dosage instructions
4. Side effects & interactions
5. Warnings & contraindications
6. Overdose and missed dose instructions"""
        st.markdown(call_openrouter(prompt, "You are a professional pharmacist."))

elif section == "💉 Illness to Medicines":
    st.header("💉 Medicines for an Illness")
    illness, go = render_input("Enter illness name:", "", "Find Medicines")
    if go and illness:
        prompt = f"""For the illness "{illness}", list:
1. Common medicines prescribed
2. Dosage forms
3. Prescription vs OTC
4. Natural alternatives
5. Safety & warnings"""
        st.markdown(call_openrouter(prompt, "You are a certified doctor and pharmacist."))

elif section == "🧘 Mental Health":
    st.header("🧘 Psychology & Mental Wellness")
    topic, go = render_input("Enter mental health concern:", "", "Get Support")
    if go and topic:
        prompt = f"""Explain the mental health topic "{topic}" with:
1. Psychological background
2. Warning signs
3. Coping strategies
4. Therapy & treatment options
5. Self-care & daily routines
6. Mindfulness exercises"""
        st.markdown(call_openrouter(prompt, "You are a clinical psychologist and wellness therapist."))

elif section == "🌿 Natural Remedies":
    st.header("🌿 Homeopathy & Natural Remedies")
    condition, go = render_input("Enter condition:", "", "Get Remedy")
    if go and condition:
        prompt = f"""Suggest homeopathy and natural remedies for "{condition}" with:
1. Homeopathic medicine (with potencies)
2. Home remedies using ingredients
3. Ayurvedic or holistic alternatives
4. Lifestyle and prevention tips
5. What to avoid during condition"""
        st.markdown(call_openrouter(prompt, "You are an Ayurvedic and homeopathy expert."))

elif section == "🤖 Talk to Doctor AI":
    st.header("🤖 Talk to Doctor AI")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_msg = st.chat_input("Ask your health question...")
    if user_msg:
        st.session_state.chat_history.append({"role": "user", "content": user_msg})
        messages = [{"role": "system", "content": "You are a smart, experienced doctor giving accurate and kind advice."}]
        messages += st.session_state.chat_history
        res = requests.post(API_URL, headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }, json={"model": MODEL, "messages": messages})
        if res.status_code == 200:
            reply = res.json()["choices"][0]["message"]["content"]
            st.session_state.chat_history.append({"role": "assistant", "content": reply})
        else:
            st.error("❌ API error")

    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

elif section == "🧪 Symptom Checker":
    st.header("🧪 Symptom Checker")
    symptoms, go = render_input("Enter symptoms:", "e.g. fever, cough, headache", "Check")
    if go and symptoms:
        prompt = f"""Given the symptoms: {symptoms}, predict:
1. Possible medical condition(s)
2. Likely causes
3. Medical advice and suggestions"""
        st.markdown(call_openrouter(prompt, "You are an AI medical assistant trained to diagnose based on symptoms."))
