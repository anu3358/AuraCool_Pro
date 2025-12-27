import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import time
from engine import SovereignEngine, get_sector_data

st.set_page_config(page_title="AURAMASTER SOVEREIGN", layout="wide")

# High-Tech Industrial UI
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; color: #1c1c1c; }
    .status-card { background: white; padding: 20px; border-radius: 10px; border-left: 8px solid #0056b3; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    .protocol-active { background: #e8f5e9; border: 1px solid #2e7d32; padding: 10px; border-radius: 5px; color: #2e7d32; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

if 'engine' not in st.session_state:
    st.session_state.engine = SovereignEngine()

sectors = get_sector_data()

# --- TOP NAVIGATION ---
st.title("🛡️ SOVEREIGN CLIMATE OS: PUNJAB SECTOR")
st.markdown("---")

# --- CONTROL PANEL ---
col_ctrl, col_map = st.columns([1, 2])

with col_ctrl:
    st.subheader("Target Optimization")
    selected_name = st.selectbox("Sector Focus", list(sectors.keys()))
    target_temp = st.slider("Target Stabilization (°C)", 28, 35, 31)
    
    sector = sectors[selected_name]
    alb, grn, cost = st.session_state.engine.optimize_intervention(sector['temp'], target_temp, sector['area'])
    v2g_mwh = st.session_state.engine.calculate_v2g_capacity(sector['evs'])
    water, co2 = st.session_state.engine.calculate_resource_nexus(sector['temp'] - target_temp, sector['area'])

    st.markdown(f"""
    <div class="status-card">
        <h4>AI DEPLOYMENT PLAN</h4>
        <p><b>Albedo Coating:</b> +{int(alb*100)}% Coverage</p>
        <p><b>Green Infrastructure:</b> +{int(grn*100)}% Density</p>
        <hr>
        <p><b>Est. Investment:</b> ₹{round(cost/10000000, 2)} Cr</p>
    </div>
    """, unsafe_allow_html=True)

with col_map:
    st.subheader("Thermal Anomaly Detection")
    # 3D Mapping of the heat island
    view = pdk.ViewState(latitude=sector['lat'], longitude=sector['lon'], zoom=12, pitch=45)
    map_data = pd.DataFrame({
        "lat": [sector['lat'] + np.random.normal(0, 0.01) for _ in range(100)],
        "lon": [sector['lon'] + np.random.normal(0, 0.01) for _ in range(100)],
        "heat": [np.random.randint(100, 500) for _ in range(100)]
    })
    layer = pdk.Layer("ColumnLayer", data=map_data, get_position="[lon, lat]", get_elevation="heat", radius=100, get_fill_color="[255, 100, 0, 160]")
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view))

# --- IMPACT ARBITRAGE TABS ---
st.divider()
t1, t2, t3 = st.tabs(["⚡ V2G GRID ARBITRAGE", "💧 HYDRO-THERMAL NEXUS", "💰 CARBON ROI"])

with t1:
    st.subheader("Virtual Power Plant Synchronization")
    st.metric("V2G Emergency Buffer", f"{v2g_mwh} MWh", help="Energy available from local EVs to prevent brownouts.")
    st.write("This buffer can stabilize the local grid for 4 hours during peak heat without using thermal coal plants.")

with t2:
    st.subheader("Agricultural Water Preservation")
    st.info(f"By cooling the urban sector, we save **{water} Million Liters** of water from evaporative loss.")
    st.write("This directly recharges the local water table, providing relief to the surrounding agricultural belt.")

with t3:
    st.subheader("Financial Performance")
    col_a, col_b = st.columns(2)
    col_a.metric("Carbon Credits (Annual)", f"₹{round(co2 * 2.4, 1)} L")
    col_b.metric("Grid Procurement Savings", f"₹{round(v2g_mwh * 0.8, 1)} L")

if st.button("🔴 INITIATE SOVEREIGN DEFENSE PROTOCOL"):
    st.markdown('<div class="protocol-active">PROTOCOL ENGAGED: Automating cooling dispatch systems...</div>', unsafe_allow_html=True)
    st.snow()
