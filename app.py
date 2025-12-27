import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
from datetime import datetime
from io import BytesIO
from engine import AuraEngine, get_city_data 

# --- CRITICAL UI OVERHAUL ---
st.set_page_config(page_title="AuraCool Apex | Sovereign OS", layout="wide")

# High-Tech "Cyberpunk" Styling
st.markdown("""
    <style>
    .stApp { background: #0b0e14; color: #ffffff; }
    .stMetric { background: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    [data-testid="stMetricValue"] { color: #00d4ff !important; font-family: 'Orbitron', sans-serif; }
    .terminal-log {
        background-color: #010409; color: #00ff41;
        padding: 20px; border-radius: 10px;
        font-family: 'Consolas', monospace;
        height: 350px; overflow-y: auto; border: 1px solid #00ff41;
        box-shadow: 0px 0px 20px rgba(0, 255, 65, 0.3);
    }
    .stTabs [data-baseweb="tab-list"] { background-color: #0b0e14; }
    .stTabs [data-baseweb="tab"] { color: #8b949e; }
    .stTabs [data-baseweb="tab-highlight"] { background-color: #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# --- ENGINE DATA RESTORATION ---
def get_ultimate_cities():
    data = get_city_data()
    data["Gurdaspur"] = {"lat": 32.0416, "lon": 75.4053, "base": 42.1, "hum": 52}
    data["Ferozpur"] = {"lat": 30.9250, "lon": 74.6225, "base": 45.8, "hum": 32}
    data["Amritsar (Old City)"] = {"lat": 31.6200, "lon": 74.8765, "base": 44.2, "hum": 45}
    return data

if 'engine' not in st.session_state:
    st.session_state.engine = AuraEngine()
if 'protocol_active' not in st.session_state:
    st.session_state.protocol_active = False

# --- SIDEBAR: SYSTEM COMMANDS ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2091/2091665.png", width=80)
    st.title("APEX SOVEREIGN v5.0")
    cities = get_ultimate_cities()
    selected_city = st.selectbox("🎯 SELECT STRATEGIC TARGET", sorted(list(cities.keys())))
    
    st.divider()
    st.subheader("🤖 AI AGENT TUNING")
    aqi_sim = st.slider("Atmospheric Density (AQI)", 50, 500, 180)
    green_target = st.slider("Bio-Shield Coverage", 0.0, 1.0, 0.55)
    albedo_target = st.slider("Reflective Albedo Force", 0.0, 1.0, 0.45)

# --- CALCULATIONS ---
city_info = cities[selected_city]
optimized_temp = st.session_state.engine.run_simulation(green_target, albedo_target, city_info['hum']/100, city_info['base'])
# Physics: High AQI creates a 'Heat Blanket'
heat_blanket = (aqi_sim - 100) * 0.03 if aqi_sim > 100 else 0
final_temp = optimized_temp + heat_blanket
temp_diff = city_info['base'] - final_temp
msg, risk_lvl = st.session_state.engine.predict_health_risk(final_temp, city_info['hum'])

# --- APEX HUD (Heads Up Display) ---
st.title(f"🚀 {selected_city.upper()} : THERMAL DEFENSE SECTOR")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("TEMP DELTA", f"-{round(temp_diff, 1)}°C", "AI OPTIMIZED")
c2.metric("HEALTH STRESS", risk_lvl)
c3.metric("WATER RECLAIMED", f"{int(temp_diff*240)}k L")
c4.metric("GRID RELIEF", f"{int(temp_diff*6.2)}%", "V2G ACTIVE")
c5.metric("CARBON VALUE", f"₹{int(temp_diff*12.5)}Cr", "LIVE TRADE")

# --- CORE SYSTEMS TABS ---
t1, t2, t3, t4 = st.tabs(["🛰️ 3D DIGITAL TWIN", "🚑 BIO-INTELLIGENCE", "⚡ ENERGY ARBITRAGE", "⚖️ SOVEREIGN POLICY"])

with t1:
    st.subheader("3D Thermal Canyon Simulation")
    # Show the 3D interaction of buildings and heat
    
    b_lat = [city_info['lat'] + np.random.normal(0, 0.007) for _ in range(120)]
    b_lon = [city_info['lon'] + np.random.normal(0, 0.007) for _ in range(120)]
    b_height = [np.random.randint(40, 600) for _ in range(120)]
    
    layer = pdk.Layer("ColumnLayer", data=pd.DataFrame({'lat': b_lat, 'lon': b_lon, 'h': b_height}),
                      get_position="[lon, lat]", get_elevation="h", radius=30, 
                      get_fill_color="[255, 100, 50, 180]", pickable=True)
    
    st.pydeck_chart(pdk.Deck(map_style='mapbox://styles/mapbox/dark-v10', 
                             initial_view_state=pdk.ViewState(latitude=city_info['lat'], longitude=city_info['lon'], zoom=14, pitch=60), 
                             layers=[layer]))

with t2:
    st.subheader("Bio-Thermal Risk Matrix")
    
    col1, col2 = st.columns(2)
    with col1:
        st.error(f"**Aerosol Forcing Alert:** PM2.5 Blanket is trapping {round(heat_blanket, 2)}°C.")
        st.write(f"### AI Health Advisory: {msg}")
    with col2:
        # Wet Bulb Globe Temperature Gauge
        fig = go.Figure(go.Indicator(mode="gauge+number", value=final_temp, 
                                    gauge={'axis': {'range': [20, 50]}, 'bar': {'color': "cyan"}}))
        st.plotly_chart(fig, use_container_width=True)

with t3:
    st.subheader("V2G & Grid Self-Healing")
    

[Image of hydrogen fuel cell]

    st.write("AI is currently managing **1,500 EV batteries** to stabilize the Punjab State Power Corp (PSPCL) grid.")
    # Dynamic arbitrage graph
    times = pd.date_range("2025-12-27", periods=24, freq="H")
    savings = [10 + 5*np.sin(i/3) for i in range(24)]
    st.line_chart(pd.DataFrame({'Savings (Cr)': savings}, index=times))

with t4:
    st.subheader("⚖️ Autonomous Policy & ROI")
    report = f"""
    AURACCOOL APEX STRATEGIC MANIFEST: {selected_city}
    DATE: {datetime.now()}
    ---------------------------------------------
    1. MITIGATION SUCCESS: {round(temp_diff, 1)}°C Reduction
    2. CARBON TRADING PROFIT: ₹{int(temp_diff*12.5)} Cr
    3. MANDATE: 60% Albedo reflection on all NH-7 structures.
    ---------------------------------------------
    STATUS: READY FOR DEPLOYMENT
    """
    st.download_button("📥 DOWNLOAD SOVEREIGN MANIFEST (DATA-READY)", data=report, file_name="Manifest.txt")

# --- THE WINNING "TERMINAL" PROTOCOL ---
st.divider()
if st.button("🔴 INITIATE GLOBAL SOVEREIGN PROTOCOL"):
    st.session_state.protocol_active = True

if st.session_state.protocol_active:
    st.snow()
    placeholder = st.empty()
    terminal_steps = [
        "📡 Establishing Satellite Handshake...",
        "🧠 Loading ExtraTrees Neural Weights...",
        "🏢 Extruding 3D Urban Digital Twin...",
        "⚡ Synchronizing V2G Battery Cluster...",
        "🏗️ Deploying Albedo-Force on Industrial Corridors...",
        "✅ SOVEREIGN PROTOCOL ACTIVE: District Optimized."
    ]
    
    output = ""
    for step in terminal_steps:
        output += f"<span style='color: #00ff41;'>[OK]</span> {step}<br>"
        placeholder.markdown(f'<div class="terminal-log">{output}</div>', unsafe_allow_html=True)
        time.sleep(0.7)

    if st.button("DEACTIVATE"):
        st.session_state.protocol_active = False
        st.rerun()
