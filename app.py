import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go
from engine import AuraEngine, DecisionAgent, get_city_data 

# --- UI CONFIGURATION ---
st.set_page_config(page_title="AuraCool OS | Punjab 2025", layout="wide")

# HIGH-VISIBILITY THEME: Slate & Neon
st.markdown("""
    <style>
    /* Main Background - Dark Slate for better contrast than pure black */
    .stApp { 
        background-color: #1a1c23; 
        color: #ffffff; 
    }
    
    /* Metrics Styling - Neon Cyan with high readability */
    [data-testid="stMetricValue"] { 
        color: #00f2ff !important; 
        font-size: 38px !important; 
        font-weight: 800 !important; 
    }
    
    /* Sidebar - Slightly darker but with clear borders */
    .stSidebar { 
        background-color: #111217; 
        border-right: 2px solid #ff00ff; 
    }
    
    /* Metric Cards - Boxed with border for maximum visibility */
    .main-stats { 
        background-color: #252833; 
        padding: 25px; 
        border-radius: 12px; 
        border: 2px solid #3d4251; 
        margin-bottom: 25px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }
    
    /* Headers - Neon Pink */
    h1, h2, h3 { 
        color: #ff00ff; 
        font-family: 'Helvetica Neue', sans-serif; 
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] { background-color: transparent; }
    .stTabs [data-baseweb="tab"] { color: #ffffff; font-size: 18px; }
    .stTabs [aria-selected="true"] { color: #ff00ff !important; border-bottom: 3px solid #ff00ff; }
    </style>
    """, unsafe_allow_html=True)

if 'engine' not in st.session_state:
    st.session_state.engine = AuraEngine()

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.title("🏙️ AuraCool OS")
    st.markdown("---")
    cities = get_city_data()
    selected_city = st.selectbox("📍 Target District", list(cities.keys()))
    
    st.divider()
    st.subheader("Simulate Interventions")
    green = st.slider("Tree Canopy Expansion (%)", 0, 100, 25) / 100
    refl = st.slider("Reflective Infrastructure (%)", 0, 100, 15) / 100
    
    st.subheader("Map Visualization")
    map_mode = st.radio("View Mode", ["Current Heatmap", "AI Optimized View"])

# --- AI DATA PROCESSING ---
city_info = cities[selected_city]
optimized_temp = st.session_state.engine.run_simulation(green, refl, 0.7, city_info['hum']/100)
display_temp = optimized_temp if map_mode == "AI Optimized View" else city_info['base']
temp_diff = city_info['base'] - optimized_temp
msg, risk_lvl = st.session_state.engine.predict_health_risk(display_temp, city_info['hum'])
co2, money = st.session_state.engine.calculate_carbon_credits(temp_diff)

# --- MAIN INTERFACE ---
st.title(f"District Health & Thermal Scan: {selected_city}")

# Top Metric Cards (High Visibility Container)
st.markdown('<div class="main-stats">', unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Surface Temp", f"{round(display_temp, 1)}°C", f"-{round(temp_diff, 1)}°C" if map_mode == "AI Optimized View" else None)
c2.metric("Health Risk", risk_lvl)
c3.metric("Grid Load Reduction", f"{int(temp_diff*3.2)}%", "Power Saved")
c4.metric("Carbon Yield", f"${int(money)}")
st.markdown('</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🗺️ Geospatial Analysis", "⚡ Power Grid Impact", "🦁 Agent Deliberation"])

with tab1:
    st.subheader("Live Thermal Surface Scan")
    points = 400
    weight_val = 0.4 if map_mode == "AI Optimized View" else 1.2
    
    map_df = pd.DataFrame({
        "lat": [city_info['lat'] + np.random.normal(0, 0.006) for _ in range(points)],
        "lon": [city_info['lon'] + np.random.normal(0, 0.006) for _ in range(points)],
        "intensity": [np.random.uniform(0.1, 1.0) * weight_val for _ in range(points)]
    })

    view_state = pdk.ViewState(latitude=city_info['lat'], longitude=city_info['lon'], zoom=13, pitch=0)
    
    # Heatmap color range: Purple to Cyan to White (Highest Visibility)
    layer = pdk.Layer(
        "HeatmapLayer",
        data=map_df,
        get_position="[lon, lat]",
        get_weight="intensity",
        radius_pixels=50,
        color_range=[
            [43, 0, 43, 0],    # Transparent
            [128, 0, 128, 100], # Purple
            [0, 242, 255, 150], # Neon Cyan
            [255, 0, 255, 200], # Neon Pink
            [255, 255, 255, 255]  # White
        ]
    )

    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v10',
        initial_view_state=view_state,
        layers=[layer],
    ))

with tab2:
    st.subheader("Electricity Demand Forecasting")
    hours = list(range(0, 24))
    baseline_load = [30 + 20*np.sin((h-6)*np.pi/12) + 10*(city_info['base']/40) for h in hours]
    optimized_load = [b * (1 - (temp_diff*0.04)) for b in baseline_load]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hours, y=baseline_load, name="Current Grid Demand", line=dict(color='white', width=2, dash='dot')))
    fig.add_trace(go.Scatter(x=hours, y=optimized_load, name="AI Optimized Demand", line=dict(color='#00f2ff', width=4)))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white",
        xaxis_title="Hour of Day", yaxis_title="Load (Megawatts)"
    )
    st.plotly_chart(fig, use_container_width=True)
    

with tab3:
    st.subheader("AI Governance Strategy")
    col_l, col_r = st.columns([1, 2])
    with col_l:
        st.image("https://cdn-icons-png.flaticon.com/512/3222/3222792.png", width=180)
    with col_r:
        st.chat_message("assistant", avatar="🦁").write(f"**Command Center Reporting for {selected_city}:**")
        st.write(msg)
        st.info(f"ROI Analysis: Cooling {selected_city} by {round(temp_diff, 1)}°C provides a {round(money/10, 2)}x return on climate investment.")

if st.button("🚀 EXECUTE MUNICIPAL DEPLOYMENT"):
    st.snow()
    st.success("Strategy pushed to Municipal Smart Grid.")
