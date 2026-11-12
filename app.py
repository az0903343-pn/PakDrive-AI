import streamlit as st
import pandas as pd
import numpy as np
import joblib
from xgboost import XGBClassifier
from tensorflow.keras.models import load_model
from duckduckgo_search import DDGS

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="PakDrive AI | 3D Vehicle & Punjab Scheme Advisor",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://googleapis.com');
    
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #f4f7f5 !important;
        color: #1a202c !important;
        font-family: 'Poppins', sans-serif !important;
    }
    
    h1, h2, h3, h4, h5, p, label, span {
        color: #1a202c !important;
    }
    
    .navbar {
        background-color: #ffffff;
        padding: 16px 32px;
        border-radius: 14px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        border-bottom: 4px solid #0d4b26;
    }
    .nav-logo {
        font-size: 26px;
        font-weight: 700;
        color: #0d4b26 !important;
    }
    
    .hero-box {
        background: linear-gradient(135deg, #09381c 0%, #15733b 100%);
        padding: 50px 30px;
        border-radius: 18px;
        text-align: center;
        box-shadow: 0 12px 30px rgba(13, 75, 38, 0.25);
        margin-bottom: 25px;
    }
    .hero-title {
        font-size: 36px;
        font-weight: 700;
        color: #ffffff !important;
        margin-bottom: 10px;
    }
    .hero-subtitle {
        font-size: 16px;
        color: #d1fae5 !important;
        max-width: 780px;
        margin: 0 auto;
    }
    
    .vehicle-card {
        background: #ffffff;
        border-radius: 18px;
        padding: 22px;
        text-align: center;
        box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        border: 2px solid #e2e8f0;
        transition: all 0.35s ease;
        margin-bottom: 20px;
    }
    .vehicle-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 18px 38px rgba(13, 75, 38, 0.22);
        border-color: #0d4b26;
    }
    .vehicle-img-3d {
        width: 150px;
        height: 150px;
        object-fit: contain;
        filter: drop-shadow(0 14px 16px rgba(0,0,0,0.25));
        margin: 10px auto;
        display: block;
        transition: transform 0.4s ease;
    }
    .vehicle-card:hover .vehicle-img-3d {
        transform: scale(1.15) rotate(-4deg);
    }
    .badge-scheme {
        background-color: #dcfce7;
        color: #166534 !important;
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 8px;
    }
    .price-tag {
        font-size: 22px;
        font-weight: 700;
        color: #0d4b26 !important;
        margin: 8px 0;
    }
    
    div[data-testid="stPopover"] {
        position: fixed;
        bottom: 25px;
        right: 25px;
        z-index: 9999;
    }
    div[data-testid="stPopover"] > button {
        background-color: #0d4b26 !important;
        color: #ffffff !important;
        border-radius: 50px !important;
        padding: 14px 24px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        box-shadow: 0 8px 25px rgba(13, 75, 38, 0.45) !important;
        border: 2px solid #ffffff !important;
    }
    
    .footer {
        background-color: #09381c;
        padding: 25px;
        border-radius: 14px;
        text-align: center;
        margin-top: 40px;
    }
    .footer p, .footer b {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD MODELS & DATASET
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
    dl_model = load_model("dl_vehicle_model.h5", compile=False)
    return df, scaler, le_fuel, le_usage, le_target, xgb_model, dl_model

df, scaler, le_fuel, le_usage, le_target, xgb_model, dl_model = load_assets()

@st.cache_data(ttl=3600)
def get_live_market_rates(query):
    try:
        with DDGS() as ddgs:
            return list(ddgs.text(query, max_results=3))
    except Exception:
        return []

# ==========================================
# TOP NAVBAR & HERO SECTION
# ==========================================
st.markdown("""
<div class="navbar">
    <div class="nav-logo">🚘 PakDrive AI <span style="font-size:14px; color:#15803d !important;">| 3D Vehicle & Scheme Portal</span></div>
    <div style="font-size:14px; font-weight:500;">Cycle to Helicopter • Electric vs Petrol • Punjab E-Bike Scheme</div>
</div>

<div class="hero-box">
    <div class="hero-title">DISCOVER YOUR PERFECT RIDE IN PAKISTAN</div>
    <div class="hero-subtitle">
        Cycle se lekar Helicopter tak — Apna budget select karein aur foran 3D Vehicles, Taza Market Rates, Electric vs Petrol Comparison, aur Maryam Nawaz Punjab E-Bike Scheme ki tafseel dekhein.
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# USER INPUT PANEL
# ==========================================
st.markdown("### 🔍 Apni Zaroorat Aur Budget Select Karein")
c1, c2, c3, c4 = st.columns(4)
with c1:
    budget = st.number_input("Aapka Budget (PKR)", min_value=15000, max_value=1500000000, value=185000, step=10000)
with c2:
    daily_km = st.slider("Rozana ka Safar (KM)", min_value=2, max_value=500, value=35)
with c3:
    fuel_pref = st.selectbox("Fuel / Power Type", ["Any (Show All)", "Electric", "Petrol", "Manual", "Diesel", "Aviation Fuel"])
with c4:
    usage_type = st.selectbox("Istemaal (Purpose)", ["Personal", "Family", "Commercial", "Luxury/Offroad", "Marine/Leisure", "Aviation"])

st.button("🚀 Show 3D Vehicles, Rates & Comparison", use_container_width=True, type="primary")

# ==========================================
# ML & DL PREDICTION
# ==========================================
selected_fuel = "Electric" if fuel_pref == "Any (Show All)" else fuel_pref
if selected_fuel not in le_fuel.classes_:
    selected_fuel = le_fuel.classes_
if usage_type not in le_usage.classes_:
    usage_type = le_usage.classes_

fuel_enc = le_fuel.transform([selected_fuel])
usage_enc = le_usage.transform([usage_type])
passengers = 1 if budget < 150000 else (2 if budget < 500000 else 5)

input_data = np.array([[np.log1p(budget), daily_km, passengers, fuel_enc, usage_enc]])
input_scaled = scaler.transform(input_data)

dl_probs = dl_model.predict(input_scaled, verbose=0)
dl_pred_idx = int(np.argmax(dl_probs))
dl_confidence = float(dl_probs[dl_pred_idx] * 100)
predicted_category = str(le_target.inverse_transform([dl_pred_idx])).split('_', 1)[-1]

xgb_pred_idx = int(xgb_model.predict(input_scaled))
xgb_category = str(le_target.inverse_transform([xgb_pred_idx])).split('_', 1)[-1]

st.success(f"🧠 **Deep Learning Prediction:** `{predicted_category}` (Confidence: **{dl_confidence:.1f}%**)  |  🚀 **XGBoost ML Prediction:** `{xgb_category}`")

# ==========================================
# FILTER & DISPLAY 3D VEHICLE CARDS
# ==========================================
unique_vehicles = df.drop_duplicates(subset=["Model_Name"]).copy()
if fuel_pref != "Any (Show All)":
    filtered = unique_vehicles[unique_vehicles["Fuel_Type"] == fuel_pref].copy()
    if filtered.empty:
        filtered = unique_vehicles.copy()
else:
    filtered = unique_vehicles.copy()

filtered["Price_Diff"] = abs(filtered["Price_PKR"] - budget)
matched_df = filtered.sort_values("Price_Diff").head(4)

st.markdown("### 🏆 Aapke Budget Ke Mutabiq 3D Vehicles & Latest Rates")
cols = st.columns(len(matched_df))

for idx, (_, row) in enumerate(matched_df.iterrows()):
    with cols[idx]:
        scheme_text = str(row["Govt_Scheme"])
        if "Yes" in scheme_text:
            badge = f'<div class="badge-scheme">🏛️ {scheme_text}</div>'
        else:
            badge = '<div class="badge-scheme" style="background:#e2e8f0; color:#334155 !important;">Standard Market Rate</div>'
        
        price_formatted = f"{int(row['Price_PKR']):,}"
        html_parts = [
            '<div class="vehicle-card">',
            badge,
            f'<img src="{row["Image_3D_URL"]}" class="vehicle-img-3d">',
            f'<h4 style="margin:6px 0; font-weight:700;">{row["Model_Name"]}</h4>',
            f'<div style="font-size:13px; color:#475569 !important;">{row["Fuel_Type"]} • Range: {row["Max_Range_KM"]} km</div>',
            f'<div class="price-tag">Rs. {price_formatted}</div>',
            f'<div style="font-size:12px; color:#0f766e !important; font-weight:600;">Kharcha: Rs. {row["Running_Cost_Per_100km"]} / 100km</div>',
            '<hr style="margin:12px 0; border-color:#e2e8f0;">',
            '<div style="text-align:left; font-size:12.5px;">',
            f'<p style="color:#15803d !important; margin-bottom:6px;"><b>✅ Advantages:</b> {row["Advantages"]}</p>',
            f'<p style="color:#b91c1c !important; margin-bottom:0;"><b>❌ Disadvantages:</b> {row["Disadvantages"]}</p>',
            '</div></div>'
        ]
        st.markdown("".join(html_parts), unsafe_allow_html=True)

# ==========================================
# LIVE PAKWHEELS & PUNJAB SCHEME UPDATES
# ==========================================
st.markdown("### 🌐 Live PakWheels & Punjab Govt E-Bike Scheme Updates")
top_vehicle = str(matched_df.iloc["Model_Name"])
