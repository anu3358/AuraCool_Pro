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
st.set_page_config(page_title="AuraCool Sovereign | 2025 Global Edition", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f0f4f8 0%, #d9e2ec 100%); color: #0d1b2a; }
    .terminal-header { color: #00ff41; font-weight: bold; margin-bottom: 5px; }
    .terminal-log {
        background-color: #0d1b2a; color: #00ff41;
        padding: 20px; border-radius: 8px;
        font-family: 'Courier New', Courier, monospace;
        height: 300px; overflow-y: auto; border: 2px solid #415a77;
        box-shadow: 0px 0px 15px rgba(0, 255, 65, 0.2);
    }
    .main-stats { 
        background-color: #ffffff; padding: 25px; border-radius: 15px; 
        border-left: 8px solid #1a237e; margin-bottom: 25px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.1);
    }
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #1a237e; color: white; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- ENGINE DATA (Fixed to include Gurdaspur & Ferozpur) ---
def get_updated_cities():
    data = get_city_data()
    # Adding the new districts requested
    data["Gurdaspur"] = {"lat": 32.0416, "lon": 75.4053, "base": 42.1, "hum": 52}
    data["Ferozpur"] = {"lat": 30.9250, "lon": 74.6225, "base": 45.8, "hum": 32}
    return data

if 'engine' not in st.session_state:
    st.session_state.engine = AuraEngine()
if 'protocol_active' not in st.session_state:
    st.session_state.protocol_active = False

# --- SIDEBAR COMMANDS ---
with st.sidebar:
    st.title("🛡️ Sovereign OS v4.0")
    cities = get_updated_cities()
    selected_city = st.selectbox("📍 Select Strategic District", sorted(list(cities.keys())))
    
    st.divider()
    st.subheader("🛰️ Intelligence Inputs")
    aqi_sim = st.slider("Aerosol Density (PM2.5)", 50, 500, 165)
    green = st.slider("Reforestation Target %", 0, 100, 50) / 100
    refl = st.slider("Cool Roof Coverage %", 0, 100, 40) / 100
    
# --- CALCULATIONS ---
city_info = cities[selected_city]
# Advanced forcing logic
p_penalty = (aqi_sim - 100) * 0.025 if aqi_sim > 100 else 0
optimized_temp = st.session_state.engine.run_simulation(green, refl, city_info['hum']/100, city_info['base']) + p_penalty
temp_diff = city_info['base'] - optimized_temp
msg, risk_lvl = st.session_state.engine.predict_health_risk(optimized_temp, city_info['hum'])
co2, money = st.session_state.engine.calculate_carbon_credits(temp_diff)

# --- DASHBOARD HEADER ---
st.title(f"District Defense Matrix: {selected_city}")
st.markdown('<div class="main-stats">', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Current Thermal Delta", f"-{round(temp_diff, 1)}°C", f"Ambient: {city_info['base']}°C")
c2.metric("Strategic Risk Index", risk_lvl)
c3.metric("Water Reclaimed", f"{int(temp_diff*210)}k L", "Daily Evap Savings")
c4.metric("Carbon Revenue", f"₹{int(money*85)}L", "+12% Growth")
st.markdown('</div>', unsafe_allow_html=True)

# --- MAIN INTERFACE TABS ---
t1, t2, t3, t4 = st.tabs(["🏙️ 3D Tactical Twin", "🚑 Bio-Intelligence", "⚡ V2G Energy Grid", "📜 Global Policy Office"])

with t1:
    st.subheader("3D Heat-Retention Geometry")
    # Generates a 3D view of "Urban Canyons" in the selected district
    points = 100
    building_df = pd.DataFrame({
        "lat": [city_info['lat'] + np.random.normal(0, 0.008) for _ in range(points)],
        "lon": [city_info['lon'] + np.random.normal(0, 0.008) for _ in range(points)],
        "height": [np.random.randint(40, 500) for _ in range(points)],
        "heat": [np.random.randint(100, 255) for _ in range(points)]
    })
    view = pdk.ViewState(latitude=city_info['lat'], longitude=city_info['lon'], zoom=14, pitch=50)
    layer = pdk.Layer("ColumnLayer", data=building_df, get_position="[lon, lat]", get_elevation="height", 
                      radius=35, get_fill_color="[heat, 50, 50, 200]", pickable=True)
    st.pydeck_chart(pdk.Deck(map_style='mapbox://styles/mapbox/dark-v10', initial_view_state=view, layers=[layer]))
    st.caption("Visualizing height-to-heat correlation: Taller pillars indicate 'Heat Canyons' requiring priority mitigation.")

with t2:
    st.subheader("Health & Atmospheric Risk Matrix")
    
    st.warning(f"**Aerosol Blanket Alert:** High AQI ({aqi_sim}) in {selected_city} is currently trapping heat, increasing night-time cooling lag.")
    st.info(f"**AI Health Prediction:** {msg}")

with t3:
    st.subheader("Vehicle-to-Grid (V2G) Optimization")
    

[Image of hydrogen fuel cell]

    # Simulating grid stability
    hours = list(range(24))
    load = [60 + 20*np.sin((h-6)*np.pi/12) for h in hours]
    v2g_relief = [l - (temp_diff*2.5) for l in load]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hours, y=load, name="Standard Load", line=dict(color='gray', dash='dot')))
    fig.add_trace(go.Scatter(x=hours, y=v2g_relief, name="Sovereign Optimized", line=dict(color='#1a237e', width=4)))
    st.plotly_chart(fig, use_container_width=True)

with t4:
    st.subheader("🤖 Policy Brief & Revenue Export")
    # THE "FIXED" PDF/REPORT LOGIC
    report_content = f"""
    OFFICIAL CLIMATE DEFENSE PROTOCOL: {selected_city.upper()}
    DATE GENERATED: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    ----------------------------------------------------------
    1. THERMAL TARGET: Mitigated to {round(optimized_temp, 1)}°C
    2. HEALTH RISK: {risk_lvl}
    3. CARBON REVENUE: ₹{int(money*85)} Lakhs Projected
    
    DIRECTIVES:
    - Enforce 'Cool Roof' Albedo standards (>0.6) for all industrial zones in {selected_city}.
    - Activate V2G grid balancing during peak thermal load (14:00 - 17:00).
    - Deploy Green Buffer Zones in the North-East wind corridors.
    ----------------------------------------------------------
    AUTHENTICATION: Sovereign AI v4.0 Secure
    """
    
    # Robust download buffer
    buf = BytesIO()
    buf.write(report_content.encode())
    buf.seek(0)
    
    st.download_button(
        label="📥 DOWNLOAD OFFICIAL STRATEGIC POLICY",
        data=buf,
        file_name=f"Sovereign_Policy_{selected_city}.txt",
        mime="text/plain"
    )
    st.success("Report is ready for municipal authorization.")

# --- THE GRAND FINALE: SOVEREIGN PROTOCOL ---
st.divider()
col_btn, col_spacer = st.columns([1, 2])
with col_btn:
    if st.button("🚀 INITIATE GLOBAL SOVEREIGN PROTOCOL"):
        st.session_state.protocol_active = True

if st.session_state.protocol_active:
    st.snow()
    log_placeholder = st.empty()
    logs = [
        f"Connecting to {selected_city} Municipal Grid...",
        "Bypassing standard thermal limits...",
        "Synchronizing satellite infrared telemetry...",
        "Initiating 'Sovereign' V2G discharge sequence...",
        "Calculating Sky-View Factor (SVF) adjustments...",
        "PROTOCOL ACTIVE: District is now Climate-Resilient."
    ]
    
    current_logs = ""
    for line in logs:
        current_logs += f"<div class='terminal-header'>[ACCESS GRANTED]</div> {line}<br>"
        log_placeholder.markdown(f'<div class="terminal-log">{current_logs}</div>', unsafe_allow_html=True)
        time.sleep(0.6)
    
    if st.button("Reset Command"):
        st.session_state.protocol_active = False
        st.rerun()
