import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
from engine import AuraEngine

# --- UI CONFIGURATION ---
st.set_page_config(page_title="AURAMASTER | Urban Command", layout="wide")

# Professional Gov-Tech Theme (High Visibility)
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1a1a1a; }
    .news-ticker {
        background: #004085; color: white; padding: 12px; 
        font-family: 'Arial', sans-serif; font-weight: bold; 
        border-radius: 5px; margin-bottom: 25px; border-left: 10px solid #ffcc00;
    }
    .stMetric { background-color: #f1f3f5; border: 1px solid #dee2e6; padding: 15px; border-radius: 10px; }
    .feature-box { background-color: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #007bff; }
    </style>
    """, unsafe_allow_html=True)

# --- LIVE INTELLIGENCE TICKER ---
st.markdown(f"""
    <div class="news-ticker">
        🔴 ADVISORY: Heat Dome developing over Northern Punjab | 
        ⚡ V2G GRID: 15,000 EV Units Standby for Discharge | 
        🛰️ SATELLITE: Thermal Anomaly detected in Ludhiana Sector
    </div>
    """, unsafe_allow_html=True)

if 'engine' not in st.session_state:
    st.session_state.engine = AuraEngine()

def get_data():
    return {
        "Gurdaspur": {"lat": 32.0416, "lon": 75.4053, "base": 42.5, "hum": 0.52},
        "Ferozpur": {"lat": 30.9250, "lon": 74.6225, "base": 46.2, "hum": 0.35},
        "Ludhiana": {"lat": 30.9010, "lon": 75.8573, "base": 47.1, "hum": 0.44},
        "Amritsar": {"lat": 31.6340, "lon": 74.8723, "base": 44.8, "hum": 0.40}
    }

# --- SIDEBAR CONTROL ---
with st.sidebar:
    st.header("⚙️ System Parameters")
    cities = get_data()
    city_name = st.selectbox("Strategic District", list(cities.keys()))
    st.divider()
    green = st.slider("Urban Canopy Expansion (%)", 0.0, 1.0, 0.35)
    albedo = st.slider("Cool Surface (Albedo) Coating (%)", 0.0, 1.0, 0.25)
    aqi = st.slider("Atmospheric AQI", 50, 500, 160)

# --- ENGINE CALCULATIONS ---
city = cities[city_name]
opt_temp = st.session_state.engine.run_simulation(green, albedo, city['hum'], city['base'])
delta = city['base'] - opt_temp
res_grade, res_msg = st.session_state.engine.calculate_resilience_score(green, albedo, aqi)
mwh, savings_cr = st.session_state.engine.calculate_v2g_revenue(delta)
risk_lvl, risk_msg = st.session_state.engine.predict_health_risk(opt_temp, city['hum'])

# --- MAIN DASHBOARD ---
st.title(f"District Command Center: {city_name}")

# Metrics Section
c1, c2, c3, c4 = st.columns(4)
c1.metric("Resilience Grade", res_grade)
c2.metric("Temp Reduction", f"-{round(delta, 1)}°C")
c3.metric("V2G Grid Relief", f"{round(mwh, 1)} MWh")
c4.metric("Econ. Recovery", f"₹{round(savings_cr, 2)} Cr")

st.divider()

t1, t2, t3 = st.tabs(["🏙️ Digital Twin Analysis", "⚡ Energy Arbitrage", "📜 Policy Manifest"])

with t1:
    st.subheader("Geospatial Thermal Mapping")
    # 3D Building Simulation
    map_data = pd.DataFrame({
        "lat": [city['lat'] + np.random.normal(0, 0.006) for _ in range(150)],
        "lon": [city['lon'] + np.random.normal(0, 0.006) for _ in range(150)],
        "height": [np.random.randint(10, 400) for _ in range(150)]
    })
    view = pdk.ViewState(latitude=city['lat'], longitude=city['lon'], zoom=14, pitch=55)
    layer = pdk.Layer("ColumnLayer", data=map_data, get_position="[lon, lat]", get_elevation="height", radius=35, get_fill_color="[0, 102, 204, 200]")
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view))
    st.warning(f"**Health Advisory:** {risk_msg}")

with t2:
    st.subheader("V2G Energy Nexus & Economics")
    st.markdown('<div class="feature-box">', unsafe_allow_html=True)
    st.write(f"Thermal mitigation in **{city_name}** reduces the district's Peak Energy demand by approximately **{int(mwh)} MWh**.")
    st.write("This allows the government to utilize EV batteries as a Virtual Power Plant, avoiding expensive power purchase agreements.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Financial Impact Chart
    chart_data = pd.DataFrame({
        'Source': ['Carbon Offset', 'Grid Stability', 'Health Savings'],
        'Value (Cr)': [round(delta*1.1, 2), savings_cr, round(delta*0.9, 2)]
    })
    st.bar_chart(chart_data, x='Source', y='Value (Cr)')

with t3:
    st.subheader("Official Strategic Brief")
    brief = f"""
    GOVERNMENT OF PUNJAB - CLIMATE DEFENSE UNIT
    -------------------------------------------
    SECTOR: {city_name.upper()} 
    RESILIENCE RATING: {res_grade}
    OPTIMIZED TEMP TARGET: {round(opt_temp, 1)}°C
    
    STRATEGIC ACTIONS:
    1. Deploy Albedo coatings to NH-7 Commercial Corridor.
    2. Unlock V2G discharging for 5,000 commercial vehicles.
    3. Estimated Revenue Generation: ₹{round(savings_cr, 2)} Crore.
    """
    st.text_area("Official Mandate", brief, height=220)
    st.download_button("📥 Export Policy Manifest", brief, file_name=f"Policy_{city_name}.txt")

# --- EXECUTION ---
st.divider()
if st.button("🚀 EXECUTE SOVEREIGN PROTOCOL"):
    with st.spinner("Synchronizing Grid Infrastructure..."):
        time.sleep(1.5)
        st.balloons()
        st.success("Sovereign Protocol Successfully Engaged. Autonomous District Cooling is Active.")
