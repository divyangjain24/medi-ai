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

# === SIDEBAR ===
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
    ])

# === API FUNCTION ===
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

# === LAYOUT HELPER ===
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
    st.markdown("Get symptoms, causes, treatment, diet, and lifestyle guidance.")
    illness, go = render_input("Enter illness name:", "", "Get Info")
    if go and illness:
        query = f"""Provide professional medical info on "{illness}" with:
1. Definition & cause
2. Symptoms
3. Diagnosis & tests
4. Medical treatment
5. Home/natural remedies
6. Diet & nutrition
7. Lifestyle changes"""
        st.markdown(call_openrouter(query, "You are a medical expert and certified doctor."))

elif section == "💊 Medicine Details":
    st.header("💊 Medicine Information")
    st.markdown("Get accurate details on usage, dosage, risks, and interactions.")
    med, go = render_input("Enter medicine name:", "", "Get Info")
    if go and med:
        query = f"""Provide details for the medicine "{med}" including:
1. What it treats
2. Active ingredients
3. Dosage instructions
4. Side effects & interactions
5. Warnings & contraindications
6. Overdose and missed dose instructions"""
        st.markdown(call_openrouter(query, "You are a professional pharmacist."))

elif section == "💉 Illness to Medicines":
    st.header("💉 Get Medicines for Illness")
    st.markdown("Enter any illness name and get a list of common medicines prescribed for it.")
    illness_name, go = render_input("Enter illness name:", "e.g. migraine, asthma", "Find Medicines")
    if go and illness_name:
        query = f"""Give a list of commonly prescribed medicines for the illness "{illness_name}". Include:
1. Medicine name
2. Dosage form (tablet, syrup, etc.)
3. Purpose
4. OTC or prescription
5. Warnings or interactions"""
        st.markdown(call_openrouter(query, "You are a senior medical doctor and pharmacology expert."))

elif section == "🧘 Mental Health":
    st.header("🧘 Psychology & Mental Wellness")
    st.markdown("Get therapeutic strategies, mindfulness techniques, and mental health guidance.")
    topic, go = render_input("Enter mental health concern:", "", "Get Support")
    if go and topic:
        query = f"""Explain the mental health topic "{topic}" with:
1. Psychological background
2. Warning signs
3. Coping strategies
4. Therapy & treatment options
5. Self-care & daily routines
6. Mindfulness exercises"""
        st.markdown(call_openrouter(query, "You are a clinical psychologist and wellness therapist."))

elif section == "🌿 Natural Remedies":
    st.header("🌿 Homeopathy & Natural Remedies")
    st.markdown("Discover natural and homeopathic cures with lifestyle guidance.")
    condition, go = render_input("Enter condition:", "", "Get Remedy")
    if go and condition:
        query = f"""Suggest homeopathy and natural remedies for "{condition}" with:
1. Homeopathic medicine (with potencies)
2. Home remedies using ingredients
3. Ayurvedic or holistic alternatives
4. Lifestyle and prevention tips
5. What to avoid during condition"""
        st.markdown(call_openrouter(query, "You are an Ayurvedic and homeopathy expert."))

elif section == "🤖 Talk to Doctor AI":
    st.header("🤖 Talk to Doctor AI")
    st.markdown("Chat live with a friendly AI doctor. Ask anything about health, symptoms, or general advice.")
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_msg = st.chat_input("Ask your question...")
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
    st.markdown("Enter your symptoms (comma-separated) to get possible illness and suggestions.")
    symptoms, go = render_input("Enter symptoms:", "e.g. fever, cough, headache", "Check")
    if go and symptoms:
        query = f"""Given the symptoms: {symptoms}, predict:
1. Possible medical condition(s)
2. Likely causes
3. Medical advice and suggestions"""
        st.markdown(call_openrouter(query, "You are an AI medical assistant trained to diagnose based on symptoms."))
