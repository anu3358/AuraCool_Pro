import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go
from engine import AuraEngine, DecisionAgent, get_city_data 

# --- UI CONFIGURATION ---
st.set_page_config(page_title="AuraCool OS | Cyber-Pink Edition", layout="wide")

# High-Contrast Pink & Midnight Theme
st.markdown("""
    <style>
    .stApp { background-color: #0d000a; color: #ff00ff; }
    [data-testid="stMetricValue"] { color: #ff00ff !important; font-size: 40px; font-weight: 900; text-shadow: 2px 2px #000000; }
    [data-testid="stMetricLabel"] { color: #ffffff !important; font-size: 16px; }
    .stSidebar { background-color: #1a0014; border-right: 2px solid #ff00ff; }
    .main-stats { background-color: #2b0021; padding: 25px; border-radius: 15px; border: 2px solid #ff00ff; margin-bottom: 25px; }
    h1, h2, h3 { color: #ff00ff; font-family: 'Trebuchet MS'; text-transform: uppercase; letter-spacing: 2px; }
    .stTabs [data-baseweb="tab-list"] { background-color: #1a0014; }
    .stTabs [data-baseweb="tab"] { color: #ffffff; }
    .stTabs [aria-selected="true"] { color: #ff00ff !important; border-bottom: 3px solid #ff00ff; }
    </style>
    """, unsafe_allow_html=True)

if 'engine' not in st.session_state:
    st.session_state.engine = AuraEngine()

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.title("💖 AURA-PINK OS")
    st.write("---")
    cities = get_city_data()
    selected_city = st.selectbox("📍 SELECT DISTRICT", list(cities.keys()))
    
    st.subheader("⚙️ INTERVENTIONS")
    green = st.slider("Canopy Expansion", 0.0, 1.0, 0.3)
    refl = st.slider("Reflective Surfaces", 0.0, 1.0, 0.2)
    
    st.subheader("🛰️ SCAN SETTINGS")
    map_mode = st.radio("LAYER VIEW", ["Baseline Heat", "AI Optimized"])

# --- AI DATA PROCESSING ---
city_info = cities[selected_city]
optimized_temp = st.session_state.engine.run_simulation(green, refl, 0.7, city_info['hum']/100)
display_temp = optimized_temp if map_mode == "AI Optimized" else city_info['base']
temp_diff = city_info['base'] - optimized_temp
msg, risk_lvl = st.session_state.engine.predict_health_risk(display_temp, city_info['hum'])
co2, money = st.session_state.engine.calculate_carbon_credits(temp_diff)

# --- MAIN INTERFACE ---
st.title(f"📡 THERMAL SCAN: {selected_city}")

# Metric Cards (Neon Pink Style)
st.markdown('<div class="main-stats">', unsafe_allow_html=True)
m1, m2, m3, m4 = st.columns(4)
m1.metric("TEMP", f"{round(display_temp, 1)}°C", f"-{round(temp_diff, 1)}°C" if map_mode == "AI Optimized" else None)
m2.metric("RISK LEVEL", risk_lvl)
m3.metric("POWER SAVED", f"{int(temp_diff*3.5)}%")
m4.metric("REVENUE", f"${int(money)}")
st.markdown('</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["💗 MAP VIEW", "📊 POWER ANALYSIS", "🤖 AI COMMAND"])

with tab1:
    st.subheader("Cyber-Heat Visualization")
    points = 500
    weight_val = 0.3 if map_mode == "AI Optimized" else 1.3
    
    map_df = pd.DataFrame({
        "lat": [city_info['lat'] + np.random.normal(0, 0.007) for _ in range(points)],
        "lon": [city_info['lon'] + np.random.normal(0, 0.007) for _ in range(points)],
        "intensity": [np.random.uniform(0.1, 1.0) * weight_val for _ in range(points)]
    })

    view_state = pdk.ViewState(latitude=city_info['lat'], longitude=city_info['lon'], zoom=12.5, pitch=0)
    
    # Pink-Theme Heatmap Layer
    layer = pdk.Layer(
        "HeatmapLayer",
        data=map_df,
        get_position="[lon, lat]",
        get_weight="intensity",
        radius_pixels=40,
        color_range=[
            [43, 0, 43, 0],    # Transparent
            [128, 0, 128, 100], # Purple
            [255, 0, 255, 150], # Neon Pink
            [255, 100, 255, 200], # Light Pink
            [255, 255, 255, 255]  # White (Hottest)
        ]
    )

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v10',
        initial_view_state=view_state,
        layers=[layer]
    ))
    st.caption("White/Pink hotspots indicate zones requiring immediate thermal intervention.")

with tab2:
    st.subheader("Grid Load Forecasting")
    # Power Grid Logic
    hours = list(range(0, 24))
    baseline = [30 + 15*np.sin((h-6)*np.pi/12) + (city_info['base']/2) for h in hours]
    optimized = [b - (temp_diff * 2) for b in baseline]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hours, y=baseline, name="Baseline Load", line=dict(color='white', dash='dot')))
    fig.add_trace(go.Scatter(x=hours, y=optimized, name="Optimized Load", line=dict(color='#ff00ff', width=4)))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
        font_color="white", xaxis_title="Hour", yaxis_title="Load (MW)"
    )
    st.plotly_chart(fig, use_container_width=True)
    

with tab3:
    col_l, col_r = st.columns([1, 2])
    with col_l:
        st.image("https://cdn-icons-png.flaticon.com/512/3222/3222792.png", width=180)
    with col_r:
        st.chat_message("assistant", avatar="🦁").write(f"**SHER-AGENT (PUNJAB MISSION CONTROL):**")
        st.write(msg)
        st.info(f"Deployed strategy in {selected_city} will save the municipality approximately ${int(money)} annually.")

if st.button("🚀 EXECUTE PINK-PROTOCOL DEPLOYMENT"):
    st.balloons()
    st.success("Protocol Active. Smart Grid Updated.")
