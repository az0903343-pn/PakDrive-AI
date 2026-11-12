import streamlit as st
import pandas as pd
import numpy as np
import joblib
import requests
from xgboost import XGBClassifier
from tensorflow.keras.models import load_model
from google import genai

# ==========================================
# PAGE CONFIGURATION & WEBSITE THEME CSS
# ==========================================
st.set_page_config(
    page_title="PakDrive AI | Smart Vehicle & Scheme Advisor",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS (Inspired by your Emerald Green & White Website Image + 3D Cards)
st.markdown("""
<style>
    @import url('https://googleapis.com');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: #f8faf9;
    }
    
    /* Top Navbar */
    .navbar {
        background-color: #ffffff;
        padding: 15px 30px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        border-bottom: 3px solid #0d4b26;
    }
    .nav-logo {
        font-size: 24px;
        font-weight: 700;
        color: #0d4b26;
    }
    .nav-links {
        color: #4a5568;
        font-size: 14px;
        font-weight: 500;
    }
    
    /* Hero Banner */
    .hero-box {
        background: linear-gradient(135deg, #09381c 0%, #146c38 100%);
        padding: 45px 30px;
        border-radius: 18px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 25px rgba(13, 75, 38, 0.25);
        margin-bottom: 25px;
    }
    .hero-title {
        font-size: 36px;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .hero-subtitle {
        font-size: 16px;
        color: #d1fae5;
        max-width: 750px;
        margin: 0 auto;
    }
    
    /* Floating Search Card */
    .search-container {
        background: #ffffff;
        padding: 25px;
        border-radius: 16px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        margin-bottom: 30px;
    }
    
    /* 3D Vehicle Cards */
    .vehicle-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 6px 20px rgba(0,0,0,0.06);
        border: 1px solid #edf2f7;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
    }
    .vehicle-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 15px 35px rgba(13, 75, 38, 0.18);
        border-color: #0d4b26;
    }
    .vehicle-img-3d {
        width: 140px;
        height: 140px;
        object-fit: contain;
        filter: drop-shadow(0 12px 15px rgba(0,0,0,0.2));
        margin-bottom: 15px;
        transition: transform 0.4s ease;
    }
    .vehicle-card:hover .vehicle-img-3d {
        transform: scale(1.12) rotate(-3deg);
    }
    .badge-scheme {
        background-color: #dcfce7;
        color: #166534;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 8px;
    }
    .price-tag {
        font-size: 20px;
        font-weight: 700;
        color: #0d4b26;
        margin: 8px 0;
    }
    
    /* Footer */
    .footer {
        background-color: #09381c;
        color: #e2e8f0;
        padding: 25px;
        border-radius: 14px;
        text-align: center;
        margin-top: 40px;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD TRAINED ML & DL MODELS
# ==========================================
@st.cache_resource
def load_assets():
    df = pd.read_csv("vehicles_3d_master.csv")
    scaler = joblib.load("scaler.pkl")
    le_fuel = joblib.load("le_fuel.pkl")
    le_usage = joblib.load("le_usage.pkl")
    le_target = joblib.load("le_target.pkl")
    
    xgb_model = XGBClassifier()
    xgb_model.load_model("xgb_vehicle_model.json")
    
    dl_model = load_model("dl_vehicle_model.h5")
    return df, scaler, le_fuel, le_usage, le_target, xgb_model, dl_model

try:
    df, scaler, le_fuel, le_usage, le_target, xgb_model, dl_model = load_assets()
except Exception as e:
    st.error(f"Model files load karne mein masla aaya: {e}. Yaqeeni banayein ke tamam .pkl, .h5, aur .json files GitHub repo mein mojood hain.")
    st.stop()

# ==========================================
# TOP NAVBAR & HERO SECTION
# ==========================================
st.markdown("""
<div class="navbar">
    <div class="nav-logo">🚘 PakDrive AI <span style="font-size:13px; color:#16a34a;">| 3D Vehicle & Scheme Advisor</span></div>
    <div class="nav-links">Bicycle to Helicopter • Electric vs Petrol • Punjab E-Bike Scheme • Live Rates</div>
</div>

<div class="hero-box">
    <div class="hero-title">DISCOVER YOUR PERFECT RIDE IN PAKISTAN</div>
    <div class="hero-subtitle">
        Cycle se lekar Helicopter tak — Apna budget darj karein aur hamara Hybrid Machine Learning + Deep Learning AI aapko behtareen sawari, Electric vs Petrol comparison, aur Maryam Nawaz Punjab E-Bike Scheme ki mukammal tafseel dega.
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# API KEYS CONFIGURATION (OPTIONAL LIVE SEARCH)
# ==========================================
with st.expander("🔑 Live Market Rates & AI Analysis API Keys (Optional)"):
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        gemini_api_key = st.text_input("Google Gemini API Key (Detailed Pros/Cons & Scheme Advice)", type="password")
    with col_k2:
        serper_api_key = st.text_input("Serper.dev API Key (Live PakWheels & Govt Portal Rates)", type="password")

# ==========================================
# USER INPUT PANEL (WEBSITE SEARCH BAR STYLE)
# ==========================================
st.markdown('<div class="search-container">', unsafe_allow_html=True)
st.subheader("🔍 Apni Zaroorat Aur Budget Batayein")

c1, c2, c3, c4 = st.columns(4)
with c1:
    budget = st.number_input("Aapka Budget (PKR)", min_value=15000, max_value=1500000000, value=185000, step=10000)
with c2:
    daily_km = st.slider("Rozana ka Safar (KM)", min_value=2, max_value=500, value=35)
with c3:
    fuel_pref = st.selectbox("Fuel / Power Type", ["Any (AI Recommend)", "Electric", "Petrol", "Manual", "Diesel", "Aviation Fuel"])
with c4:
    usage_type = st.selectbox("Istemaal (Purpose)", ["Personal", "Family", "Commercial", "Luxury/Offroad", "Marine/Leisure", "Aviation"])

predict_btn = st.button("🚀 Find Best Vehicle & Compare Now", use_container_width=True, type="primary")
st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PREDICTION & 3D RESULTS SECTION
# ==========================================
if predict_btn:
    # Model Prediction Logic
    selected_fuel = "Electric" if fuel_pref == "Any (AI Recommend)" else fuel_pref
    if selected_fuel not in le_fuel.classes_:
        selected_fuel = le_fuel.classes_[0]
    if usage_type not in le_usage.classes_:
        usage_type = le_usage.classes_[0]

    fuel_enc = le_fuel.transform([selected_fuel])[0]
    usage_enc = le_usage.transform([usage_type])[0]
    passengers = 1 if budget < 150000 else (2 if budget < 500000 else 5)
    
    input_data = np.array([[np.log1p(budget), daily_km, passengers, fuel_enc, usage_enc]])
    input_scaled = scaler.transform(input_data)
    
    # Deep Learning & XGBoost Predictions
    dl_probs = dl_model.predict(input_scaled, verbose=0)[0]
    dl_pred_idx = np.argmax(dl_probs)
    dl_confidence = dl_probs[dl_pred_idx] * 100
    predicted_category = le_target.inverse_transform([dl_pred_idx])[0]
    
    xgb_pred_idx = xgb_model.predict(input_scaled)[0]
    xgb_category = le_target.inverse_transform([xgb_pred_idx])[0]

    # Top AI Prediction Banner
    st.success(f"🧠 **Deep Learning Model Prediction:** `{predicted_category.split('_', 1)[1]}` (Confidence: **{dl_confidence:.1f}%**) | 🚀 **XGBoost ML Prediction:** `{xgb_category.split('_', 1)[1]}`")

    # Budget ke mutabiq best matching vehicles filter karna
    matched_df = df[(df["Price_PKR"] <= budget * 1.25) & (df["Price_PKR"] >= budget * 0.40)].drop_duplicates(subset=["Model_Name"])
    if matched_df.empty:
        df["Price_Diff"] = abs(df["Price_PKR"] - budget)
        matched_df = df.sort_values("Price_Diff").drop_duplicates(subset=["Model_Name"]).head(4)
    else:
        matched_df = matched_df.head(4)

    # 3D Vehicle Cards Display
    st.markdown("### 🏆 Aapke Budget Mein Behtareen 3D Options")
    cols = st.columns(len(matched_df))
    
    for idx, (_, row) in enumerate(matched_df.iterrows()):
        with cols[idx]:
            scheme_html = f'<div class="badge-scheme">🏛️ {row["Govt_Scheme"]}</div>' if "Yes" in str(row["Govt_Scheme"]) else '<div class="badge-scheme" style="background:#f1f5f9; color:#475569;">Standard Market</div>'
            st.markdown(f"""
            <div class="vehicle-card">
                {scheme_html}
                <br>
                <img src="{row['Image_3D_URL']}" class="vehicle-img-3d">
                <h4 style="margin:5px 0; color:#1e293b;">{row['Model_Name']}</h4>
                <div style="font-size:13px; color:#64748b;">{row['Fuel_Type']} • Max Range: {row['Max_Range_KM']} km</div>
                <div class="price-tag">Rs. {row['Price_PKR']:,.0f}</div>
                <div style="font-size:12px; color:#0f766e; margin-bottom:10px;">Running Cost: Rs. {row['Running_Cost_Per_100km']}/100km</div>
                <hr style="margin:10px 0;">
                <div style="text-align:left; font-size:12px;">
                    <p style="color:#15803d;"><b>✅ Advantages:</b> {row['Advantages']}</p>
                    <p style="color:#b91c1c;"><b>❌ Disadvantages:</b> {row['Disadvantages']}</p>
                </div>
            </div>
