import streamlit as st
import pandas as pd
import pydeck as pdk
import random

st.set_page_config(layout="wide")

# Constants
NUM_DRONES = 10
MAP_CENTER = [1.3521, 103.8198]  # Example: Singapore

# Simulate random drone positions
def generate_drones():
    lat_center, lon_center = MAP_CENTER
    data = {
        "lat": [lat_center + random.uniform(-0.01, 0.01) for _ in range(NUM_DRONES)],
        "lon": [lon_center + random.uniform(-0.01, 0.01) for _ in range(NUM_DRONES)],
        "name": [f"Drone {i+1}" for i in range(NUM_DRONES)],
    }
    return pd.DataFrame(data)

df = generate_drones()

st.title("🛰️ BeeSynk Swarm Simulation Prototype")

st.pydeck_chart(pdk.Deck(
    map_style="mapbox://styles/mapbox/satellite-streets-v11",
    initial_view_state=pdk.ViewState(
        latitude=MAP_CENTER[0],
        longitude=MAP_CENTER[1],
        zoom=13,
        pitch=45,
    ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=df,
            get_position='[lon, lat]',
            get_color='[255, 204, 0, 160]',
            get_radius=30,
        ),
    ],
))