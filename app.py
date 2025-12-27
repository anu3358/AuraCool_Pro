import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
from engine import AuraEngine, DecisionAgent, get_city_data 

# --- MASTER UI CONFIG ---
st.set_page_config(page_title="AuraCool OS | Punjab 2025", layout="wide")

# High-End Command Center Styling
st.markdown("""
    <style>
    .stApp { background-color: #020408; color: #00ffcc; }
    [data-testid="stMetricValue"] { color: #00ffcc !important; font-family: 'Orbitron', sans-serif; }
    .stSidebar { background-color: #0a0c10; border-right: 1px solid #00ffcc33; }
    .css-1kyx60w { background-color: #10141d; } /* Sidebar background */
    </style>
    """, unsafe_allow_html=True)

if 'engine' not in st.session_state:
    st.session_state.engine = AuraEngine()

# --- SIDEBAR: MISSION CONTROL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2099/2099192.png", width=70)
    st.title("AuraCool OS")
    st.caption("2025 Urban Heat Mitigation System")
    st.divider()
    
    cities = get_city_data()
    selected_city = st.selectbox("📍 Select District", list(cities.keys()))
    
    st.subheader("🛠️ Strategic Deployment")
    green = st.slider("Urban Canopy expansion", 0.0, 1.0, 0.35)
    refl = st.slider("Cool Surface (Albedo) Implementation", 0.0, 1.0, 0.25)
    
    st.subheader("🔍 Scan Mode")
    scan_mode = st.radio("Display Layer", ["Thermal Intensity", "Health Vulnerability Index"])
    
    view_mode = st.toggle("Activate AI Optimization", value=False)

# --- ENGINE PROCESSING ---
city_info = cities[selected_city]
# Calculate result based on toggle
if view_mode:
    current_temp = st.session_state.engine.run_simulation(green, refl, 0.6, city_info['hum']/100)
else:
    current_temp = city_info['base']

temp_diff = city_info['base'] - current_temp
msg, lvl = st.session_state.engine.predict_health_risk(current_temp, city_info['hum'])
co2, money = st.session_state.engine.calculate_carbon_credits(temp_diff)

# --- MAIN DASHBOARD ---
st.title(f"District Analysis: {selected_city}")

# Metric Dashboard
m1, m2, m3, m4 = st.columns(4)
m1.metric("Surface Temp", f"{round(current_temp, 1)}°C", f"-{round(temp_diff, 1)}°C" if view_mode else None)
m2.metric("Health Risk Status", lvl)
m3.metric("ESG Credit Yield", f"${int(money)}")
m4.metric("Grid Stability", "94%" if view_mode else "71%")

tab1, tab2, tab3 = st.tabs(["🌐 Spatial Intelligence", "📈 Impact Metrics", "🤖 Agent Briefing"])

with tab1:
    # Determine Map Colors
    # Thermal uses Red/Yellow. Vulnerability uses Purple/Pink.
    if scan_mode == "Thermal Intensity":
        c_range = [[255, 255, 178], [254, 204, 92], [253, 141, 60], [240, 59, 32], [189, 0, 38]]
        map_title = "Surface Temperature Heatmap"
    else:
        c_range = [[237, 248, 251], [179, 205, 227], [140, 150, 198], [136, 86, 167], [129, 15, 124]]
        map_title = "Population Vulnerability Index (High Density Zones)"

    # Intensity Logic
    weight_factor = 0.5 if view_mode and scan_mode == "Thermal Intensity" else 1.0
    
    map_points = pd.DataFrame({
        "lat": [city_info['lat'] + np.random.normal(0, 0.007) for _ in range(500)],
        "lon": [city_info['lon'] + np.random.normal(0, 0.007) for _ in range(500)],
        "weight": [np.random.uniform(0.1, 1.0) * weight_factor for _ in range(500)]
    })

    st.subheader(map_title)
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v10',
        initial_view_state=pdk.ViewState(latitude=city_info['lat'], longitude=city_info['lon'], zoom=12.5, pitch=40),
        layers=[pdk.Layer(
            "HeatmapLayer",
            data=map_points,
            get_position="[lon, lat]",
            get_weight="weight",
            radius_pixels=50,
            color_range=c_range,
            intensity=1,
            threshold=0.03
        )]
    ))
    
    

with tab2:
    st.subheader("Fluid Dynamics & Economic Yield")
    col_left, col_right = st.columns(2)
    
    with col_left:
        # Airflow Physics
        x, y, u, v = st.session_state.engine.simulate_airflow_vectors(city_info['lat'], city_info['lon'])
        fig = ff.create_quiver(x, y, u, v, scale=.005, line_color='#00ffcc')
        fig.update_layout(title="Atmospheric Dissipation Vectors", paper_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig, use_container_width=True)
        
    with col_right:
        st.write("### Carbon Credit Growth")
        st.write("By reducing the urban temperature, the city generates tradable carbon credits.")
        st.progress(min(temp_diff/10, 1.0))
        st.info(f"Cumulative Savings for {selected_city}: ${int(money)} USD/Year")

with tab3:
    st.subheader("Multi-Agent Deliberation")
    agent_sher = DecisionAgent("Sher", "Punjab Health Command", "🦁")
    
    with st.chat_message("assistant", avatar="🦁"):
        st.write(f"**{agent_sher.name} Reporting:**")
        st.write(msg)
        if view_mode:
            st.success("Optimization active. Cooling centers are now strategically mapped to high-vulnerability zones.")
        else:
            st.warning("Immediate action required. High-risk thermal clusters detected in residential blocks.")

# Final Footer Action
if st.button("🚀 Execute Smart City Cooling Protocol"):
    st.balloons()
    st.success("Deployment Signal Sent to Municipal Grids.")
