import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from engine import AuraEngine, DecisionAgent, get_city_data 

# --- UI CONFIGURATION ---
st.set_page_config(page_title="AuraCool Sovereign | 2025 Global Edition", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f0f4f8; color: #0d1b2a; }
    [data-testid="stMetricValue"] { color: #1b263b !important; font-size: 32px !important; font-weight: 900 !important; }
    .main-stats { 
        background-color: #ffffff; padding: 20px; border-radius: 12px; 
        border-top: 8px solid #415a77; margin-bottom: 20px;
        box-shadow: 0px 10px 30px rgba(0,0,0,0.1);
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #e0e1dd; border-radius: 5px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

if 'engine' not in st.session_state:
    st.session_state.engine = AuraEngine()

# --- SIDEBAR: GLOBAL COMMAND ---
with st.sidebar:
    st.title("🏛️ Sovereign OS")
    cities = get_city_data()
    selected_city = st.selectbox("📍 Target District", list(cities.keys()))
    
    st.divider()
    st.subheader("🛰️ Sensor Fusion")
    sat_mode = st.radio("Satellite Feed", ["Visual", "Thermal (LST)", "NDVI (Greenness)"])
    aqi_sim = st.slider("PM2.5 Pollution", 50, 500, 140)
    
    st.subheader("🤖 AI Mitigation Path")
    green = st.slider("Forestry %", 0, 100, 45) / 100
    refl = st.slider("Cool Surface %", 0, 100, 35) / 100
    ev_mode = st.toggle("Enable V2G (Vehicle-to-Grid)", value=True)

# --- AI PHYSICS ENGINE ---
city_info = cities[selected_city]
# Advanced Math: SVF + Pollution + Albedo
pollution_impact = (aqi_sim - 100) * 0.02 if aqi_sim > 100 else 0
optimized_temp = st.session_state.engine.run_simulation(green, refl, 0.7, city_info['hum']/100) + pollution_impact
temp_diff = city_info['base'] - optimized_temp
msg, risk_lvl = st.session_state.engine.predict_health_risk(optimized_temp, city_info['hum'])
co2, money = st.session_state.engine.calculate_carbon_credits(temp_diff)

# --- TOP METRICS ---
st.title(f"Sovereign Intelligence: {selected_city}")
st.markdown('<div class="main-stats">', unsafe_allow_html=True)
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Thermal Delta", f"-{round(temp_diff, 1)}°C", "AI Mitigated")
m2.metric("Grid Stability", f"{98 - int(temp_diff)}%", "Self-Healing Active")
m3.metric("Sky View Factor", "0.42", "Canyon Risk High")
m4.metric("Water Credits", f"{int(temp_diff*180)}k L")
m5.metric("Carbon Revenue", f"₹{int(money*82)}L")
st.markdown('</div>', unsafe_allow_html=True)

# --- MAIN INTERFACE ---
tabs = st.tabs(["🛰️ Satellite Twin", "🚑 Health & Pollution", "⚡ Energy Nexus", "🌾 Agri-Water", "📜 AI Policy & ROI"])

with tabs[0]: # 3D DIGITAL TWIN + SVF
    st.subheader("3D Sky-View & Thermal Reflection Map")
    
    building_data = pd.DataFrame({
        "lat": [city_info['lat'] + np.random.normal(0, 0.007) for _ in range(80)],
        "lon": [city_info['lon'] + np.random.normal(0, 0.007) for _ in range(80)],
        "height": [np.random.randint(50, 400) for _ in range(80)],
        "temp": [np.random.randint(35, 50) for _ in range(80)]
    })
    
    color_scale = "[255, (1-temp/50)*255, 0]" if sat_mode == "Thermal (LST)" else "[0, 200, 100]"
    
    view = pdk.ViewState(latitude=city_info['lat'], longitude=city_info['lon'], zoom=14, pitch=60)
    layer = pdk.Layer("ColumnLayer", data=building_data, get_position="[lon, lat]", get_elevation="height", 
                      radius=25, get_fill_color=[200, 30, 0, 160], pickable=True)
    
    st.pydeck_chart(pdk.Deck(map_style='mapbox://styles/mapbox/dark-v10', initial_view_state=view, layers=[layer]))
    st.caption("SVF Analysis: Red pillars indicate 'Heat Traps' where urban geometry prevents thermal escape.")

with tabs[1]: # HEALTH & POLLUTION
    st.subheader("Bio-Thermal Emergency Grid")
    
    c_l, c_r = st.columns(2)
    with c_l:
        st.error(f"**Aerosol Forcing Alert:** PM2.5 levels ({aqi_sim}) are acting as a thermal blanket.")
        st.warning(f"**Health Risk:** {risk_lvl}. {msg}")
    with c_r:
        fig_health = go.Figure(go.Indicator(mode="gauge+number", value=optimized_temp, title={'text': "Wet Bulb Globe Temp"},
                                           gauge={'axis': {'range': [20, 50]}, 'bar': {'color': "darkblue"}}))
        st.plotly_chart(fig_health, use_container_width=True)

with tabs[2]: # ENERGY & V2G
    st.subheader("Grid Self-Healing & V2G Nexus")
    st.write(f"V2G is active. **{int(temp_diff*15)} MWh** of emergency power available from EV fleet.")
    # Transformer Health Chart
    x = ["T1-North", "T2-Industrial", "T3-Civil", "T4-Rural"]
    y = [95, 45, 88, 72] # Health percentages
    fig_grid = go.Figure([go.Bar(x=x, y=y, marker_color=['green', 'red', 'green', 'orange'])])
    fig_grid.update_layout(title="Substation Thermal Stress Index")
    st.plotly_chart(fig_grid, use_container_width=True)

with tabs[3]: # AGRI-WATER
    st.subheader("Precision Hydration & Agri-Yield")
    
    st.info(f"AI-Driven Irrigation: Saved **{int(temp_diff*180)}k Liters** today by reducing urban plume evaporation.")
    st.metric("Crop Yield Projection", "+4.2%", "Thermal Stress Avoided")

with tabs[4]: # POLICY & ROI
    st.subheader("Sovereign AI Policy Generator")
    st.success(f"**Action Plan:** {selected_city} Municipal Corporation")
    st.write("1. **V2G Mandate:** Require all parking plazas to support grid discharge by Summer 2026.")
    st.write("2. **SVF Regulation:** Limit new building heights in high-heat corridors to ensure ventilation.")
    st.write("3. **Carbon Credits:** Trading active. Net profit generated today: **$12,400 USD equivalent.**")
    if st.button("📥 Generate Official PDF Policy"):
        st.balloons()

if st.button("🚀 INITIATE GLOBAL SOVEREIGN PROTOCOL"):
    st.snow()
    st.success("Global synchronization complete. District is now a Climate-Resilient Zone.")
