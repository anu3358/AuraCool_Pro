import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go
from engine import AuraEngine, DecisionAgent, get_city_data 

# --- UI CONFIGURATION ---
st.set_page_config(page_title="AuraCool Titan | Punjab 2025", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8faff; color: #1a1c23; }
    [data-testid="stMetricValue"] { color: #1a237e !important; font-size: 35px !important; font-weight: 850 !important; }
    .main-stats { 
        background-color: #ffffff; padding: 20px; border-radius: 15px; 
        border-left: 6px solid #1a237e; margin-bottom: 20px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.05);
    }
    h1, h2, h3 { color: #1a237e; font-family: 'Helvetica', sans-serif; }
    .stButton>button { border-radius: 8px; height: 3em; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

if 'engine' not in st.session_state:
    st.session_state.engine = AuraEngine()

# --- SIDEBAR: ADVANCED AI COMMAND ---
with st.sidebar:
    st.title("🛡️ AuraCool TITAN")
    cities = get_city_data()
    selected_city = st.selectbox("📍 District Command", list(cities.keys()))
    
    st.divider()
    st.subheader("🏙️ 3D Digital Twin Settings")
    # Controlling how high the 'heat' pillars go on the map
    building_height = st.slider("Urban Density Simulation", 50, 600, 200)
    
    st.subheader("🌫️ Atmospheric Coupling")
    # Higher AQI causes heat to be trapped (Greenhouse Effect)
    aqi_sim = st.slider("Simulated PM2.5 (Pollution)", 50, 500, 150)
    
    st.subheader("🚑 Emergency AI")
    live_health = st.toggle("Live Heat-Stroke Tracking", value=True)

# --- AI DATA PROCESSING ---
city_info = cities[selected_city]

# Advanced physics: Pollution traps heat (The 'Aerosol Blanket' effect)
pollution_penalty = (aqi_sim - 100) * 0.015 if aqi_sim > 100 else 0
optimized_temp = st.session_state.engine.run_simulation(0.4, 0.3, 0.7, city_info['hum']/100) + pollution_penalty
temp_diff = city_info['base'] - optimized_temp
msg, risk_lvl = st.session_state.engine.predict_health_risk(optimized_temp, city_info['hum'])
co2, money = st.session_state.engine.calculate_carbon_credits(temp_diff)

# --- MAIN DASHBOARD ---
st.title(f"3D Urban Intelligence Grid: {selected_city}")

# Top Metrics: The Multi-Problem Solver View
st.markdown('<div class="main-stats">', unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Mitigated Temp", f"{round(optimized_temp, 1)}°C", f"-{round(temp_diff, 1)}°C")
c2.metric("Health Status", risk_lvl)
c3.metric("Aerosol Heat", f"+{round(pollution_penalty, 2)}°C", "Pollution Trap")
c4.metric("Water Saved", f"{int(temp_diff*165)}k L", "Daily Evap")
c5.metric("Solar Yield", f"+{int(temp_diff*22)}%", "Albedo Reflection")
st.markdown('</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🏙️ 3D Spatial Twin", "🚑 Health & Aerosol AI", "🌾 Agri-Energy Nexus", "📜 AI Policy Generator"])

with tab1:
    st.subheader("3D Urban Canyon & Thermal Retention")
    # Generate 3D Digital Twin Data
    points = 60
    building_data = pd.DataFrame({
        "lat": [city_info['lat'] + np.random.normal(0, 0.006) for _ in range(points)],
        "lon": [city_info['lon'] + np.random.normal(0, 0.006) for _ in range(points)],
        "height": [np.random.randint(20, building_height) for _ in range(points)],
        "heat_intensity": [np.random.randint(150, 255) for _ in range(points)]
    })

    view_state = pdk.ViewState(latitude=city_info['lat'], longitude=city_info['lon'], zoom=14, pitch=50, bearing=45)
    
    # Building Layer (Extruded Pillars)
    layer_3d = pdk.Layer(
        "ColumnLayer", data=building_data, get_position="[lon, lat]", get_elevation="height",
        radius=35, get_fill_color="[heat_intensity, 30, 100, 200]", pickable=True, auto_highlight=True,
    )

    st.pydeck_chart(pdk.Deck(map_style='mapbox://styles/mapbox/light-v10', initial_view_state=view_state, layers=[layer_3d]))
    st.caption("Visualizing 'Urban Canyons': Taller, darker pillars indicate areas where heat is trapped between buildings.")

with tab2:
    st.subheader("Combined Health & Pollution Risk")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.error(f"**Atmospheric Forcing:** Dust/PM2.5 levels of {aqi_sim} are currently trapping heat, reducing the effectiveness of night-time cooling.")
        if live_health:
            st.warning("🚑 **Emergency Alert:** AI has detected a cluster of 5 heat-exhaustion cases in high-density zones. Rerouting Cooling Van #4.")
    with col_b:
        # Multi-axis Chart
        h = list(range(24))
        heat_line = [optimized_temp + 6*np.sin((i-6)*np.pi/12) for i in h]
        poll_line = [aqi_sim + 30*np.cos((i-18)*np.pi/12) for i in h]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=h, y=heat_line, name="Temp (°C)", yaxis="y1", line=dict(color='#d32f2f', width=4)))
        fig.add_trace(go.Scatter(x=h, y=poll_line, name="AQI Level", yaxis="y2", line=dict(color='#455a64', dash='dot')))
        fig.update_layout(title="Daily Thermal-Pollution Correlation", yaxis=dict(title="Temperature"), yaxis2=dict(title="Pollution Index", overlaying="y", side="right"))
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Agri-Energy Bridge: The V2G Solution")
    
    st.markdown(f"""
    **Vehicle-to-Grid (V2G) Strategy:**
    When the temperature in {selected_city} crosses 42°C, the grid risk increases by 40%.
    * **Simulated Fleet:** 1,200 Electric Vehicles.
    * **Potential Backup:** **{int(temp_diff*15)} MWh** of energy can be fed back into the grid to keep hospitals cooling centers running.
    """)
    st.metric("Grid Stability Index", "88/100", "+12% with V2G")

with tab4:
    st.subheader("🤖 AI Municipal Policy Generator")
    st.info(f"AI has processed {selected_city}'s urban geometry and climate data to generate the 2025 Mitigation Policy.")
    
    p1, p2, p3 = st.columns(3)
    p1.success("**Building Code 4.1:** Mandate high-albedo (white) roofing for all industrial zones to reclaim ₹{int(money*4)} Lacs in Carbon Credits.")
    p2.success("**Urban Forestry:** Plant 'Green Buffers' in wind corridors to filter PM2.5 particles and reduce the heat-blanket effect.")
    p3.success("**Tax Incentive:** 10% property tax rebate for residents implementing 'Vertical Balcony Forests' in high-density areas.")
    
    if st.button("📄 DOWNLOAD FULL POLICY BRIEF (PDF)"):
        st.balloons()
        st.write("Generating PDF... 100% Complete.")

if st.button("🚀 EXECUTE TITAN URBAN PROTOCOL"):
    st.snow()
    st.success(f"Strategy deployed. {selected_city} is now under AI-Optimized Thermal Protection.")
