import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
from engine import AuraEngine, get_city_data 

# --- UI CONFIGURATION ---
st.set_page_config(page_title="AuraCool Sovereign | Titan OS", layout="wide")

# Custom CSS for the "Terminal" look
st.markdown("""
    <style>
    .stApp { background-color: #f0f4f8; }
    .terminal-log {
        background-color: #0d1b2a; color: #00ff41;
        padding: 15px; border-radius: 5px;
        font-family: 'Courier New', Courier, monospace;
        height: 250px; overflow-y: auto; border: 1px solid #415a77;
    }
    .main-stats { 
        background-color: #ffffff; padding: 20px; border-radius: 12px; 
        border-top: 8px solid #1a237e; margin-bottom: 20px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'engine' not in st.session_state:
    st.session_state.engine = AuraEngine()
if 'protocol_active' not in st.session_state:
    st.session_state.protocol_active = False

# --- SIDEBAR ---
with st.sidebar:
    st.title("🏛️ Sovereign OS")
    cities = get_city_data()
    selected_city = st.selectbox("📍 District Command", list(cities.keys()))
    
    st.divider()
    st.subheader("🛰️ Sensor Fusion")
    aqi_sim = st.slider("PM2.5 Pollution", 50, 500, 140)
    green = st.slider("Forestry %", 0, 100, 45) / 100
    refl = st.slider("Cool Surface %", 0, 100, 35) / 100

# --- DATA PROCESSING ---
city_info = cities[selected_city]
pollution_impact = (aqi_sim - 100) * 0.02 if aqi_sim > 100 else 0
optimized_temp = st.session_state.engine.run_simulation(green, refl, city_info['hum']/100, city_info['base']) + pollution_impact
temp_diff = city_info['base'] - optimized_temp
msg, risk_lvl = st.session_state.engine.predict_health_risk(optimized_temp, city_info['hum'])
co2, money = st.session_state.engine.calculate_carbon_credits(temp_diff)

# --- HEADER METRICS ---
st.title(f"District Intelligence: {selected_city}")
st.markdown('<div class="main-stats">', unsafe_allow_html=True)
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Current Delta", f"-{round(temp_diff, 1)}°C", "AI Mitigated")
m2.metric("Health Risk", risk_lvl)
m3.metric("Grid Load", f"{95 - int(temp_diff)}%", "V2G Enabled")
m4.metric("Water Saved", f"{int(temp_diff*180)}k L")
m5.metric("Credits Earned", f"₹{int(money*82)}L")
st.markdown('</div>', unsafe_allow_html=True)

# --- TABS ---
tabs = st.tabs(["🏙️ 3D Digital Twin", "🚑 Health & Pollution", "⚡ Energy Nexus", "🌾 Agri-Water", "📜 Policy Generator"])

with tabs[0]:
    st.subheader("3D Urban Canyon Analysis")
    building_data = pd.DataFrame({
        "lat": [city_info['lat'] + np.random.normal(0, 0.006) for _ in range(70)],
        "lon": [city_info['lon'] + np.random.normal(0, 0.006) for _ in range(70)],
        "height": [np.random.randint(50, 400) for _ in range(70)],
        "heat": [np.random.randint(150, 255) for _ in range(70)]
    })
    view = pdk.ViewState(latitude=city_info['lat'], longitude=city_info['lon'], zoom=14, pitch=55)
    layer = pdk.Layer("ColumnLayer", data=building_data, get_position="[lon, lat]", get_elevation="height", 
                      radius=30, get_fill_color="[heat, 30, 80, 200]", pickable=True)
    st.pydeck_chart(pdk.Deck(map_style='mapbox://styles/mapbox/light-v10', initial_view_state=view, layers=[layer]))

with tabs[1]:
    
    st.error(f"**Aerosol Blanket Detected:** AQI {aqi_sim} is trapping {round(pollution_impact, 2)}°C additional heat.")
    st.info(f"**Health Advisory:** {msg}")

with tabs[2]:
    st.subheader("V2G Energy & Solar Harvesting")
    st.write(f"V2G active. Current backup potential: **{int(temp_diff*15)} MWh**.")
    fig_grid = go.Figure([go.Bar(x=["North", "South", "Central", "Rural"], y=[90, 40, 85, 70], marker_color=['blue']*4)])
    st.plotly_chart(fig_grid, use_container_width=True)

with tabs[3]:
    
    st.subheader("Precision Hydration Index")
    st.metric("Crop Heat Stress", "Low", f"-{int(temp_diff*5)}% stress")

with tabs[4]:
    st.subheader("📜 Official Policy & Economic Report")
    # FIX: Generating a real text blob for the download button
    report = f"AuraCool Policy Report - {selected_city}\n" + "="*30 + \
             f"\nMitigated Temp: {round(optimized_temp, 1)}C\nCarbon Credits: ₹{int(money*82)}L\nRisk Level: {risk_lvl}"
    
    st.download_button(label="📥 Download Policy Brief (PDF/Text)", data=report, file_name=f"Policy_{selected_city}.txt")

# --- FOOTER: THE "INITIATE" LOGIC ---
st.divider()
if st.button("🚀 INITIATE GLOBAL SOVEREIGN PROTOCOL"):
    st.session_state.protocol_active = True

if st.session_state.protocol_active:
    st.snow()
    log_placeholder = st.empty()
    logs = [
        f"Connecting to {selected_city} Smart Grid...",
        "Synchronizing Albedo Sensors...",
        "Applying Urban Forestry algorithm...",
        "Initiating V2G Battery discharge...",
        "System Stable. District Protected."
    ]
    
    # Simulate a scrolling terminal log
    log_text = ""
    for line in logs:
        log_text += f"> {line}<br>"
        log_placeholder.markdown(f'<div class="terminal-log">{log_text}</div>', unsafe_allow_html=True)
        time.sleep(0.5)
