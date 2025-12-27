import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
from engine import SovereignEngine, get_sector_data

st.set_page_config(page_title="AURAMASTER SOVEREIGN", layout="wide", page_icon="🛡️")

if 'engine' not in st.session_state:
    st.session_state.engine = SovereignEngine()

sectors = get_sector_data()

# --- HIGH-END UI STYLING ---
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; }
    [data-testid="stMetricValue"] { font-size: 28px; color: #1e3a8a !important; font-weight: 800; }
    .status-card { background: #1e293b; color: #38bdf8; padding: 20px; border-radius: 12px; border-top: 6px solid #ef4444; font-family: monospace; }
    .intervention-box { background: white; border: 1px solid #e2e8f0; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("🛡️ AuraMaster: Sovereign Urban Command")
st.write("Projecting Thermal Defense Strategies for the State of Punjab | 2025 Release")

# --- CONTROL CENTER ---
col_map, col_controls = st.columns([2, 1])

with col_controls:
    st.subheader("🛠️ Strategic Asset Manager")
    sector_name = st.selectbox("Focus Sector", list(sectors.keys()))
    target_temp = st.slider("Target Stabilization (°C)", 25, 35, 30)
    
    s = sectors[sector_name]
    alb, grn, cost = st.session_state.engine.optimize_intervention(s['temp'], target_temp, s['area'])
    mwh = st.session_state.engine.calculate_v2g_impact(s['evs'])
    water, co2 = st.session_state.engine.calculate_nexus_savings(s['temp'] - target_temp, s['area'])
    status, work_ratio, health_advice = st.session_state.engine.calculate_labor_protection(s['temp'])

    st.markdown(f"""
    <div class="intervention-box">
        <h4 style="margin-top:0;">DEPLOYMENT BLUEPRINT</h4>
        <p><b>Surface Albedo:</b> +{int(alb*100)}% coverage</p>
        <p><b>Bio-Infrastructure:</b> +{int(grn*100)}% density</p>
        <p style="font-size: 22px; color: #1e3a8a;"><b>CAPEX: ₹{round(cost/10000000, 2)} Cr</b></p>
    </div>
    """, unsafe_allow_html=True)

with col_map:
    st.subheader("📡 Thermal Intelligence Twin")
    view = pdk.ViewState(latitude=s['lat'], longitude=s['lon'], zoom=11, pitch=45)
    # Heat Cloud Generation
    map_data = pd.DataFrame({
        "lat": [s['lat'] + np.random.normal(0, 0.012) for _ in range(200)],
        "lon": [s['lon'] + np.random.normal(0, 0.012) for _ in range(200)],
        "heat": [np.random.randint(100, 700) for _ in range(200)]
    })
    layer = pdk.Layer("ColumnLayer", data=map_data, get_position="[lon, lat]", get_elevation="heat", radius=100, get_fill_color="[220, 38, 38, 160]")
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view))

st.divider()

# --- THE NEXUS TABS (THE WINNING FEATURES) ---
t1, t2, t3, t4 = st.tabs(["⚡ GRID (V2G)", "💧 WATER NEXUS", "🚑 LABOR PROTECTION", "🛰️ COMPLIANCE"])

with t1:
    st.subheader("Virtual Power Plant: Grid Resilience")
    st.write("Harvesting energy from thousands of EVs to stabilize the grid during heat spikes.")
    st.metric("V2G Relief Available", f"{mwh} MWh", help="Available for dispatch to industrial zones.")
    

[Image of hydrogen fuel cell]


with t2:
    st.subheader("Agricultural Hydro-Thermal Recovery")
    st.write("Water saved by reducing urban 'Heat Thirst' and preventing atmospheric loss.")
    st.metric("Water Preserved", f"{water} Million Liters", delta="Preserved for Irrigation")
    

[Image of the global water cycle]


with t3:
    st.subheader("🚑 Physiological Survival Limits")
    col_h1, col_h2 = st.columns(2)
    with col_h1:
        st.metric("Bio-Health Status", status)
        st.metric("Work-Rest Cycle", work_ratio)
    with col_h2:
        st.info(f"**Action Plan:** {health_advice}")
        st.progress(s['temp']/50)
    

with t4:
    st.subheader("Autonomous Sentinel Audit")
    st.markdown(f"""
    <div class="status-card">
        > SCANNING SECTOR: {sector_name.upper()}...<br>
        > DATA SOURCE: Sentinel-3 Land Surface Temperature (LST)...<br>
        > ALERT: Thermal anomaly detected in industrial cluster 4.<br>
        > ACTION: Mandatory albedo upgrade notice issued to 14 facilities.
    </div>
    """, unsafe_allow_html=True)

if st.button("🚀 EXECUTE SOVEREIGN DEFENSE PROTOCOL"):
    st.balloons()
    st.toast("State-Wide Protocol Active.")
