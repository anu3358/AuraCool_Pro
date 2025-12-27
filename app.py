import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
from io import BytesIO
from engine import AuraEngine, get_city_data 

# --- UI CONFIGURATION ---
st.set_page_config(page_title="AURAMASTER | Sovereign Urban OS", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #010409; color: #e6edf3; }
    .ticker-bar {
        background: #0d1117; padding: 10px; border-bottom: 2px solid #1f6feb;
        color: #39ff14; font-family: 'Courier New', monospace; font-weight: bold;
        text-align: center; font-size: 16px;
    }
    .main-stats { 
        background-color: #0d1117; padding: 25px; border-radius: 15px; 
        border: 1px solid #30363d; border-top: 5px solid #1f6feb;
    }
    .terminal-log {
        background-color: #000000; color: #39ff14;
        padding: 20px; border-radius: 10px;
        font-family: 'Courier New', monospace;
        height: 300px; overflow-y: auto; border: 1px solid #39ff14;
    }
    [data-testid="stMetricValue"] { color: #58a6ff !important; font-weight: 800; font-family: 'Orbitron', sans-serif; }
    .feature-header { color: #58a6ff; font-weight: bold; border-bottom: 1px solid #30363d; padding-bottom: 5px; margin-bottom: 15px;}
    </style>
    """, unsafe_allow_html=True)

# --- LIVE CARBON TICKER ---
st.markdown(f"""
    <div class="ticker-bar">
        LIVE MARKET: CARBON CREDIT $ {round(np.random.uniform(28, 29), 2)} ▲ | 
        WIND VECTOR: NE 12.4 KM/H | 
        SATELLITE SYNC: ACTIVE
    </div>
    """, unsafe_allow_html=True)

if 'engine' not in st.session_state:
    st.session_state.engine = AuraEngine()
if 'protocol' not in st.session_state:
    st.session_state.protocol = False

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛡️ SOVEREIGN v5.2")
    cities = get_city_data()
    city_name = st.selectbox("📍 GEOSPATIAL FOCUS", list(cities.keys()))
    st.markdown("---")
    green = st.slider("Forestry Density", 0.0, 1.0, 0.45)
    albedo = st.slider("Albedo Surface Force", 0.0, 1.0, 0.35)
    aqi = st.slider("Atmospheric PM2.5", 50, 500, 150)

# --- AI LOGIC ---
city = cities[city_name]
aerosol_heat = (aqi - 100) * 0.035 if aqi > 100 else 0
final_temp = st.session_state.engine.run_simulation(green, albedo, city['hum'], city['base']) + aerosol_heat
delta = city['base'] - final_temp
msg, risk_lvl = st.session_state.engine.predict_health_risk(final_temp, city['hum'])
co2, revenue = st.session_state.engine.calculate_carbon_credits(delta)

# --- DASHBOARD ---
st.title(f"THERMAL DEFENSE GRID: {city_name.upper()}")
st.markdown('<div class="main-stats">', unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("TEMP REDUCTION", f"-{round(delta, 1)}°C")
c2.metric("THREAT LEVEL", risk_lvl)
c3.metric("GRID STABILITY", f"{85 + int(delta)}%")
c4.metric("WATER RECLAIMED", f"{int(delta*190)}k L")
c5.metric("CARBON ROI", f"₹{int(revenue*84)} L")
st.markdown('</div>', unsafe_allow_html=True)

tabs = st.tabs(["🛰️ 3D DIGITAL TWIN", "🚑 BIO-HEALTH AI", "⚡ ENERGY ARBITRAGE", "📜 SOVEREIGN POLICY"])

with tabs[0]:
    st.markdown('<div class="feature-header">NEURAL WIND VECTORING & 3D CANYONS</div>', unsafe_allow_html=True)
    b_data = pd.DataFrame({
        "lat": [city['lat'] + np.random.normal(0, 0.007) for _ in range(120)],
        "lon": [city['lon'] + np.random.normal(0, 0.007) for _ in range(120)],
        "height": [np.random.randint(50, 550) for _ in range(120)],
        "heat": [np.random.randint(150, 255) for _ in range(120)]
    })
    view = pdk.ViewState(latitude=city['lat'], longitude=city['lon'], zoom=14, pitch=60)
    layer = pdk.Layer("ColumnLayer", data=b_data, get_position="[lon, lat]", get_elevation="height", 
                      radius=35, get_fill_color="[heat, 40, 60, 200]", pickable=True)
    st.pydeck_chart(pdk.Deck(map_style='mapbox://styles/mapbox/dark-v10', initial_view_state=view, layers=[layer]))

with tabs[1]:
    st.markdown('<div class="feature-header">BIO-THERMAL STRESS ANALYSIS</div>', unsafe_allow_html=True)
    st.error(f"**Aerosol Forcing:** PM2.5 levels are trapping {round(aerosol_heat, 2)}°C of heat.")
    fig = go.Figure(go.Indicator(
        mode = "gauge+number", value = final_temp,
        title = {'text': "District Wet Bulb Temperature (°C)"},
        gauge = {'axis': {'range': [20, 50]}, 'bar': {'color': "#1f6feb"}}
    ))
    st.plotly_chart(fig, use_container_width=True)

with tabs[2]:
    st.markdown('<div class="feature-header">V2G ENERGY & GRID SELF-HEALING</div>', unsafe_allow_html=True)
    st.write(f"Grid Status: **REBALANCING**. V2G Buffer: **{int(delta*18)} MWh**.")
    st.line_chart(pd.DataFrame(np.random.randn(20, 2), columns=['Grid Frequency', 'V2G Relief']))

with tabs[3]:
    st.markdown('<div class="feature-header">SOVEREIGN POLICY MANIFEST</div>', unsafe_allow_html=True)
    manifest = f"SOVEREIGN MANIFEST: {city_name}\n" + "-"*30 + f"\nDelta: {round(delta, 1)}C\nRevenue: ₹{int(revenue*84)}L"
    st.download_button("📥 DOWNLOAD DATA-AUTH MANIFEST", manifest, file_name=f"Manifest_{city_name}.txt")

# --- PROTOCOL ---
st.divider()
if st.button("🔴 INITIATE GLOBAL SOVEREIGN PROTOCOL"):
    st.session_state.protocol = True

if st.session_state.protocol:
    st.snow()
    placeholder = st.empty()
    steps = ["📡 Establishing Sat Uplink...", "🧠 Neural SVF Mapping...", "🌪️ Wind Dynamics Calculation...", "✅ PROTOCOL ENGAGED."]
    log = ""
    for step in steps:
        log += f"> {step}<br>"
        placeholder.markdown(f'<div class="terminal-log">{log}</div>', unsafe_allow_html=True)
        time.sleep(0.5)
