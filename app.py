import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
from engine import AuraEngine

# --- APP CONFIGURATION ---
st.set_page_config(page_title="AURAMASTER | Urban Command", layout="wide")

# Professional "Gov-Tech" Light Theme
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1a1a1a; }
    .news-ticker {
        background: #004085; color: white; padding: 10px; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: bold; border-radius: 5px; margin-bottom: 20px;
    }
    .stMetric { background-color: #f8f9fa; border: 1px solid #e9ecef; padding: 15px; border-radius: 10px; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { background-color: #f8f9fa; border-radius: 5px; padding: 10px 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- LIVE NEWS TICKER (Winning Feature) ---
st.markdown(f"""
    <div class="news-ticker">
        📢 SYSTEM ALERT: High-Thermal Anomaly detected in Ferozpur Sector | 
        V2G Status: Synchronizing 1,200 EV Batteries | 
        AQI Forecast: PM2.5 levels rising in Amritsar Industrial Zone
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
    st.header("🏛️ Control Interface")
    cities = get_data()
    city_name = st.selectbox("Strategic District", list(cities.keys()))
    st.divider()
    green = st.slider("Urban Canopy (%)", 0.0, 1.0, 0.35)
    albedo = st.slider("Surface Albedo (%)", 0.0, 1.0, 0.25)
    aqi = st.slider("Atmospheric AQI", 50, 500, 160)
    st.caption("Adjust sliders to simulate infrastructure deployment.")

# --- LIVE ENGINE CALCULATIONS ---
city = cities[city_name]
opt_temp = st.session_state.engine.run_simulation(green, albedo, city['hum'], city['base'])
delta = city['base'] - opt_temp
res_grade, res_msg = st.session_state.engine.calculate_resilience_score(green, albedo, aqi)
mwh, savings_cr = st.session_state.engine.calculate_v2g_revenue(delta)
risk_lvl, risk_msg = st.session_state.engine.predict_health_risk(opt_temp, city['hum'])

# --- MAIN DASHBOARD LAYOUT ---
st.title(f"Urban Defense Command: {city_name}")

# Metrics Row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Resilience Grade", res_grade)
col2.metric("Thermal Reduction", f"-{round(delta, 1)}°C")
col3.metric("Grid Relief", f"{round(mwh, 1)} MWh")
col4.metric("Economic Impact", f"₹{round(savings_cr, 2)} Cr")

st.divider()

# Tabbed Interface
tab1, tab2, tab3 = st.tabs(["🏙️ Digital Twin Simulation", "📊 Energy & Economics", "📜 Strategic Policy"])

with tab1:
    st.subheader("3D Heat Vector Map")
    
    map_data = pd.DataFrame({
        "lat": [city['lat'] + np.random.normal(0, 0.006) for _ in range(150)],
        "lon": [city['lon'] + np.random.normal(0, 0.006) for _ in range(150)],
        "height": [np.random.randint(10, 400) for _ in range(150)]
    })
    view = pdk.ViewState(latitude=city['lat'], longitude=city['lon'], zoom=14, pitch=55)
    layer = pdk.Layer("ColumnLayer", data=map_data, get_position="[lon, lat]", get_elevation="height", radius=35, get_fill_color="[30, 144, 255, 200]")
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view))
    st.write(f"**District Health Status:** {risk_msg}")

with tab2:
    st.subheader("V2G Energy Nexus")
    

[Image of hydrogen fuel cell]

    st.write(f"By reducing thermal load, {city_name} can re-inject **{int(mwh)} MWh** of EV energy back into the grid during peak demand.")
    
    # Economics Chart
    savings_data = pd.DataFrame({
        'Category': ['Carbon Credits', 'Energy Savings', 'Healthcare Savings'],
        'Value (Cr)': [round(delta*1.2, 2), savings_cr, round(delta*0.8, 2)]
    })
    st.bar_chart(savings_data, x='Category', y='Value (Cr)')

with tab3:
    st.subheader("Policy Deployment Brief")
    
    brief = f"""
    EXECUTIVE SUMMARY FOR {city_name.upper()} DISTRICT
    --------------------------------------------------
    - TARGET TEMP: {round(opt_temp, 1)}°C
    - RESILIENCE GRADE: {res_grade}
    - ACTION: Enforce Cool-Roof Albedo standards (>0.6) on all NH-7 properties.
    - ACTION: Initiate V2G protocol for 12,000 commercial EVs.
    - REVENUE: ₹{round(savings_cr, 2)} Cr in avoided peak-power costs.
    """
    st.text_area("Official Mandate", brief, height=200)
    st.download_button("Export Official Brief", brief, file_name=f"Sovereign_Brief_{city_name}.txt")

# --- GLOBAL PROTOCOL ---
st.divider()
if st.button("🚀 EXECUTE GLOBAL SOVEREIGN PROTOCOL"):
    with st.spinner("Synchronizing District Infrastructure..."):
        time.sleep(2)
        st.balloons()
        st.success(f"Protocol Executed. {city_name} is now in Autonomous Climate Defense mode.")
