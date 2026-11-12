import streamlit as st
import pandas as pd
import numpy as np
from duckduckgo_search import DDGS

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="PakDrive AI | Ultra-Pro 3D Vehicle Showroom",
    page_icon="🚘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. ULTRA-PRO LUXURY DARK SHOWROOM THEME CSS
# ==========================================
st.markdown("""
<style>
    @import url('https://googleapis.com');
    
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: radial-gradient(circle at top, #111827 0%, #030712 100%) !important;
        color: #f8fafc !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1b4b 0%, #0f172a 100%) !important;
        border-right: 2px solid #7c3aed !important;
    }
    
    h1, h2, h3, h4, h5, p, label, span {
        color: #f8fafc !important;
    }
    
    .pro-hero {
        background: linear-gradient(135deg, #064e3b 0%, #0f172a 55%, #1e1b4b 100%);
        padding: 40px 30px;
        border-radius: 20px;
        text-align: center;
        border: 1px solid #10b981;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6);
        margin-bottom: 24px;
    }
    
    @keyframes spin3d {
        0% { transform: perspective(900px) rotateY(-15deg) scale(1.0); }
        50% { transform: perspective(900px) rotateY(15deg) scale(1.06); }
        100% { transform: perspective(900px) rotateY(-15deg) scale(1.0); }
    }
    .showcase-3d-img {
        width: 100%;
        max-height: 240px;
        object-fit: contain;
        border-radius: 14px;
        background: radial-gradient(circle, #ffffff 20%, #cbd5e1 100%);
        padding: 15px;
        animation: spin3d 6s infinite ease-in-out;
        box-shadow: 0 15px 35px rgba(16, 185, 129, 0.35);
    }
    
    .card-img-box {
        width: 100%;
        height: 165px;
        object-fit: contain;
        background: radial-gradient(circle, #ffffff 25%, #e2e8f0 100%);
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. LIVE MARKET SEARCH FUNCTION
# ==========================================
@st.cache_data(ttl=1800)
def live_market_search(query):
    try:
        with DDGS() as ddgs:
            return list(ddgs.text(query, max_results=3))
    except Exception:
        return []

# ==========================================
# 4. SIDEBAR AI CHATBOT (ALWAYS VISIBLE ON SIDE!)
# ==========================================
st.sidebar.markdown("""
<div style="background:linear-gradient(135deg,#6d28d9,#8b5cf6); padding:16px; border-radius:14px; text-align:center; margin-bottom:15px;">
    <div style="font-size:12px; color:#a7f3d0; font-weight:700;">🟢 Online • 24/7 AI Concierge</div>
    <h3 style="color:#ffffff; margin:4px 0;">PakDrive AI Chatbot</h3>
    <p style="color:#ede9fe; font-size:12px; margin:0;">Koi bhi sawal poochein (Bikes, Cars, Punjab Scheme, Helicopter)</p>
</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        dict(role="assistant", content="Assalam-o-Alaikum! Main PakDrive AI hoon. Mujh se kisi bhi vehicle ka rate, Electric vs Petrol farq, ya Maryam Nawaz Punjab E-Bike Scheme ke baray mein poochein.")
    ]

for msg in st.session_state.messages:
    st.sidebar.chat_message(msg["role"]).write(msg["content"])

with st.sidebar.form(key="side_chat_form", clear_on_submit=True):
    user_query = st.text_input("Apna sawal yahan likhein...", placeholder="e.g. Punjab E-Bike scheme ki shartain?")
    send_btn = st.form_submit_button("Send Message 🚀", use_container_width=True)

if send_btn and user_query:
    st.session_state.messages.append(dict(role="user", content=user_query))
    q_low = user_query.lower()
    if "scheme" in q_low or "maryam" in q_low or "punjab" in q_low:
        bot_reply = "🏛️ **Maryam Nawaz Punjab E-Bike Scheme:** Punjab ke students aur workers ko **Jolta JE-70L, Yadea, aur Honda CD 70** bina sood (0% markup) ke 2 saal ki asaan aqsaat par di ja rahi hain. Apply karne ke liye `bikes.punjab.gov.pk` visit karein."
    elif "helicopter" in q_low:
        bot_reply = "🚁 **Helicopter Guide:** Robinson R44 helicopter ki qeemat taqreeban Rs. 14.5 Crore hai. Pakistan mein isay uranay ke liye CAA license aur helipad clearance zaroori hai."
    else:
        web_hits = live_market_search(f"{user_query} Pakistan price PakWheels")
        if len(web_hits) > 0:
            top_hit = next(iter(web_hits))
            bot_reply = f"🔎 **Taza Market Update:** {top_hit.get('body', '')}\n\n🔗 [Website Dekhein]({top_hit.get('href', 'https://pakwheels.com')})"
        else:
            bot_reply = "Right side par apna exact budget (PKR) darj karein, main foran us range ki saari 3D vehicles aur buying links dikha dunga!"
    st.session_state.messages.append(dict(role="assistant", content=bot_reply))
    st.rerun()

# ==========================================
# 5. MAIN LUXURY SHOWROOM HERO BANNER
# ==========================================
st.markdown("""
<div class="pro-hero">
    <h1 style="font-size:36px; font-weight:800; margin-bottom:8px;">🚘 PAKDRIVE AI — NEXT-GEN 3D VEHICLE SHOWROOM</h1>
    <p style="font-size:15px; color:#d1fae5 !important;">
        Cycle se lekar Helicopter tak • Live PakWheels & Market Links • Electric vs Petrol Comparison • Maryam Nawaz Punjab E-Bike Scheme
    </p>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 6. USER BUDGET & PREFERENCE CONTROLS
# ==========================================
st.markdown("### 🎛️ Apna Budget Aur Zaroorat Select Karein")
c1, c2, c3, c4 = st.columns(4)
budget = c1.number_input("Aapka Budget (PKR)", min_value=15000, max_value=1500000000, value=170000, step=10000)
daily_km = c2.slider("Rozana ka Safar (KM)", min_value=2, max_value=500, value=40)
fuel_pref = c3.selectbox("Fuel / Power Type", ["Any (Show Best in Budget)", "Electric", "Petrol", "Manual", "Diesel", "Aviation Fuel"])
usage_type = c4.selectbox("Istemaal (Purpose)", ["Personal", "Family", "Commercial", "Luxury/Offroad", "Marine/Leisure", "Aviation"])

# ==========================================
# 7. LOAD & ENRICH DATASET FROM CSV
# ==========================================
df_raw = pd.read_csv("vehicles_3d_master.csv").drop_duplicates(subset=["Model_Name"]).copy()

cats = ["1_Bicycle", "2_Electric_Cycle", "3_Electric_Bike", "4_Petrol_Bike", "5_Three_Wheeler", "6_Car_Sedan_Hatchback", "7_Electric_Car", "8_SUV_4x4", "9_Van_Bus", "10_Heavy_Truck", "11_Boat_Yacht", "12_Helicopter_Aircraft"]
imgs = [
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
urls = [
    "https://pakwheels.com/bikes/bicycles",
    "https://olx.com.pk",
    "https://pakwheels.com/bikes/electric-bikes/",
    "https://pakwheels.com/bikes/honda/cd-70/",
    "https://pakwheels.com/used-cars/search/-/mk_sazgar/",
    "https://pakwheels.com/new-cars/suzuki/alto/",
    "https://pakwheels.com/new-cars/byd/atto-3/",
    "https://pakwheels.com/new-cars/toyota/fortuner/",
    "https://pakwheels.com/used-cars/toyota-coaster/2556",
    "https://pakwheels.com/used-cars/search/-/ct_truck/",
    "https://olx.com.pk",
    "https://controller.com"
]

df_raw["HD_Img"] = df_raw["Category"].map(dict(zip(cats, imgs)))
df_raw["Market_URL"] = df_raw["Category"].map(dict(zip(cats, urls)))

# ==========================================
# 8. HYBRID AI PREDICTION BANNER
# ==========================================
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
