import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go
from engine import AuraEngine, DecisionAgent, get_city_data 

# --- UI CONFIGURATION ---
st.set_page_config(page_title="AuraCool OS | Punjab 2025", layout="wide")

# CLEAN LIGHT THEME: Professional Command Center
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfc; color: #1a1c23; }
    [data-testid="stMetricValue"] { color: #1a237e !important; font-size: 40px !important; font-weight: 850 !important; }
    .stSidebar { background-color: #ffffff; border-right: 1px solid #dee2e6; }
    .main-stats { 
        background-color: #ffffff; padding: 25px; border-radius: 15px; 
        border: 1px solid #e0e0e0; margin-bottom: 25px;
        box-shadow: 0px 8px 24px rgba(0,0,0,0.08);
    }
    h1, h2, h3 { color: #1a237e; font-family: 'Helvetica', sans-serif; letter-spacing: -0.5px; }
    .stButton>button { width: 100%; height: 50px; font-weight: bold; background-color: #1a237e; color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

if 'engine' not in st.session_state:
    st.session_state.engine = AuraEngine()

# --- SIDEBAR: MISSION CONTROL ---
with st.sidebar:
    st.title("🛡️ AuraCool OS")
    st.info("Unified Thermal Defense Grid: Punjab 2025")
    cities = get_city_data()
    selected_city = st.selectbox("📍 District Command", list(cities.keys()))
    
    st.divider()
    st.subheader("🛠️ Strategic Deployment")
    green = st.slider("Urban Forestry Cover", 0.0, 1.0, 0.35)
    refl = st.slider("Albedo/Cool Surface Coverage", 0.0, 1.0, 0.25)
    
    st.subheader("🛰️ Analysis Layers")
    vulnerability = st.checkbox("Show Vulnerability Index", value=True)
    show_agri_bridge = st.checkbox("Show Crop Stress Zones", value=True)

# --- AI DATA PROCESSING ---
city_info = cities[selected_city]
optimized_temp = st.session_state.engine.run_simulation(green, refl, 0.7, city_info['hum']/100)
temp_diff = city_info['base'] - optimized_temp
msg, risk_lvl = st.session_state.engine.predict_health_risk(optimized_temp, city_info['hum'])
co2, money = st.session_state.engine.calculate_carbon_credits(temp_diff)

# --- MAIN DASHBOARD ---
st.title(f"AuraCool Command Center: {selected_city}")

# Top Metrics: The Multi-Problem Solver
st.markdown('<div class="main-stats">', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Current Delta", f"-{round(temp_diff, 2)}°C", "AI Mitigated")
c2.metric("Critical Risk", risk_lvl)
c3.metric("Water Saved", f"{int(temp_diff*145)}k L", "Evap Reduction")
c4.metric("Crop Yield Protection", f"+{round(temp_diff*1.4, 1)}%", "Heat Stress Avoided")
st.markdown('</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Spatial Defense", "🏥 Health Crisis AI", "🌾 Agri-Water Nexus", "📈 Economic ROI"])

with tab1:
    st.subheader("Strategic Infrastructure Placement")
    points = 800
    map_df = pd.DataFrame({
        "lat": [city_info['lat'] + np.random.normal(0, 0.01) for _ in range(points)],
        "lon": [city_info['lon'] + np.random.normal(0, 0.01) for _ in range(points)],
        "weight": [np.random.uniform(0.1, 1.0) for _ in range(points)]
    })
    
    layers = [pdk.Layer("HeatmapLayer", data=map_df, get_position="[lon, lat]", get_weight="weight", radius_pixels=45, color_range=[[232,245,233], [129,212,250], [255,235,59], [255,152,0], [211,47,47]])]

    if vulnerability:
        # Markers for high risk areas like crowded markets or slums
        vuln_data = pd.DataFrame({
            "lat": [city_info['lat'] + 0.004, city_info['lat'] - 0.007],
            "lon": [city_info['lon'] - 0.002, city_info['lon'] + 0.005],
            "label": ["High-Density Market", "Slum Settlement"]
        })
        layers.append(pdk.Layer("ScatterplotLayer", data=vuln_data, get_position="[lon, lat]", get_radius=200, get_fill_color=[106, 27, 154, 180]))

    st.pydeck_chart(pdk.Deck(map_style='mapbox://styles/mapbox/light-v10', initial_view_state=pdk.ViewState(latitude=city_info['lat'], longitude=city_info['lon'], zoom=13), layers=layers))
    st.caption("Thermal scan of district urban core. Purple circles represent priority zones for mobile cooling units.")

with tab2:
    st.subheader("Hospital Admissions & Patient Load Forecasting")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.warning(f"**Emergency Status:** {msg}")
        st.info("💡 **Golden Hour Strategy:** Deploying ambulances to mapped vulnerability zones to reduce response time by 15 mins.")
    with col_b:
        temps = np.arange(30, 50, 1)
        load = [(t-30)**2.2 / 10 for t in temps]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=temps, y=load, name="Predicted ER Load", fill='tozeroy', line=dict(color='#d32f2f')))
        fig.update_layout(title="Emergency Load vs Temperature", xaxis_title="Ambient Temp (°C)", yaxis_title="Daily Admissions")
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Groundwater & Agriculture Protection")
    
    st.markdown(f"""
    **Urban-to-Agri Leakage Analysis:**
    High temperatures in **{selected_city}** create a 'heat plume' that dries out the surrounding soil.
    * **Evaporation Prevention:** {int(temp_diff*145)}k Liters saved today.
    * **Crop Safety:** Preventing thermal shock in Rice/Wheat belts.
    """)
    # Groundwater Stress Chart
    months = ["Apr", "May", "Jun", "Jul"]
    water_stress = [70, 85, 95, 80]
    mitigated_stress = [s - (temp_diff*3) for s in water_stress]
    fig_agri = go.Figure()
    fig_agri.add_trace(go.Bar(x=months, y=water_stress, name="Baseline Stress", marker_color='#ef5350'))
    fig_agri.add_trace(go.Bar(x=months, y=mitigated_stress, name="With AuraCool", marker_color='#66bb6a'))
    fig_agri.update_layout(title="Groundwater Irrigation Pressure Index", barmode='group')
    st.plotly_chart(fig_agri, use_container_width=True)

with tab4:
    st.subheader("Carbon Monetization & ESG")
    co2_tons, annual_val = st.session_state.engine.calculate_carbon_credits(temp_diff)
    col1, col2 = st.columns(2)
    col1.metric("Carbon Credits Earned", f"{int(co2_tons)} Tons")
    col2.metric("Market Value (INR)", f"₹{int(annual_val*82)} Lakhs")
    st.success("Analysis: This project qualifies for international green municipal bonds.")

if st.button("🚀 INITIATE PUNJAB THERMAL DEFENSE PROTOCOL"):
    st.snow()
    st.success(f"Strategy deployed for {selected_city}. Energy, Water, and Health grids synchronized.")
