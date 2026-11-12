import streamlit as st
import pandas as pd
import numpy as np
import joblib
from xgboost import XGBClassifier
from tensorflow.keras.models import load_model
from duckduckgo_search import DDGS

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="PakDrive AI | Luxury 3D Vehicle Showroom",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. LUXURY SHOWROOM CSS & FLOATING CHATBOT
# ==========================================
st.markdown("""
<style>
    @import url('https://googleapis.com');
    
    .stApp {
        background: linear-gradient(180deg, #f1f5f9 0%, #ffffff 50%, #f8fafc 100%) !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    .lux-navbar {
        background: #ffffff;
        padding: 16px 30px;
        border-radius: 16px;
        box-shadow: 0 6px 25px rgba(15, 23, 42, 0.08);
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        border-bottom: 4px solid #059669;
    }
    .lux-brand {
        font-size: 26px;
        font-weight: 800;
        color: #064e3b;
    }
    
    .showroom-hero {
        background: radial-gradient(circle at 50% 20%, #1e293b 0%, #090d16 100%);
        padding: 48px 30px;
        border-radius: 22px;
        text-align: center;
        box-shadow: 0 18px 40px rgba(9, 13, 22, 0.3);
        margin-bottom: 25px;
    }
    .showroom-title {
        font-size: 36px;
        font-weight: 800;
        color: #ffffff !important;
        margin-bottom: 10px;
    }
    .showroom-sub {
        font-size: 16px;
        color: #cbd5e1 !important;
        max-width: 780px;
        margin: 0 auto;
    }
    
    .lux-card {
        background: #ffffff;
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
        border: 1px solid #e2e8f0;
        transition: transform 0.35s ease, box-shadow 0.35s ease;
        margin-bottom: 20px;
    }
    .lux-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 22px 45px rgba(5, 150, 105, 0.22);
        border-color: #059669;
    }
    .studio-stage {
        background: radial-gradient(circle, #ffffff 0%, #e2e8f0 100%);
        border-radius: 16px;
        padding: 12px;
        margin: 12px 0;
        border: 1px solid #cbd5e1;
    }
    .vehicle-3d-photo {
        width: 100%;
        height: 160px;
        object-fit: contain;
        filter: drop-shadow(0 15px 15px rgba(0,0,0,0.25));
        transition: transform 0.4s ease;
    }
    .lux-card:hover .vehicle-3d-photo {
        transform: scale(1.1) rotate(-2deg);
    }
    .lux-price {
        font-size: 23px;
        font-weight: 800;
        color: #064e3b;
        margin: 8px 0;
    }
    .buy-btn {
        display: block;
        width: 100%;
        background: linear-gradient(90deg, #064e3b 0%, #059669 100%);
        color: #ffffff !important;
        padding: 10px 14px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 13px;
        text-decoration: none;
        margin-top: 12px;
        box-shadow: 0 6px 15px rgba(5, 150, 105, 0.3);
    }
    
    .video-3d-stage {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 15px 35px rgba(15, 23, 42, 0.25);
        margin-bottom: 15px;
    }
    @keyframes spin3dShowroom {
        0% { transform: perspective(900px) rotateY(-16deg) scale(1.0); }
        50% { transform: perspective(900px) rotateY(16deg) scale(1.08); }
        100% { transform: perspective(900px) rotateY(-16deg) scale(1.0); }
    }
    .rotating-3d-vehicle {
        width: 260px;
        height: 175px;
        object-fit: contain;
        animation: spin3dShowroom 6s infinite ease-in-out;
        filter: drop-shadow(0 20px 25px rgba(16, 185, 129, 0.35));
    }
    
    div[data-testid="stPopover"] {
        position: fixed;
        bottom: 24px;
        right: 24px;
        z-index: 99999;
    }
    div[data-testid="stPopover"] > button {
        background: linear-gradient(135deg, #5b21b6 0%, #7c3aed 100%) !important;
        color: #ffffff !important;
        border-radius: 50px !important;
        padding: 14px 26px !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        box-shadow: 0 10px 28px rgba(124, 58, 237, 0.45) !important;
        border: 2px solid #ffffff !important;
    }
    .chat-header-card {
        background: linear-gradient(135deg, #5b21b6 0%, #7c3aed 100%);
        padding: 16px;
        border-radius: 14px;
        text-align: center;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. VERIFIED VEHICLE IMAGES & MARKET LINKS
# ==========================================
VEHICLE_MEDIA = {
    "1_Bicycle": {
        "img": "https://wikimedia.org",
        "url": "https://pakwheels.com"
    },
    "2_Electric_Cycle": {
        "img": "https://wikimedia.org",
        "url": "https://olx.com.pk"
    },
    "3_Electric_Bike": {
        "img": "https://wikimedia.org",
        "url": "https://pakwheels.com"
    },
    "4_Petrol_Bike": {
        "img": "https://wikimedia.org",
        "url": "https://pakwheels.com"
    },
    "5_Three_Wheeler": {
        "img": "https://wikimedia.org",
        "url": "https://pakwheels.com"
    },
    "6_Car_Sedan_Hatchback": {
        "img": "https://wikimedia.org",
        "url": "https://pakwheels.com"
    },
    "7_Electric_Car": {
        "img": "https://wikimedia.org",
        "url": "https://pakwheels.com"
    },
    "8_SUV_4x4": {
        "img": "https://wikimedia.org",
        "url": "https://pakwheels.com"
    },
    "9_Van_Bus": {
        "img": "https://wikimedia.org",
        "url": "https://pakwheels.com"
    },
    "10_Heavy_Truck": {
        "img": "https://wikimedia.org",
        "url": "https://pakwheels.com"
    },
    "11_Boat_Yacht": {
        "img": "https://wikimedia.org",
        "url": "https://olx.com.pk"
    },
    "12_Helicopter_Aircraft": {
        "img": "https://wikimedia.org",
        "url": "https://controller.com"
    }
}

# ==========================================
# 4. LOAD MODELS & DATASET
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

@st.cache_data(ttl=1800)
def fetch_live_market_data(query):
    try:
        with DDGS() as ddgs:
            return list(ddgs.text(query, max_results=3))
    except Exception:
        return []

# ==========================================
# 5. LUXURY NAVBAR & HERO SECTION
# ==========================================
st.markdown("""
<div class="lux-navbar">
    <div class="lux-brand">🚘 PakDrive AI <span style="font-size:13px; color:#475569;">| LUXURY 3D SHOWROOM</span></div>
    <div style="font-size:14px; font-weight:600; color:#0f172a;">Cycle to Helicopter • Live PakWheels API • Maryam Nawaz E-Bike Scheme</div>
</div>

<div class="showroom-hero">
    <div class="showroom-title">EXPERIENCE LUXURY & SMART MOBILITY</div>
    <div class="showroom-sub">
        Apna budget darj karein — Hamara Deep Learning aur XGBoost AI aapke budget ki exact range mein behtareen sawari, 3D Showroom Tour, Live Market Links, aur Punjab Govt Scheme ki mukammal tafseel dikhayega.
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 6. USER INPUT PANEL (NO INDENTATION BLOCKS!)
# ==========================================
st.markdown("### 🔍 Apna Budget Aur Zaroorat Select Karein")
c1, c2, c3, c4 = st.columns(4)
