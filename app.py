import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import time
from engine import AuraEngine

st.set_page_config(page_title="AURAMASTER | Punjab State Command", layout="wide")

# Gov-Tech Theme
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; color: #1a1a1a; }
    .news-ticker {
        background: #004085; color: white; padding: 12px; 
        font-family: 'Arial', sans-serif; font-weight: bold; 
        border-radius: 5px; margin-bottom: 25px; border-left: 10px solid #ffcc00;
    }
    .stMetric { background-color: #f1f3f5; border: 1px solid #dee2e6; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

if 'engine' not in st.session_state:
    st.session_state.engine = AuraEngine()

def get_state_data():
    return {
        "Gurdaspur": {"lat": 32.0416, "lon": 75.4053, "base": 42.5, "hum": 0.52},
        "Ferozpur": {"lat": 30.9250, "lon": 74.6225, "base": 46.2, "hum": 0.35},
        "Ludhiana": {"lat": 30.9010, "lon": 75.8573, "base": 47.1, "hum": 0.44},
        "Amritsar": {"lat": 31.6340, "lon": 74.8723, "base": 44.8, "hum": 0.40},
        "Patiala": {"lat": 30.3398, "lon": 76.3869, "base": 43.5, "hum": 0.48}
    }

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ State Control")
    cities = get_state_data()
    green = st.slider("Urban Canopy (%)", 0.0, 1.0, 0.35)
    albedo = st.slider("Albedo Coating (%)", 0.0, 1.0, 0.25)
    aqi = st.slider("Atmospheric AQI", 50, 500, 160)
    selected_focus = st.selectbox("Deep Sector Audit", list(cities.keys()))

# --- DATA AGGREGATION ---
state_list = []
total_rev, total_mwh, total_water = 0, 0, 0

for name, data in cities.items():
    opt_temp = st.session_state.engine.run_simulation(green, albedo, data['hum'], data['base'])
    delta = data['base'] - opt_temp
    mwh, rev = st.session_state.engine.calculate_v2g_revenue(delta)
    water = st.session_state.engine.calculate_water_recovery(delta)
    
    total_rev += rev
    total_mwh += mwh
    total_water += water
    state_list.append({"name": name, "lat": data['lat'], "lon": data['lon'], "temp": opt_temp, "delta": delta, "height": opt_temp * 500})

df = pd.DataFrame(state_list)

# --- HEADER ---
st.markdown('<div class="news-ticker">🌍 STATE COMMAND: Virtual Power Plant Synced | 💧 WATER ADVISORY: Evaporation delta tracking active</div>', unsafe_allow_html=True)
st.title("Punjab Climate Defense & Resource Command")

m1, m2, m3, m4 = st.columns(4)
m1.metric("State Avg. Temp", f"{round(df['temp'].mean(), 1)}°C")
m2.metric("Total Water Saved", f"{round(total_water, 2)} Million L")
m3.metric("State ROI", f"₹{round(total_rev, 2)} Cr")
m4.metric("Grid Relief", f"{round(total_mwh, 1)} MWh")

st.divider()

# --- THE WINNING TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["🗺️ State Twin", "💧 Water-Energy Nexus", "🛰️ Sentinel Audit", "📜 Policy Brief"])

with tab1:
    st.subheader("3D State-Wide Thermal View")
    view = pdk.ViewState(latitude=31.2, longitude=75.4, zoom=6.5, pitch=45)
    layer = pdk.Layer("ColumnLayer", data=df, get_position="[lon, lat]", get_elevation="height", radius=7000, get_fill_color="[0, 100, 255, 180]")
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view, tooltip={"text": "{name}: {temp}°C"}))

with tab2:
    st.subheader("💧 Resource Recovery: Solving Water Scarcity")
    st.write(f"Thermal reduction in **{selected_focus}** directly prevents groundwater depletion.")
    
    st.info(f"AI Estimate: **{round(total_water / 5, 2)} Million Liters** of water recovered in this sector through reduced evaporative demand.")
    st.bar_chart(df.set_index('name')['delta'])

with tab3:
    st.subheader("🛰️ Sentinel Intelligence: Automated Auditing")
    st.write("Using simulated Sentinel-3 Thermal Infrared data to detect policy violations.")
    # Show "Hot Spots" - areas where Albedo is low despite mandates
    anomalies = pd.DataFrame({"Zone": ["Industrial Area A", "Sector 12", "Truck Terminal"], "Heat Index": [48.2, 45.6, 49.1], "Compliance": ["❌ VIOLATION", "✅ OK", "⚠️ WARNING"]})
    st.table(anomalies)
    

with tab4:
    st.subheader("State Strategic Mandate")
    

[Image of hydrogen fuel cell]

    brief = f"STATE DECREE: {selected_focus.upper()}\n- Target Mitigation: -{round(df[df['name']==selected_focus]['delta'].values[0], 1)}C\n- V2G Requirement: 15% EV Discharge\n- Status: READY"
    st.text_area("Official Script", brief, height=150)
    st.download_button("Export Brief", brief)

if st.button("🚀 EXECUTE STATE PROTOCOL"):
    st.balloons()
    st.success("State-Wide Sovereign Protocol Engaged.")
