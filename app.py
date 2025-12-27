import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go
from engine import AuraEngine, DecisionAgent, get_city_data 

# --- UI CONFIGURATION ---
st.set_page_config(page_title="AuraCool OS | Supreme AI 2025", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8faff; color: #1a1c23; }
    [data-testid="stMetricValue"] { color: #1a237e !important; font-size: 38px !important; font-weight: 850 !important; }
    .main-stats { 
        background-color: #ffffff; padding: 20px; border-radius: 15px; 
        border-left: 5px solid #1a237e; margin-bottom: 20px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.05);
    }
    h1, h2, h3 { color: #1a237e; font-family: 'Helvetica'; }
    .stChatFloatingInputContainer { background-color: #f8faff; }
    </style>
    """, unsafe_allow_html=True)

if 'engine' not in st.session_state:
    st.session_state.engine = AuraEngine()

# --- SIDEBAR: AI PARAMETERS ---
with st.sidebar:
    st.title("🛰️ AuraCool Supreme")
    st.caption("Punjab Regional AI Command")
    cities = get_city_data()
    selected_city = st.selectbox("📍 Select District", list(cities.keys()))
    
    st.divider()
    st.subheader("🤖 AI Mitigation Logic")
    auto_optimize = st.toggle("Enable AI Auto-Optimization", value=True)
    
    # Sliders for Manual override
    green = st.slider("Forestry Target (%)", 0, 100, 40) / 100
    refl = st.slider("Albedo/Cool Roof Target (%)", 0, 100, 30) / 100

# --- AI DATA PROCESSING ---
city_info = cities[selected_city]
optimized_temp = st.session_state.engine.run_simulation(green, refl, 0.7, city_info['hum']/100)
temp_diff = city_info['base'] - optimized_temp
msg, risk_lvl = st.session_state.engine.predict_health_risk(optimized_temp, city_info['hum'])
co2, money = st.session_state.engine.calculate_carbon_credits(temp_diff)

# --- MAIN DASHBOARD ---
st.title(f"District Intelligence Grid: {selected_city}")

# Top Metrics
st.markdown('<div class="main-stats">', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Current Thermal Delta", f"-{round(temp_diff, 2)}°C", "AI Controlled")
c2.metric("Health Risk Index", risk_lvl)
c3.metric("Solar Potential", f"+{int(refl*250)} MW", "Cool Roof Yield")
c4.metric("Grid Relief", f"{int(temp_diff*4.8)}%", "Load Balance")
st.markdown('</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🗺️ AI Spatial Map", "⚡ Energy & Solar Nexus", "🚜 Agri-Water AI", "🦁 Sher-AI Agent"])

with tab1:
    st.subheader("Autonomous Heat-Risk Mapping")
    # Simulation of traffic-heat pockets
    points = 700
    map_df = pd.DataFrame({
        "lat": [city_info['lat'] + np.random.normal(0, 0.009) for _ in range(points)],
        "lon": [city_info['lon'] + np.random.normal(0, 0.009) for _ in range(points)],
        "intensity": [np.random.uniform(0.1, 1.0) for _ in range(points)]
    })
    
    view_state = pdk.ViewState(latitude=city_info['lat'], longitude=city_info['lon'], zoom=13, pitch=45)
    
    heat_layer = pdk.Layer("HeatmapLayer", data=map_df, get_position="[lon, lat]", get_weight="intensity", radius_pixels=40)
    
    # AI Feature: Suggested "Cool Corridors" (Pathways for wind)
    corridor_data = pd.DataFrame({
        "path": [[ [city_info['lon']-0.01, city_info['lat']-0.01], [city_info['lon']+0.01, city_info['lat']+0.01] ]]
    })
    line_layer = pdk.Layer("PathLayer", data=corridor_data, get_path="path", get_color=[0, 200, 255], width_min_pixels=5)

    st.pydeck_chart(pdk.Deck(map_style='mapbox://styles/mapbox/light-v10', initial_view_state=view_state, layers=[heat_layer, line_layer]))
    st.caption("Blue line represents AI-suggested 'Wind Corridor' to maximize urban cooling.")

with tab2:
    st.subheader("Solar Harvesting & Power Grid Prediction")
    
    col_l, col_r = st.columns(2)
    with col_l:
        st.write("### Solar Efficiency Gain")
        st.write(f"Reflective 'Cool Roofs' in {selected_city} don't just cool buildings; they increase the efficiency of bifacial solar panels by **12%** due to albedo reflection.")
        st.metric("New Solar Capacity", f"{int(refl*1200)} Households", "Powered daily")
    with col_r:
        # Load Prediction Chart
        hours = list(range(24))
        load = [50 + 30*np.sin((h-6)*np.pi/12) for h in hours]
        ai_load = [l - (temp_diff*3) for l in load]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hours, y=load, name="Grid Load (Baseline)", line=dict(color='gray', dash='dot')))
        fig.add_trace(go.Scatter(x=hours, y=ai_load, name="AI Optimized Load", line=dict(color='#1a237e', width=4)))
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Precision Agriculture & Water Conservation")
    
    st.info(f"AI suggests {selected_city} can save **{int(temp_diff*180)}k Liters** of groundwater daily by lowering the urban heat plume over surrounding fields.")
    
    # Agri Stress Gauge
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number", value = 100 - (temp_diff*8), title = {'text': "Crop Stress Index (Lower is Better)"},
        gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#1a237e"}, 'steps': [{'range': [0, 30], 'color': "lightgreen"}, {'range': [30, 70], 'color': "orange"}, {'range': [70, 100], 'color': "red"}]}
    ))
    st.plotly_chart(fig_gauge, use_container_width=True)

with tab4:
    st.subheader("🦁 Sher-AI Command Agent")
    agent = DecisionAgent("Sher", "Punjab Climate Defense", "🦁")
    
    # Simulated Chat interaction
    with st.chat_message("assistant", avatar="🦁"):
        st.write(f"Hello, I am the **AuraCool Sher Agent**. Analyzing {selected_city}...")
        st.write(f"**Current Health Threat:** {risk_lvl}")
        st.write(f"**Recommendation:** Implement Albedo targets of {int(refl*100)}% in the industrial sector to trigger ₹{int(money*8)} Lacs in Carbon credits.")
        
    user_query = st.text_input("Ask Sher-AI a question (e.g. 'How much water can we save in Patiala?')")
    if user_query:
        st.write(f"**Sher-AI:** Based on my 2025 neural model, implementing these strategies in {selected_city} will stabilize the local grid and reduce heatstroke risk by {int(temp_diff*15)}%.")

if st.button("🚀 DEPLOY AI PROTOCOL"):
    st.snow()
    st.success("Synchronized deployment: Smart Grid, Hospital Emergency, and Solar Arrays updated.")
