import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
from engine import SovereignEngine, get_sector_data

st.set_page_config(page_title="AURAMASTER SOVEREIGN", layout="wide", page_icon="🛡️")

if 'engine' not in st.session_state:
    st.session_state.engine = SovereignEngine()

sectors = get_sector_data()

st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; }
    [data-testid="stMetricValue"] { font-size: 28px; color: #1e3a8a !important; font-weight: 800; }
    .status-card { background: #1e293b; color: #38bdf8; padding: 20px; border-radius: 12px; border-top: 6px solid #ef4444; font-family: monospace; }
    .intervention-box { background: white; border: 1px solid #e2e8f0; padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ AuraMaster: Sovereign Urban Command")
st.write("Projecting Thermal Defense Strategies for the State of Punjab")

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
    st.subheader("📡 Live Thermal Digital Twin")
    view = pdk.ViewState(latitude=s['lat'], longitude=s['lon'], zoom=11, pitch=45)
    map_data = pd.DataFrame({
        "lat": [s['lat'] + np.random.normal(0, 0.012) for _ in range(150)],
        "lon": [s['lon'] + np.random.normal(0, 0.012) for _ in range(150)],
        "heat": [np.random.randint(100, 700) for _ in range(150)]
    })
    layer = pdk.Layer("ColumnLayer", data=map_data, get_position="[lon, lat]", get_elevation="heat", radius=100, get_fill_color="[220, 38, 38, 160]")
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view))

st.divider()

t1, t2, t3, t4 = st.tabs(["⚡ GRID (V2G)", "💧 WATER NEXUS", "🚑 LABOR PROTECTION", "🛰️ COMPLIANCE"])

with t1:
    st.subheader("Virtual Power Plant: Grid Resilience")
    st.metric("V2G Relief Available", f"{mwh} MWh")
    st.write("Using EV batteries to stabilize the grid during extreme heat events.")

with t2:
    st.subheader("Agricultural Hydro-Thermal Recovery")
    st.metric("Water Preserved", f"{water} Million Liters")
    st.write("Groundwater saved by urban cooling (reduced evaporation flux).")

with t3:
    st.subheader("🚑 Physiological Survival Limits")
    c1, c2 = st.columns(2)
    c1.metric("Survival Status", status)
    c2.metric("Work-Rest Cycle", work_ratio)
    st.warning(f"**Bio-Advisory:** {health_advice}")

with t4:
    st.subheader("Autonomous Sentinel Audit")
    st.markdown(f"""<div class="status-card">> SCANNING: {sector_name.upper()}...<br>> SOURCE: Sentinel-3 LST IR Data...<br>> STATUS: Anomaly detected in industrial cluster.<br>> ACTION: Mandate issued.</div>""", unsafe_allow_html=True)

if st.button("🚀 EXECUTE SOVEREIGN PROTOCOL"):
    st.balloons()
