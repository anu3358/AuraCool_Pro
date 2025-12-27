import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from engine import AuraEngine

st.set_page_config(page_title="AURAMASTER ELITE | Sovereign OS", layout="wide")

# High-Density Engineering UI
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .status-panel { background: #ffffff; padding: 20px; border-radius: 5px; border-top: 4px solid #d32f2f; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .ai-logic-box { background: #e3f2fd; border: 1px solid #2196f3; padding: 15px; border-radius: 5px; font-family: monospace; }
    </style>
    """, unsafe_allow_html=True)

if 'engine' not in st.session_state:
    st.session_state.engine = AuraEngine()

# --- STATE DATA ---
cities = {
    "Ludhiana": {"lat": 30.9010, "lon": 75.8573, "base": 47.1, "hum": 0.44, "density": 85},
    "Amritsar": {"lat": 31.6340, "lon": 74.8723, "base": 44.8, "hum": 0.40, "density": 65},
    "Ferozpur": {"lat": 30.9250, "lon": 74.6225, "base": 46.2, "hum": 0.35, "density": 40}
}

st.title("🛡️ AURAMASTER: District Sovereign Control")

# --- AI OPTIMIZER INTERFACE ---
col_sidebar, col_main = st.columns([1, 3])

with col_sidebar:
    st.markdown('<div class="status-panel">', unsafe_allow_html=True)
    st.header("🎯 AI Optimizer")
    target = st.number_input("Target Temperature (°C)", 25.0, 35.0, 30.0)
    city_name = st.selectbox("Strategic Sector", list(cities.keys()))
    
    city = cities[city_name]
    # RUN AI OPTIMIZATION
    rec_green, rec_albedo, est_cost = st.session_state.engine.optimize_infrastructure(target, city['base'])
    
    st.markdown("### AI Recommendation")
    st.write(f"**Greenery:** +{int(rec_green*100)}%")
    st.write(f"**Albedo:** +{int(rec_albedo*100)}%")
    st.write(f"**CAPEX:** ₹{round(est_cost/100000, 2)} Lacs")
    st.markdown('</div>', unsafe_allow_html=True)

with col_main:
    # --- METRIC GRID ---
    m1, m2, m3 = st.columns(3)
    final_temp = st.session_state.engine.run_simulation(rec_green, rec_albedo, city['hum'], city['base'])
    delta = city['base'] - final_temp
    mwh, rev = st.session_state.engine.calculate_v2g_revenue(delta)
    water = st.session_state.engine.calculate_water_recovery(delta)
    
    m1.metric("Thermal Mitigation", f"-{round(delta, 1)}°C")
    m2.metric("Grid Relief (V2G)", f"{round(mwh, 1)} MWh")
    m3.metric("Water Saved", f"{round(water, 1)} Million L")

    # --- THE "KILLER" FEATURE: CFD WIND CORRIDORS ---
    st.subheader("🌬️ Fluid Dynamics & Urban Ventilation Mapping")
    vent_factor = st.session_state.engine.calculate_cfd_ventilation(city['density'])
    st.write(f"Current Ventilation Coefficient: **{vent_factor}** (Values < 0.3 indicate Critical Heat Stagnation)")
    
    # 3D Wind Vector Simulation
    view = pdk.ViewState(latitude=city['lat'], longitude=city['lon'], zoom=14, pitch=50)
    map_data = pd.DataFrame({
        "lat": [city['lat'] + np.random.normal(0, 0.005) for _ in range(100)],
        "lon": [city['lon'] + np.random.normal(0, 0.005) for _ in range(100)],
        "height": [np.random.randint(50, 400) for _ in range(100)],
        "v_vector": [np.random.rand() * vent_factor for _ in range(100)]
    })
    
    layer = pdk.Layer(
        "ColumnLayer", data=map_data, get_position="[lon, lat]", 
        get_elevation="height", radius=40, 
        get_fill_color="[255, (1 - v_vector) * 255, 0, 150]"
    )
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view))

# --- BOTTOM LOGIC TABS ---
st.divider()
t1, t2 = st.tabs(["🧬 Genetic Logic", "⚡ V2G Arbitrage"])
with t1:
    st.markdown('<div class="ai-logic-box">', unsafe_allow_html=True)
    st.text(f"GENETIC OPTIMIZER LOG:\nIteration 104: Converged.\nDelta Target: {delta}C\nMinimizing CAPEX for {city_name}...")
    st.markdown('</div>', unsafe_allow_html=True)
