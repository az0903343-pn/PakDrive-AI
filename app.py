import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from duckduckgo_search import DDGS

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="PakDrive AI | Ultra-Pro 3D Luxury Showroom",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. ULTRA-PRO DARK OBSIDIAN & GOLD LUXURY CSS
# ==========================================
st.markdown("""
<style>
    @import url('https://googleapis.com');
    
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: radial-gradient(circle at top, #111827 0%, #030712 100%) !important;
        color: #f8fafc !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    h1, h2, h3, h4, h5, p, label, span, div {
        color: #f8fafc !important;
    }
    
    .pro-navbar {
        background: rgba(17, 24, 39, 0.85);
        backdrop-filter: blur(16px);
        padding: 18px 32px;
        border-radius: 18px;
        border: 1px solid rgba(16, 185, 129, 0.35);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24px;
    }
    .pro-brand {
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(90deg, #10b981, #34d399, #fbbf24);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .pro-hero {
        background: linear-gradient(135deg, #064e3b 0%, #0f172a 55%, #1e1b4b 100%);
        padding: 55px 35px;
        border-radius: 24px;
        text-align: center;
        border: 1px solid rgba(52, 211, 153, 0.4);
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.65);
        margin-bottom: 30px;
    }
    .pro-hero-title {
        font-size: 40px;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #ffffff !important;
        margin-bottom: 12px;
        text-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    .pro-hero-sub {
        font-size: 16px;
        color: #d1fae5 !important;
        max-width: 820px;
        margin: 0 auto;
        line-height: 1.6;
    }
    
    .pro-card {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-radius: 22px;
        padding: 22px;
        text-align: center;
        border: 1px solid rgba(148, 163, 184, 0.25);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.5);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin-bottom: 22px;
    }
    .pro-card:hover {
        transform: translateY(-12px) scale(1.02);
        border-color: #10b981;
        box-shadow: 0 25px 55px rgba(16, 185, 129, 0.3);
    }
    .studio-pedestal {
        background: radial-gradient(circle, #ffffff 10%, #cbd5e1 100%);
        border-radius: 16px;
        padding: 14px;
        margin: 14px 0;
        box-shadow: inset 0 -10px 20px rgba(0,0,0,0.15);
    }
    .vehicle-hd-img {
        width: 100%;
        height: 165px;
        object-fit: contain;
        filter: drop-shadow(0 16px 16px rgba(0,0,0,0.35));
        transition: transform 0.45s ease;
    }
    .pro-card:hover .vehicle-hd-img {
        transform: scale(1.12) rotate(-2deg);
    }
    .pro-price {
        font-size: 24px;
        font-weight: 800;
        color: #34d399 !important;
        margin: 8px 0;
    }
    .pro-buy-btn {
        display: block;
        width: 100%;
        background: linear-gradient(90deg, #059669 0%, #10b981 100%);
        color: #ffffff !important;
        padding: 11px 16px;
        border-radius: 12px;
        font-weight: 700;
        font-size: 13.5px;
        text-decoration: none;
        margin-top: 14px;
        box-shadow: 0 8px 20px rgba(16, 185, 129, 0.35);
    }
    .pro-buy-btn:hover {
        opacity: 0.92;
        color: #ffffff !important;
    }
    
    .stage-3d-box {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        border-radius: 22px;
        padding: 25px;
        text-align: center;
        border: 1px solid rgba(16, 185, 129, 0.4);
        box-shadow: 0 20px 45px rgba(0,0,0,0.55);
        margin-bottom: 16px;
    }
    @keyframes spinShowroom {
        0% { transform: perspective(900px) rotateY(-18deg) scale(1.0); }
        50% { transform: perspective(900px) rotateY(18deg) scale(1.08); }
        100% { transform: perspective(900px) rotateY(-18deg) scale(1.0); }
    }
    .spin-vehicle-img {
        width: 270px;
        height: 180px;
        object-fit: contain;
        animation: spinShowroom 6s infinite ease-in-out;
        filter: drop-shadow(0 22px 28px rgba(16, 185, 129, 0.45));
    }
    
    div[data-testid="stPopover"] {
        position: fixed;
        bottom: 24px;
        right: 24px;
        z-index: 99999;
    }
    div[data-testid="stPopover"] > button {
        background: linear-gradient(135deg, #6d28d9 0%, #8b5cf6 100%) !important;
        color: #ffffff !important;
        border-radius: 50px !important;
        padding: 15px 28px !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        box-shadow: 0 12px 30px rgba(139, 92, 246, 0.55) !important;
        border: 2px solid #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. NAVBAR & HERO SECTION
# ==========================================
st.markdown("""
<div class="pro-navbar">
    <div class="pro-brand">🚘 PakDrive AI <span style="font-size:13px; color:#94a3b8; -webkit-text-fill-color:#94a3b8;">| ULTRA-PRO 3D SHOWROOM</span></div>
    <div style="font-size:13.5px; font-weight:600; color:#cbd5e1;">Cycle to Helicopter • Live Market API • Maryam Nawaz E-Bike Scheme</div>
</div>

<div class="pro-hero">
    <div class="pro-hero-title">NEXT-GEN 3D VEHICLE & SCHEME ADVISOR</div>
    <div class="pro-hero-sub">
        Cycle se lekar Helicopter tak — Apna budget darj karein aur dekhein Ultra-HD 3D Showroom, Taza Market Rates, Electric vs Petrol Comparison, aur Maryam Nawaz Punjab E-Bike Scheme ki mukammal tafseel.
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 4. USER INPUT CONTROLS
# ==========================================
st.markdown("### 🎛️ Apna Budget Aur Zaroorat Select Karein")
c1, c2, c3, c4 = st.columns(4)
budget = c1.number_input("Aapka Budget (PKR)", min_value=15000, max_value=1500000000, value=160000, step=10000)
daily_km = c2.slider("Rozana ka Safar (KM)", min_value=2, max_value=500, value=35)
fuel_pref = c3.selectbox("Fuel / Power Type", ["Any (Show Best in Budget)", "Electric", "Petrol", "Manual", "Diesel", "Aviation Fuel"])
usage_type = c4.selectbox("Istemaal (Purpose)", ["Personal", "Family", "Commercial", "Luxury/Offroad", "Marine/Leisure", "Aviation"])

# ==========================================
# 5. BUILT-IN MASTER CATALOG
# ==========================================
CATALOG = [
    {
        "Model_Name": "Sohrab Classic Bicycle",
        "Category": "Bicycle",
        "Fuel_Type": "Manual",
        "Price_PKR": 22000,
        "Running_Cost": 0,
        "Range_KM": 15,
        "Govt_Scheme": "Standard Market",
        "Advantages": "Zero petrol kharcha, sehat ke liye behtareen, kisi license ki zaroorat nahi.",
        "Disadvantages": "Raftaar kam hai aur lambay safar mein thakawat hoti hai.",
        "Img": "https://wikimedia.org",
        "Link": "https://pakwheels.com"
    },
    {
        "Model_Name": "Smart E-Bicycle 350W",
        "Category": "Electric Cycle",
        "Fuel_Type": "Electric",
        "Price_PKR": 115000,
        "Running_Cost": 80,
        "Range_KM": 45,
        "Govt_Scheme": "Standard Market",
        "Advantages": "Pedal aur electric motor dono options, charging kharcha na hone ke barabar.",
        "Disadvantages": "Top speed 30 km/h tak mehdood hai.",
        "Img": "https://wikimedia.org",
        "Link": "https://olx.com.pk"
    },
    {
        "Model_Name": "Honda CD 70 (2026 Model)",
        "Category": "Petrol Bike",
        "Fuel_Type": "Petrol",
        "Price_PKR": 157900,
        "Running_Cost": 1800,
        "Range_KM": 55,
        "Govt_Scheme": "Yes (Punjab Petrol Bike Quota)",
        "Advantages": "Pakistan mein sab se mazboot resale value, har gali mein mechanic aur saste parts.",
        "Disadvantages": "Mehngay petrol ki wajah se mahana Rs. 8,000+ kharcha aata hai.",
        "Img": "https://wikimedia.org",
        "Link": "https://pakwheels.com"
    },
    {
        "Model_Name": "Jolta JE-70L (Punjab E-Bike)",
        "Category": "Electric Bike",
        "Fuel_Type": "Electric",
        "Price_PKR": 185000,
        "Running_Cost": 120,
        "Range_KM": 80,
        "Govt_Scheme": "Yes (Maryam Nawaz E-Bike Scheme)",
        "Advantages": "Students ke liye bina sood (0% markup) asaan aqsaat, Rs. 120 mein 100 km safar.",
        "Disadvantages": "Full charge hone mein 5-6 ghantay lagtay hain, 80 km range limit.",
        "Img": "https://wikimedia.org",
        "Link": "https://pakwheels.com"
    },
    {
        "Model_Name": "Sazgar Electric Rickshaw",
        "Category": "Three Wheeler",
        "Fuel_Type": "Electric",
        "Price_PKR": 550000,
        "Running_Cost": 350,
        "Range_KM": 100,
        "Govt_Scheme": "Yes (Green Transport Subsidy)",
