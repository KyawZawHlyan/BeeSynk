import streamlit as st
import pandas as pd
import pydeck as pdk
import random
import time
import numpy as np

# Constants
NUM_DRONES = 10
MAP_CENTER = [14.3561, 101.3840]  # Khao Yai National Park
SIMULATION_TIME = 15
TIME_STEP = 1

# Initialize Streamlit
st.set_page_config(layout="wide")
st.markdown(
    "<h1 style='text-align: center; color: #0437F2;'>"
    "BeeSynk Drone Swarm Simulation (Prototype)"
    "</h1>",
    unsafe_allow_html=True
)
st.subheader("Simulating real-time environmental monitoring using autonomous drone swarms.")
# Function to initialize drone positions
def init_drones():
    return pd.DataFrame({
        "lat": [MAP_CENTER[0] + random.uniform(-0.005, 0.005) for _ in range(NUM_DRONES)],
        "lon": [MAP_CENTER[1] + random.uniform(-0.005, 0.005) for _ in range(NUM_DRONES)],
        "name": [f"Drone {i+1}" for i in range(NUM_DRONES)],
        "dx": [random.uniform(-0.0005, 0.0005) for _ in range(NUM_DRONES)],  # X velocity
        "dy": [random.uniform(-0.0005, 0.0005) for _ in range(NUM_DRONES)],  # Y velocity
    })

# Function to randomly move drones
import numpy as np

def update_drones(df):
    df["lat"] += df["dy"] + np.random.uniform(-0.0001, 0.0001, size=NUM_DRONES)
    df["lon"] += df["dx"] + np.random.uniform(-0.0001, 0.0001, size=NUM_DRONES)
    return df

# Create an empty placeholder for the map
map_placeholder = st.empty()

# Initialize drones
df = init_drones()

# Simulation loop (live animation for 10 seconds)
for t in range(SIMULATION_TIME):
    df = update_drones(df)
    
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position='[lon, lat]',
        get_color='[255, 0, 0, 160]',  # Red dots
        get_radius=30,
    )

    view_state = pdk.ViewState(
        latitude=MAP_CENTER[0],
        longitude=MAP_CENTER[1],
        zoom=13,
        pitch=45,
    )

    map = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/satellite-streets-v11",
        tooltip={"text": "{name}"}
    )

    map_placeholder.pydeck_chart(map)
    time.sleep(TIME_STEP)

# Final summary (dummy values)
st.subheader("Simulation Successfully Terminated")
area = round(random.uniform(12.5, 30.0), 2)
battery = round(random.uniform(1.0, 5.0), 1)

st.markdown(f"""
- **Total Area Covered:** {area} km²  
- **Battery Used:** {battery}%  
- **Time Taken:** {SIMULATION_TIME} seconds
""")
