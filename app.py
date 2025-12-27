import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
from engine import AuraEngine

# --- APP CONFIGURATION ---
st.set_page_config(page_title="AURAMASTER | Punjab State Command", layout="wide")

# Gov-Tech High Visibility Theme
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

# --- LIVE INTELLIGENCE TICKER ---
st.markdown(f"""
    <div class="news-ticker">
        🌍 STATE COMMAND: Monitoring 5 Strategic Districts | 
        🛰️ SATELLITE: Punjab Thermal Grid Synchronized | 
        ⚡ V2G: Virtual Power Plant Capacity at 84%
    </div>
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

# --- SIDEBAR CONTROL ---
with st.sidebar:
    st.header("⚙️ State-Level Parameters")
    cities = get_state_data()
    st.write("Adjusting these sliders simulates a state-wide infrastructure rollout.")
    green = st.slider("Urban Canopy expansion (%)", 0.0, 1.0, 0.35)
    albedo = st.slider("Cool Surface Coating (%)", 0.0, 1.0, 0.25)
    aqi = st.slider("Atmospheric AQI", 50, 500, 160)
    
    st.divider()
    selected_focus = st.selectbox("Detailed Sector Analysis", list(cities.keys()))

# --- STATE-WIDE DATA PROCESSING ---
state_list = []
total_revenue = 0
total_mwh = 0

for name, data in cities.items():
    # Calculate optimized metrics for each city
    opt_temp = st.session_state.engine.run_simulation(green, albedo, data['hum'], data['base'])
    delta = data['base'] - opt_temp
    mwh, revenue_cr = st.session_state.engine.calculate_v2g_revenue(delta)
    
    total_revenue += revenue_cr
    total_mwh += mwh
    
    # Prepare data for the 3D Map
    state_list.append({
        "name": name,
        "lat": data['lat'],
        "lon": data['lon'],
        "temp": opt_temp,
        "delta": delta,
        "height": opt_temp * 500, # Height represents heat intensity
        "color": [255, int(255 - (delta * 20)), 0, 200] # Redder = Hotter
    })

df = pd.DataFrame(state_list)
focus_city = df[df['name'] == selected_focus].iloc[0]

# --- MAIN DASHBOARD ---
st.title("Punjab State Thermal Defense Command")

# State-Wide Metrics
c1, c2, c3, c4 = st.columns(4)
c1.metric("State Avg. Temp", f"{round(df['temp'].mean(), 1)}°C")
c2.metric("Total Grid Relief", f"{round(total_mwh, 1)} MWh")
c3.metric("State ROI", f"₹{round(total_revenue, 2)} Cr")
c4.metric("Active Sectors", len(cities))

st.divider()

# --- 3D STATE MAP ---
st.subheader("State-Wide 3D Thermal Digital Twin")
st.write("Visualizing all strategic sectors. Pillar height represents heat intensity; color shift indicates cooling efficacy.")

view = pdk.ViewState(latitude=31.0, longitude=75.4, zoom=6.8, pitch=45)

layer = pdk.Layer(
    "ColumnLayer",
    data=df,
    get_position="[lon, lat]",
    get_elevation="height",
    radius=8000,
    get_fill_color="color",
    pickable=True,
    auto_highlight=True,
)

st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view,
    tooltip={"text": "{name}\nCurrent Temp: {temp}°C\nReduction: -{delta}°C"}
))

# --- DETAIL TABS ---
t1, t2 = st.tabs(["📊 Sector Breakdown", "📜 Policy Manifest"])

with t1:
    col_a, col_b = st.columns(2)
    with col_a:
        st.write(f"### Economic Impact: {selected_focus}")
        st.bar_chart(df.set_index('name')[['temp', 'delta']])
    with col_b:
        st.write("### Grid Energy Arbitrage")
        st.line_chart(np.random.randn(10, 2)) # Simulated grid stability

with t2:
    brief = f"""
    STATE POLICY DECREE - PUNJAB CLIMATE UNIT
    -------------------------------------------
    SECTOR: {selected_focus.upper()}
    ESTIMATED REVENUE: ₹{round(total_revenue/len(cities), 2)} Cr
    
    ACTION PLAN:
    - Deploy Albedo-Force coatings state-wide.
    - Synchronize V2G battery discharge across NH-44 corridor.
    """
    st.text_area("State Mandate", brief, height=150)
    st.download_button("📥 Export Punjab State Policy", brief, file_name="Punjab_State_Policy.txt")

# --- EXECUTION ---
if st.button("🚀 EXECUTE STATE-WIDE SOVEREIGN PROTOCOL"):
    with st.spinner("Synchronizing Punjab State Grid..."):
        time.sleep(2)
        st.balloons()
        st.success("Sovereign Protocol Active. Punjab State is now in Autonomous Cooling Mode.")
