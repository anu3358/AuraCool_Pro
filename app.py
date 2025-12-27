import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
from engine import AuraEngine, DecisionAgent, get_city_data

# --- MIDNIGHT TECH THEME ---
st.set_page_config(page_title="AuraCool Punjab | 2025", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #05070a; color: #00ffcc; }
    [data-testid="stMetricValue"] { color: #00ffcc !important; font-size: 32px; font-weight: bold; }
    .stTabs [data-baseweb="tab-list"] { background-color: #05070a; border-bottom: 1px solid #333; }
    .stTabs [data-baseweb="tab"] { color: #888; }
    .stTabs [aria-selected="true"] { color: #00ffcc !important; border-bottom: 2px solid #00ffcc; }
    div[data-testid="stExpander"] { background-color: #10141d; border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

if 'engine' not in st.session_state:
    st.session_state.engine = AuraEngine()

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3222/3222792.png", width=100)
    st.title("AuraCool: Punjab Grid")
    cities = get_city_data()
    selected_city = st.selectbox("Select Urban Sector", list(cities.keys()))
    st.divider()
    green = st.slider("Urban Forestry Coverage", 0.0, 1.0, 0.25)
    reflect = st.slider("Solar-Reflective Surfaces", 0.0, 1.0, 0.20)
    density = st.slider("Infrastructure Density", 0.0, 1.0, 0.75)

# --- AI CALCULATION ---
city_info = cities[selected_city]
sim_temp = st.session_state.engine.run_simulation(green, reflect, density, city_info['hum']/100)
temp_diff = city_info['base'] - sim_temp
health_msg, health_lvl = st.session_state.engine.predict_health_risk(sim_temp, city_info['hum'])
co2, money = st.session_state.engine.calculate_carbon_credits(temp_diff)

# --- MAIN DASHBOARD ---
st.header(f"🛰️ Command Dashboard: {selected_city}")

t1, t2, t3, t4 = st.tabs(["🌡️ Thermal Twin", "🏥 Health AI", "💨 Airflow Physics", "💎 Carbon Ledger"])

with t1:
    c1, c2, c3 = st.columns(3)
    c1.metric("Predicted Temp", f"{sim_temp}°C", f"-{round(temp_diff, 2)}°C")
    c2.metric("Local Humidity", f"{city_info['hum']}%")
    c3.metric("Cooling Efficiency", f"{int((temp_diff/10)*100)}%", "AI Optimized")

    map_data = pd.DataFrame({
        "lat": [city_info['lat'] + np.random.uniform(-0.01, 0.01) for _ in range(80)],
        "lon": [city_info['lon'] + np.random.uniform(-0.01, 0.01) for _ in range(80)],
        "heat": [np.random.randint(38, 52) for _ in range(80)]
    })
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/dark-v10',
        initial_view_state=pdk.ViewState(latitude=city_info['lat'], longitude=city_info['lon'], zoom=13, pitch=50),
        layers=[pdk.Layer('HexagonLayer', data=map_data, get_position='[lon, lat]', radius=200, elevation_scale=80, extruded=True)]
    ))

with t2:
    st.subheader("Regional Health Risk Assessment")
    if "CRITICAL" in health_msg: st.error(health_msg)
    else: st.warning(health_msg)
    
    
    
    st.markdown("""
    ### 🛡️ Mitigation Strategy
    1. **Water Stations:** Deploy mobile hydration units in high-density areas.
    2. **Energy Grid:** Expect 15% increase in cooling load between 12:00 PM - 4:00 PM.
    3. **Agriculture:** Advise farmers on early morning irrigation to reduce evapotranspiration stress.
    """)

with t3:
    st.subheader("Urban Airflow Vector Field")
    x, y, u, v = st.session_state.engine.simulate_airflow_vectors(city_info['lat'], city_info['lon'])
    fig = ff.create_quiver(x, y, u, v, scale=.005, arrow_scale=.3, line_color='#00fbff')
    st.plotly_chart(fig, use_container_width=True)

with t4:
    st.subheader("ESG & Carbon Credit Monetization")
    st.write(f"**Total Carbon Credits Generated:** {co2:,} Metric Tons")
    st.write(f"**Potential Market Revenue:** ${money:,}")
    st.progress(min(temp_diff/8, 1.0))
    
    with st.expander("🤖 View Agent Deliberation"):
        st.chat_message("assistant", avatar="🦁").write(f"**Sher Agent (Punjab Command):** Cooling {selected_city} is critical for both public health and preventing livestock heat stress.")
        st.chat_message("assistant", avatar="💰").write(f"**Quartz Agent (FinTech):** We can tokenize these carbon credits on the smart grid to fund more green roofs.")

if st.button("🚀 Push to Smart City Grid"):
    st.snow()
