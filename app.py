import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
from engine import SovereignEngine, get_sector_data

st.set_page_config(page_title="AURAMASTER SOVEREIGN", layout="wide")

# Ensure the Engine is initialized correctly in session state
if 'engine' not in st.session_state:
    st.session_state.engine = SovereignEngine()

sectors = get_sector_data()

# --- HEADER & UI ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .status-card { background: white; padding: 20px; border-radius: 10px; border-left: 8px solid #0056b3; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ SOVEREIGN CLIMATE OS: PUNJAB DEFENSE GRID")

col_ctrl, col_map = st.columns([1, 2])

with col_ctrl:
    st.subheader("🛠️ Autonomous Optimization")
    selected_name = st.selectbox("Sector Focus", list(sectors.keys()))
    target_temp = st.slider("Target Stabilization (°C)", 28, 35, 31)
    
    sector = sectors[selected_name]
    
    # Call the engine
    alb, grn, cost = st.session_state.engine.optimize_intervention(sector['temp'], target_temp, sector['area'])
    v2g_mwh = st.session_state.engine.calculate_v2g_capacity(sector['evs'])
    water, co2 = st.session_state.engine.calculate_resource_nexus(sector['temp'] - target_temp, sector['area'])

    st.markdown(f"""
    <div class="status-card">
        <h4>AI DEPLOYMENT STRATEGY</h4>
        <p><b>Surface Albedo:</b> +{int(alb*100)}% Coverage</p>
        <p><b>Bio-Infrastructure:</b> +{int(grn*100)}% Density</p>
        <hr>
        <p><b>Total CAPEX:</b> ₹{round(cost/10000000, 2)} Cr</p>
    </div>
    """, unsafe_allow_html=True)

with col_map:
    st.subheader("📡 Thermal Intelligence (Live)")
    view = pdk.ViewState(latitude=sector['lat'], longitude=sector['lon'], zoom=11, pitch=45)
    map_data = pd.DataFrame({
        "lat": [sector['lat'] + np.random.normal(0, 0.01) for _ in range(100)],
        "lon": [sector['lon'] + np.random.normal(0, 0.01) for _ in range(100)],
        "heat": [np.random.randint(100, 500) for _ in range(100)]
    })
    layer = pdk.Layer("ColumnLayer", data=map_data, get_position="[lon, lat]", get_elevation="heat", radius=100, get_fill_color="[255, 70, 0, 180]")
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view))

# --- THE PROBLEM-SOLVER TABS ---
t1, t2, t3 = st.tabs(["⚡ GRID STABILITY", "💧 RESOURCE NEXUS", "🚑 BIO-HEALTH RISK"])

with t1:
    st.metric("V2G Energy Buffer", f"{v2g_mwh} MWh")
    st.write("Using EV batteries to prevent Ludhiana's industrial grid from collapsing.")
    

[Image of hydrogen fuel cell]


with t2:
    st.metric("Water Preserved", f"{water} Million Liters")
    st.write("Groundwater saved for Punjab agriculture by urban thermal cooling.")
    

[Image of the global water cycle]


with t3:
    st.subheader("Thermal Physiological Stress Index")
    st.write("Analyzing the 'Wet Bulb' threshold for the local labor force.")
    
    if sector['temp'] > 45:
        st.error("CRITICAL: Mortality risk for outdoor workers is high. Mitigation protocol required.")
    else:
        st.success("STABLE: Thermal levels within physiological safety limits.")
