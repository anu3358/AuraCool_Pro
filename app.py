import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np  # Explicitly defined
import plotly.figure_factory as ff
from engine import AuraEngine, DecisionAgent, get_city_data

# Force-check numpy availability
if 'np' not in globals():
    import numpy as np

st.set_page_config(page_title="AuraCool Ultra | 2025", layout="wide")

# Initialization
if 'engine' not in st.session_state:
    st.session_state.engine = AuraEngine()

# --- SIDEBAR ---
with st.sidebar:
    st.title("🛡️ AuraCool OS")
    cities = get_city_data()
    selected_city = st.selectbox("Select Target Grid", list(cities.keys()))
    st.divider()
    green = st.sidebar.slider("Canopy Coverage (%)", 0, 100, 30) / 100
    reflect = st.sidebar.slider("Surface Albedo (%)", 0, 100, 20) / 100
    density = st.sidebar.slider("Structural Density (%)", 0, 100, 70) / 100

# --- LOGIC ---
city_info = cities[selected_city]
sim_temp = st.session_state.engine.run_simulation(green, reflect, density)
temp_diff = city_info['base'] - sim_temp
co2, money = st.session_state.engine.calculate_carbon_credits(temp_diff)

# --- UI TABS ---
t1, t2, t3, t4 = st.tabs(["🌡️ Thermal Twin", "💨 Airflow Physics", "💎 Carbon FinTech", "🤖 Agentic Loop"])

with t1:
    st.metric("District Temperature", f"{sim_temp}°C", f"-{round(temp_diff, 2)}°C")
    
    # Using np directly here
    map_lat = [city_info['lat'] + np.random.uniform(-0.01, 0.01) for _ in range(50)]
    map_lon = [city_info['lon'] + np.random.uniform(-0.01, 0.01) for _ in range(50)]
    
    map_data = pd.DataFrame({
        "lat": map_lat,
        "lon": map_lon,
        "heat": [np.random.randint(30, 50) for _ in range(50)]
    })
    
    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(latitude=city_info['lat'], longitude=city_info['lon'], zoom=13, pitch=45),
        layers=[pdk.Layer('HexagonLayer', data=map_data, get_position='[lon, lat]', radius=150, elevation_scale=50, extruded=True)]
    ))

with t2:
    st.subheader("Dynamic Fluid Airflow Analysis")
    x, y, u, v = st.session_state.engine.simulate_airflow_vectors(city_info['lat'], city_info['lon'])
    fig = ff.create_quiver(x, y, u, v, scale=.005, arrow_scale=.3, line_color='#00fbff')
    st.plotly_chart(fig, use_container_width=True)

with t3:
    st.subheader("Automated Carbon Credit Ledger")
    c1, c2 = st.columns(2)
    c1.metric("CO2 Offset (Tons)", f"{co2:,}")
    c2.metric("Market Credit Value", f"${money:,}")

with t4:
    agents = [
        DecisionAgent("Nexus", "Physics", "🔭"),
        DecisionAgent("Quartz", "FinTech", "💎"),
        DecisionAgent("Gaia", "Environment", "🌿")
    ]
    for a in agents:
        with st.chat_message("assistant", avatar=a.icon):
            st.write(f"**{a.name} ({a.role} Agent)**")
            st.write(a.analyze(temp_diff, money))

if st.button("🚀 Finalize Project"):
    st.snow()
