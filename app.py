import streamlit as st
import pandas as pd
import numpy as np
import joblib
import urllib.parse
from xgboost import XGBClassifier
from tensorflow.keras.models import load_model
from duckduckgo_search import DDGS

# ==========================================
# PAGE CONFIGURATION (LUXURY SHOWROOM THEME)
# ==========================================
st.set_page_config(
    page_title="PakDrive AI | Luxury 3D Vehicle & Scheme Showroom",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Luxury Studio Showroom CSS + Superior-Style Floating Chatbot
st.markdown("""
<style>
    @import url('https://googleapis.com');
    
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: linear-gradient(180deg, #eef2f3 0%, #ffffff 45%, #f1f5f9 100%) !important;
        color: #0f172a !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    h1, h2, h3, h4, h5, p, label, span {
        color: #0f172a !important;
    }
    
    /* Luxury Glass Navbar */
    .lux-navbar {
        background: rgba(255, 255, 255, 0.92);
        backdrop-filter: blur(12px);
        padding: 18px 35px;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(15, 23, 42, 0.08);
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 22px;
        border: 1px solid rgba(255,255,255,0.8);
    }
    .lux-brand {
        font-size: 26px;
        font-weight: 800;
        background: linear-gradient(90deg, #064e3b, #059669);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Showroom Studio Hero Banner */
    .showroom-hero {
        background: radial-gradient(circle at 50% 20%, #1e293b 0%, #090d16 100%);
        padding: 55px 35px;
        border-radius: 22px;
        text-align: center;
        box-shadow: 0 20px 50px rgba(9, 13, 22, 0.35);
        margin-bottom: 28px;
        border: 1px solid #334155;
    }
    .showroom-title {
        font-size: 38px;
        font-weight: 800;
        color: #ffffff !important;
        letter-spacing: -0.5px;
        margin-bottom: 10px;
    }
    .showroom-sub {
        font-size: 16px;
        color: #cbd5e1 !important;
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Luxury 3D Vehicle Card */
    .lux-card {
        background: #ffffff;
        border-radius: 22px;
        padding: 22px;
        text-align: center;
        box-shadow: 0 12px 35px rgba(15, 23, 42, 0.08);
        border: 1px solid #e2e8f0;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin-bottom: 22px;
        position: relative;
        overflow: hidden;
    }
    .lux-card:hover {
        transform: translateY(-12px);
        box-shadow: 0 25px 50px rgba(6, 78, 59, 0.22);
        border-color: #059669;
    }
    .studio-stage {
        background: radial-gradient(circle, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 16px;
        padding: 15px;
        margin: 12px 0;
        border: 1px solid #cbd5e1;
    }
    .vehicle-3d-photo {
        width: 100%;
        height: 165px;
        object-fit: contain;
        filter: drop-shadow(0 18px 18px rgba(0,0,0,0.28));
        transition: transform 0.5s ease;
    }
    .lux-card:hover .vehicle-3d-photo {
        transform: scale(1.12) rotate(-2deg);
    }
    .lux-price {
        font-size: 24px;
        font-weight: 800;
        color: #064e3b !important;
        margin: 8px 0;
    }
    .buy-btn {
        display: inline-block;
        width: 100%;
        background: linear-gradient(90deg, #064e3b 0%, #059669 100%);
        color: #ffffff !important;
        padding: 11px 16px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 13.5px;
        text-decoration: none;
        margin-top: 12px;
        box-shadow: 0 6px 15px rgba(5, 150, 105, 0.3);
        transition: opacity 0.3s ease;
    }
    .buy-btn:hover {
        opacity: 0.9;
        color: #ffffff !important;
    }
    
    /* 3D Rotating Video Showcase Box */
    .video-3d-stage {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border-radius: 20px;
        padding: 25px;
        color: white;
        box-shadow: 0 15px 35px rgba(15, 23, 42, 0.25);
        border: 1px solid #334155;
    }
    @keyframes spin3dShowroom {
        0% { transform: perspective(900px) rotateY(-18deg) scale(1.0); }
        50% { transform: perspective(900px) rotateY(18deg) scale(1.08); }
        100% { transform: perspective(900px) rotateY(-18deg) scale(1.0); }
    }
    .rotating-3d-vehicle {
        width: 260px;
        height: 180px;
        object-fit: contain;
        animation: spin3dShowroom 6s infinite ease-in-out;
        filter: drop-shadow(0 22px 25px rgba(16, 185, 129, 0.35));
    }
    
    /* Superior University Style Floating Corner Chatbot */
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
        padding: 18px;
        border-radius: 14px;
        text-align: center;
        margin-bottom: 12px;
    }
    .chat-header-card h4, .chat-header-card p {
        color: #ffffff !important;
        margin: 2px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# VERIFIED HIGH-RES VEHICLE IMAGES & MARKET LINKS
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
# LOAD TRAINED MODELS & DATASET
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

# Free Built-in Market API (DuckDuckGo Live Search)
@st.cache_data(ttl=1800)
def fetch_live_market_data(query):
    try:
        with DDGS() as ddgs:
            return list(ddgs.text(query, max_results=3))
    except Exception:
        return []

# ==========================================
# LUXURY NAVBAR & SHOWROOM HERO
