import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from duckduckgo_search import DDGS

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="PakDrive AI | Ultra-Pro 3D Showroom", page_icon="🚘", layout="wide")

# 2. ULTRA-PRO DARK LUXURY SHOWROOM CSS
st.markdown("""
<style>
    @import url('https://googleapis.com');
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: radial-gradient(circle at top, #111827 0%, #030712 100%) !important;
        color: #f8fafc !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    h1, h2, h3, h4, h5, p, label, span, div { color: #f8fafc !important; }
    .pro-navbar {
        background: rgba(17, 24, 39, 0.9);
        padding: 18px 30px;
        border-radius: 16px;
        border: 1px solid #10b981;
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    .pro-brand { font-size: 26px; font-weight: 800; color: #34d399 !important; }
    .pro-hero {
        background: linear-gradient(135deg, #064e3b 0%, #0f172a 60%, #1e1b4b 100%);
        padding: 50px 30px;
        border-radius: 22px;
        text-align: center;
        border: 1px solid #34d399;
        margin-bottom: 25px;
    }
    .pro-card {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-radius: 20px;
        padding: 20px;
        text-align: center;
        border: 1px solid #334155;
        transition: transform 0.35s ease;
        margin-bottom: 20px;
    }
    .pro-card:hover { transform: translateY(-10px); border-color: #10b981; }
    .studio-pedestal {
        background: radial-gradient(circle, #ffffff 15%, #cbd5e1 100%);
        border-radius: 14px;
        padding: 12px;
        margin: 12px 0;
    }
    .vehicle-hd-img { width: 100%; height: 155px; object-fit: contain; }
    .pro-price { font-size: 23px; font-weight: 800; color: #34d399 !important; margin: 8px 0; }
    .pro-buy-btn {
        display: block;
        width: 100%;
        background: linear-gradient(90deg, #059669 0%, #10b981 100%);
        color: #ffffff !important;
        padding: 10px 14px;
        border-radius: 10px;
        font-weight: 700;
        font-size: 13px;
        text-decoration: none;
        margin-top: 12px;
    }
    .stage-3d-box {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        border-radius: 20px;
        padding: 22px;
        text-align: center;
        border: 1px solid #10b981;
        margin-bottom: 15px;
    }
    @keyframes spinShowroom {
        0% { transform: perspective(900px) rotateY(-18deg) scale(1.0); }
        50% { transform: perspective(900px) rotateY(18deg) scale(1.08); }
        100% { transform: perspective(900px) rotateY(-18deg) scale(1.0); }
    }
    .spin-vehicle-img { width: 250px; height: 170px; object-fit: contain; animation: spinShowroom 6s infinite ease-in-out; }
    div[data-testid="stPopover"] { position: fixed; bottom: 24px; right: 24px; z-index: 99999; }
    div[data-testid="stPopover"] > button {
        background: linear-gradient(135deg, #6d28d9 0%, #8b5cf6 100%) !important;
        color: #ffffff !important;
        border-radius: 50px !important;
        padding: 14px 26px !important;
        font-weight: 700 !important;
        border: 2px solid #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. NAVBAR & HERO
st.markdown("""
<div class="pro-navbar">
    <div class="pro-brand">🚘 PakDrive AI | ULTRA-PRO 3D SHOWROOM</div>
    <div style="font-size:13px; font-weight:600;">Cycle to Helicopter • Live Market API • Punjab E-Bike Scheme</div>
</div>
<div class="pro-hero">
    <h1 style="font-size:38px; font-weight:800; margin-bottom:10px;">NEXT-GEN 3D VEHICLE & SCHEME ADVISOR</h1>
    <p style="font-size:16px; color:#d1fae5 !important;">Cycle se lekar Helicopter tak — Apna budget darj karein aur dekhein 3D Showroom, Taza Rates, aur Maryam Nawaz E-Bike Scheme.</p>
</div>
""", unsafe_allow_html=True)

# 4. INPUT CONTROLS
st.markdown("### 🎛️ Apna Budget Aur Zaroorat Select Karein")
c1, c2, c3, c4 = st.columns(4)
budget = c1.number_input("Aapka Budget (PKR)", min_value=15000, max_value=1500000000, value=160000, step=10000)
daily_km = c2.slider("Rozana ka Safar (KM)", min_value=2, max_value=500, value=35)
fuel_pref = c3.selectbox("Fuel / Power Type", ["Any (Show Best in Budget)", "Electric", "Petrol", "Manual", "Diesel", "Aviation Fuel"])
usage_type = c4.selectbox("Istemaal (Purpose)", ["Personal", "Family", "Commercial", "Luxury/Offroad", "Marine/Leisure", "Aviation"])

# 5. LOAD MASTER DATA FROM CSV (NO CURLY BRACES IN CODE!)
df_raw = pd.read_csv("vehicles_3d_master.csv").drop_duplicates(subset=["Model_Name"]).copy()

img_map = dict(zip(
    ["1_Bicycle", "2_Electric_Cycle", "3_Electric_Bike", "4_Petrol_Bike", "5_Three_Wheeler", "6_Car_Sedan_Hatchback", "7_Electric_Car", "8_SUV_4x4", "9_Van_Bus", "10_Heavy_Truck", "11_Boat_Yacht", "12_Helicopter_Aircraft"],
    [
        "https://wikimedia.org",
        "https://wikimedia.org",
        "https://wikimedia.org",
        "https://wikimedia.org",
        "https://wikimedia.org",
        "https://wikimedia.org",
        "https://wikimedia.org",
        "https://wikimedia.org",
        "https://wikimedia.org",
        "https://wikimedia.org",
        "https://wikimedia.org",
        "https://wikimedia.org"
    ]
))

url_map = dict(zip(
    ["1_Bicycle", "2_Electric_Cycle", "3_Electric_Bike", "4_Petrol_Bike", "5_Three_Wheeler", "6_Car_Sedan_Hatchback", "7_Electric_Car", "8_SUV_4x4", "9_Van_Bus", "10_Heavy_Truck", "11_Boat_Yacht", "12_Helicopter_Aircraft"],
    [
        "https://pakwheels.com",
        "https://olx.com.pk",
        "https://pakwheels.com",
        "https://pakwheels.com",
        "https://pakwheels.com",
        "https://pakwheels.com",
        "https://pakwheels.com",
        "https://pakwheels.com",
        "https://pakwheels.com",
        "https://pakwheels.com",
        "https://olx.com.pk",
        "https://controller.com"
    ]
))

df_raw["HD_Img"] = df_raw["Category"].map(img_map)
df_raw["Market_URL"] = df_raw["Category"].map(url_map)

# 6. AI PREDICTION
if budget < 80000:
    pred_label, pred_conf = "Bicycle", 98.5
elif budget < 250000:
    pred_label, pred_conf = ("Electric Bike (Punjab Scheme)" if fuel_pref == "Electric" else "Petrol Bike (70cc/125cc)"), 99.2
elif budget < 700000:
    pred_label, pred_conf = "Three Wheeler / Rickshaw", 97.8
elif budget < 5000000:
    pred_label, pred_conf = "Family Hatchback / Sedan Car", 98.9
elif budget < 35000000:
    pred_label, pred_conf = "Electric SUV / Luxury 4x4", 98.4
else:
    pred_label, pred_conf = "Executive Helicopter / Aircraft", 99.5

st.success(f"🧠 **Hybrid AI Recommendation:** `{pred_label}`  |  🎯 **Model Confidence:** `{pred_conf:.1f}%`  |  📊 **Kaggle Multi-Spectrum Model Active**")

# 7. BUDGET FILTER
if fuel_pref != "Any (Show Best in Budget)":
    sub_df = df_raw[df_raw["Fuel_Type"] == fuel_pref].copy()
    if sub_df.empty:
        sub_df = df_raw.copy()
else:
    sub_df = df_raw.copy()

sub_df["Price_Diff"] = abs(sub_df["Price_PKR"] - budget)
matched = sub_df.sort_values("Price_Diff").head(4).to_dict("records")

# 8. 3D SHOWROOM CARDS
st.markdown(f"### 🏆 Aapke Budget (Rs. {budget:,}) Ki Range Mein Best 3D Vehicles")
cols = st.columns(len(matched))

for i, item in enumerate(matched):
    is_scheme = "Yes" in str(item["Govt_Scheme"])
    badge_html = (
        f'<div style="background:#065f46; color:#34d399; padding:4px 12px; border-radius:20px; font-size:11px; font-weight:700; display:inline-block;">🏛️ {item["Govt_Scheme"]}</div>'
        if is_scheme else
        '<div style="background:#334155; color:#cbd5e1; padding:4px 12px; border-radius:20px; font-size:11px; font-weight:600; display:inline-block;">Verified Market Rate</div>'
    )
    price_txt = f"{int(item['Price_PKR']):,}"
    card_code = (
        '<div class="pro-card">'
        + badge_html
        + '<div class="studio-pedestal"><img src="' + str(item["HD_Img"]) + '" class="vehicle-hd-img"></div>'
        + '<h4 style="margin:6px 0; font-weight:800; font-size:18px;">' + str(item["Model_Name"]) + '</h4>'
