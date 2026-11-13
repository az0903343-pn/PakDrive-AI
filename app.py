import streamlit as st
import pandas as pd
import numpy as np
import joblib
import requests
from xgboost import XGBClassifier
from tensorflow.keras.models import load_model
from google import genai

# ==========================================
# 1. WEBSITE PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="PakDrive AI | Intelligent 3D Vehicle & Scheme Portal",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. LUXURY WEBSITE & 3D SHOWROOM CSS
# ==========================================
st.markdown("""
<style>
    @import url('https://googleapis.com');
    
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: linear-gradient(180deg, #0b1120 0%, #0f172a 50%, #090d16 100%) !important;
        color: #f8fafc !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1b4b 0%, #0f172a 100%) !important;
        border-right: 2px solid #10b981 !important;
    }
    
    h1, h2, h3, h4, h5, p, label, span {
        color: #f8fafc !important;
    }
    
    /* Top Website Navigation Bar */
    .web-navbar {
        background: rgba(15, 23, 42, 0.9);
        backdrop-filter: blur(12px);
        padding: 16px 28px;
        border-radius: 16px;
        border: 1px solid rgba(16, 185, 129, 0.4);
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    .web-brand {
        font-size: 26px;
        font-weight: 800;
        color: #34d399 !important;
    }
    
    /* Website Hero Section */
    .web-hero {
        background: linear-gradient(135deg, #064e3b 0%, #0f172a 55%, #1e1b4b 100%);
        padding: 45px 30px;
        border-radius: 22px;
        text-align: center;
        border: 1px solid #10b981;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.55);
        margin-bottom: 25px;
    }
    
    /* 3D Vehicle Card Styling */
    .card-3d-img {
        width: 100%;
        height: 170px;
        object-fit: contain;
        background: radial-gradient(circle, #ffffff 20%, #cbd5e1 100%);
        border-radius: 14px;
        padding: 12px;
        margin-bottom: 12px;
        transition: transform 0.4s ease;
    }
    .card-3d-img:hover {
        transform: scale(1.06) rotate(-2deg);
    }
    
    /* 360 Rotating 3D Showcase */
    @keyframes spin360 {
        0% { transform: perspective(900px) rotateY(-16deg) scale(1.0); }
        50% { transform: perspective(900px) rotateY(16deg) scale(1.06); }
        100% { transform: perspective(900px) rotateY(-16deg) scale(1.0); }
    }
    .spin-3d-stage {
        width: 100%;
        max-height: 230px;
        object-fit: contain;
        background: radial-gradient(circle, #ffffff 25%, #cbd5e1 100%);
        border-radius: 16px;
        padding: 16px;
        animation: spin360 6s infinite ease-in-out;
        box-shadow: 0 15px 35px rgba(16, 185, 129, 0.35);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. LOAD REAL KAGGLE ML & DL MODELS
# ==========================================
@st.cache_resource
def load_trained_models():
    df = pd.read_csv("vehicles_3d_master.csv")
    scaler = joblib.load("scaler.pkl")
    le_fuel = joblib.load("le_fuel.pkl")
    le_usage = joblib.load("le_usage.pkl")
    le_target = joblib.load("le_target.pkl")
    
    xgb_model = XGBClassifier()
    xgb_model.load_model("xgb_vehicle_model.json")
    
    dl_model = load_model("dl_vehicle_model.h5", compile=False)
    return df, scaler, le_fuel, le_usage, le_target, xgb_model, dl_model

df_master, scaler, le_fuel, le_usage, le_target, xgb_model, dl_model = load_trained_models()

# ==========================================
# 4. SIDEBAR: API KEYS & LIVE AI CHATBOT
# ==========================================
st.sidebar.markdown("""
<div style="background:linear-gradient(135deg,#059669,#10b981); padding:15px; border-radius:14px; text-align:center; margin-bottom:15px;">
    <div style="font-size:12px; color:#ecfdf5; font-weight:700;">🟢 Online • Hybrid ML + DL + LLM</div>
    <h3 style="color:#ffffff; margin:4px 0;">PakDrive AI Assistant</h3>
    <p style="color:#d1fae5; font-size:12px; margin:0;">Live Rates, Scheme Info & Vehicle Advice</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar.expander("🔑 Configure Live API Keys", expanded=False):
    gemini_key = st.text_input("Google Gemini API Key", type="password", help="Get free key from ://google.com")
    serper_key = st.text_input("Serper.dev Search API Key", type="password", help="Get free key from serper.dev")

def fetch_live_web(query, api_key):
    if not api_key:
        return []
    try:
        res = requests.post(
            "https://serper.dev",
            headers={"X-API-KEY": api_key, "Content-Type": "application/json"},
            json={"q": query, "gl": "pk"},
            timeout=8
        )
        return res.json().get("organic", [])[:3]
    except Exception:
        return []

def ask_gemini_llm(prompt_text, api_key):
    if not api_key:
        return ""
    try:
        client = genai.Client(api_key=api_key)
        resp = client.models.generate_content(model="gemini-2.5-flash", contents=prompt_text)
        return resp.text
    except Exception:
        return ""

if "chat_log" not in st.session_state:
    st.session_state.chat_log = [
        {"role": "assistant", "content": "Assalam-o-Alaikum! Main PakDrive AI hoon. Mujh se poochein ke 1 Lakh mein kaunsi bike best hai, Electric aur Petrol mein kya farq hai, ya Maryam Nawaz E-Bike Scheme mein kaise apply karein."}
    ]

for chat in st.session_state.chat_log:
    st.sidebar.chat_message(chat["role"]).write(chat["content"])

chat_box = st.sidebar.form(key="advisor_chat", clear_on_submit=True)
user_msg = chat_box.text_input("Apna sawal likhein...", placeholder="e.g. 1 lakh mein electric ya petrol?")
submitted = chat_box.form_submit_button("Ask AI 🚀", use_container_width=True)

if submitted and user_msg:
    st.session_state.chat_log.append({"role": "user", "content": user_msg})
    web_info = fetch_live_web(f"{user_msg} Pakistan vehicle price PakWheels Punjab scheme", serper_key)
    web_txt = "\n".join([f"- {w.get('title')}: {w.get('snippet')}" for w in web_info])
    
    llm_ans = ask_gemini_llm(
        f"You are an expert Pakistani automotive AI advisor. Answer in clear Roman Urdu.\nUser Question: {user_msg}\nLive Web Context: {web_txt}",
        gemini_key
    )
    if llm_ans:
        final_reply = llm_ans
    elif "scheme" in user_msg.lower() or "maryam" in user_msg.lower() or "punjab" in user_msg.lower():
        final_reply = "🏛️ **Maryam Nawaz Punjab E-Bike Scheme:** Punjab ke students aur workers ko **Jolta JE-70L, Yadea, aur Honda CD 70** bina sood (0% markup) ke 2 saal ki asaan aqsaat par di ja rahi hain (`bikes.punjab.gov.pk`)."
    elif len(web_info) > 0:
        first_w = next(iter(web_info))
        final_reply = f"🔎 **Live Market Update:** {first_w.get('snippet', '')}\n\n🔗 [Source Link]({first_w.get('link', 'https://pakwheels.com')})"
    else:
        final_reply = "Aap right side par apna exact budget (PKR) darj karein—hamara Deep Learning aur XGBoost model aapko foran best options, Electric vs Petrol comparison, aur Punjab Scheme eligibility dikha dega!"
    
    st.session_state.chat_log.append({"role": "assistant", "content": final_reply})
    st.rerun()

# ==========================================
# 5. WEBSITE TOP NAVBAR & HERO SECTION
# ==========================================
st.markdown("""
<div class="web-navbar">
    <div class="web-brand">🚘 PakDrive AI <span style="font-size:13px; color:#94a3b8;">| SMART MOBILITY & SCHEME PORTAL</span></div>
    <div style="font-size:13.5px; font-weight:600; color:#cbd5e1;">Home • 3D Showroom • Electric vs Petrol • Punjab E-Bike Scheme • Live Market API</div>
</div>

<div class="web-hero">
    <h1 style="font-size:38px; font-weight:800; margin-bottom:10px;">FIND YOUR PERFECT RIDE — CYCLE TO HELICOPTER</h1>
    <p style="font-size:16px; color:#d1fae5 !important; max-width:820px; margin:0 auto;">
        Powered by <b>XGBoost Machine Learning</b> & <b>Deep Neural Networks</b>. Apna budget select karein aur dekhein ke aap Electric Bike, Petrol Bike, Car, ya Helicopter mein se kya le sakte hain, unke Advantages/Disadvantages kya hain, aur Punjab Govt Scheme mein kya sahulat hai.
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 6. USER BUDGET & PREFERENCE PANEL
# ==========================================
st.markdown("### 🎛️ Apna Budget Aur Zaroorat Darj Karein")
col1, col2, col3, col4 = st.columns(4)
budget = col1.number_input("Aapka Budget (PKR)", min_value=15000, max_value=1500000000, value=160000, step=10000)
daily_km = col2.slider("Rozana ka Safar (KM)", min_value=2, max_value=500, value=35)
fuel_pref = col3.selectbox("Fuel / Power Type", ["Any (AI Best Choice)", "Electric", "Petrol", "Manual", "Diesel", "Aviation Fuel"])
usage_type = col4.selectbox("Istemaal (Purpose)", ["Personal", "Family", "Commercial", "Luxury/Offroad", "Marine/Leisure", "Aviation"])

# ==========================================
# 7. REAL ML (XGBOOST) + DL (NEURAL NETWORK) INFERENCE
# ==========================================
st.markdown("### 🧠 Live AI Model Predictions (Machine Learning + Deep Learning)")

pred_fuel = "Electric" if fuel_pref == "Any (AI Best Choice)" else fuel_pref
if pred_fuel not in le_fuel.classes_:
    pred_fuel = str(next(iter(le_fuel.classes_)))
if usage_type not in le_usage.classes_:
    usage_type = str(next(iter(le_usage.classes_)))

f_code = int(le_fuel.transform([pred_fuel]).item())
u_code = int(le_usage.transform([usage_type]).item())
