import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
from datetime import datetime
from io import BytesIO
from engine import AuraEngine, get_city_data 

# --- UI CONFIGURATION & THEME ---
st.set_page_config(page_title="AuraCool Sovereign | Titan OS", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f0f4f8 0%, #d9e2ec 100%); color: #0d1b2a; }
    .terminal-log {
        background-color: #0d1b2a; color: #00ff41;
        padding: 20px; border-radius: 8px;
        font-family: 'Courier New', Courier, monospace;
        height: 300px; overflow-y: auto; border: 2px solid #415a77;
        box-shadow: 0px 0px 15px rgba(0, 255, 65, 0.2);
    }
    .main-stats { 
        background-color: #ffffff; padding: 25px; border-radius: 15px; 
        border-left: 10px solid #1a237e; margin-bottom: 25px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- ENGINE DATA (Now with Gurdaspur & Ferozpur) ---
def get_updated_cities():
    data = get_city_data()
    # Adding requested strategic districts
    data["Gurdaspur"] = {"lat": 32.0416, "lon": 75.4053, "base": 42.1, "hum": 52}
    data["Ferozpur"] = {"lat": 30.9250, "lon": 74.6225, "base": 45.8, "hum": 32}
    return data

if 'engine' not in st.session_state:
    st.session_state.engine = AuraEngine()
if 'protocol_active' not in st.session_state:
    st.session_state.protocol_active = False

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛡️ Sovereign Command")
    cities = get_updated_cities()
    selected_city = st.selectbox("📍 Strategic District", sorted(list(cities.keys())))
    
    st.divider()
    aqi_sim = st.slider("Aerosol Density (PM2.5)", 50, 500, 165)
    green = st.slider("Reforestation Target %", 0, 100, 50) / 100
    refl = st.slider("Cool Surface Coverage %", 0, 100, 40) / 100

# --- CALCULATIONS ---
city_info = cities[selected_city]
pollution_penalty = (aqi_sim - 100) * 0.025 if aqi_sim > 100 else 0
optimized_temp = st.session_state.engine.run_simulation(green, refl, city_info['hum']/100, city_info['base']) + pollution_penalty
temp_diff = city_info['base'] - optimized_temp
msg, risk_lvl = st.session_state.engine.predict_health_risk(optimized_temp, city_info['hum'])
co2, money = st.session_state.engine.calculate_carbon_credits(temp_diff)

# --- HEADER METRICS ---
st.title(f"Sovereign Defense Matrix: {selected_city}")
st.markdown('<div class="main-stats">', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Mitigated Temp", f"{round(optimized_temp, 1)}°C", f"-{round(temp_diff, 1)}°C")
c2.metric("Strategic Risk", risk_lvl)
c3.metric("Water Reclaimed", f"{int(temp_diff*210)}k L")
c4.metric("Carbon Revenue", f"₹{int(money*85)}L")
st.markdown('</div>', unsafe_allow_html=True)

# --- TABS ---
t1, t2, t3, t4 = st.tabs(["🏙️ 3D Digital Twin", "🚑 Bio-Intelligence", "⚡ V2G Grid", "📜 Global Policy"])

with t1:
    st.subheader("3D Heat-Retention Geometry")
    # Corrected Image call (Using a public URL for the hackathon demo)
    st.image("https://upload.wikimedia.org/wikipedia/commons/4/4e/Urban_heat_island_profile.png", 
             caption="Urban Heat Island Effect vs. Rural Baseline", use_container_width=True)
    
    building_df = pd.DataFrame({
        "lat": [city_info['lat'] + np.random.normal(0, 0.008) for _ in range(80)],
        "lon": [city_info['lon'] + np.random.normal(0, 0.008) for _ in range(80)],
        "height": [np.random.randint(50, 450) for _ in range(80)],
        "heat": [np.random.randint(100, 255) for _ in range(80)]
    })
    view = pdk.ViewState(latitude=city_info['lat'], longitude=city_info['lon'], zoom=13.5, pitch=50)
    layer = pdk.Layer("ColumnLayer", data=building_df, get_position="[lon, lat]", get_elevation="height", 
                      radius=35, get_fill_color="[heat, 40, 60, 200]", pickable=True)
    st.pydeck_chart(pdk.Deck(map_style='mapbox://styles/mapbox/dark-v10', initial_view_state=view, layers=[layer]))

with t2:
    st.subheader("Health Risk Assessment")
    st.image("https://upload.wikimedia.org/wikipedia/commons/e/ea/Heat_Stress_Index.png", caption="Bio-Thermal Stress Analysis")
    st.error(f"**Aerosol Forcing:** High pollution is trapping {round(pollution_penalty, 2)}°C additional heat.")
    st.info(f"**AI Health Prediction:** {msg}")

with t3:
    st.subheader("Vehicle-to-Grid (V2G) Optimization")
    # Fixed Image Call
    st.image("https://upload.wikimedia.org/wikipedia/commons/b/b3/Hydrogen_fuel_cell_schematic.png", caption="Grid Energy Nexus")
    st.write(f"V2G active. Emergency backup available: **{int(temp_diff*15)} MWh**.")

with t4:
    st.subheader("🤖 Policy Brief & Revenue Export")
    # NEW FEATURE: Dynamic Revenue Chart
    st.write("### Predicted Revenue Growth (2025-2026)")
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=['Carbon Credits', 'Energy Sales', 'Water Savings'])
    st.line_chart(chart_data)

    report_content = f"SOVEREIGN CLIMATE PROTOCOL: {selected_city.upper()}\n" + "="*40 + \
                     f"\nDate: {datetime.now()}\nTemp Reduction: {round(temp_diff, 1)}C\nRisk Level: {risk_lvl}"
    
    # Secure Download Logic
    buf = BytesIO()
    buf.write(report_content.encode())
    buf.seek(0)
    st.download_button(label="📥 DOWNLOAD STRATEGIC POLICY", data=buf, 
                       file_name=f"Sovereign_Policy_{selected_city}.txt", mime="text/plain")

# --- THE GRAND FINALE: TERMINAL SEQUENCE ---
st.divider()
if st.button("🚀 INITIATE GLOBAL SOVEREIGN PROTOCOL"):
    st.session_state.protocol_active = True

if st.session_state.protocol_active:
    st.snow()
    log_placeholder = st.empty()
    logs = [
        f"> Connecting to {selected_city} Smart Grid...",
        "> Bypassing standard thermal limits...",
        "> Synchronizing IR Satellite telemetry...",
        "> Initiating 'Sovereign' V2G discharge sequence...",
        "> Protocol Established. District Status: SECURE."
    ]
    
    current_logs = ""
    for line in logs:
        current_logs += f"{line}<br>"
        log_placeholder.markdown(f'<div class="terminal-log">{current_logs}</div>', unsafe_allow_html=True)
        time.sleep(0.6)
    
    if st.button("Reset Command"):
        st.session_state.protocol_active = False
        st.rerun()
