import streamlit as st
import geopandas as gpd
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
frome folium.plugins import MarkerCluster

st.set_page_config(layout="wide")
st.title("Map Salud - localizar establecimientos de salud públicos cercanos")


# Load and prepare geospatial data
@st.cache_data
def load_data(path="establecimientos-salud-publicos.csv"):
    df = pd.read_csv(path, delimiter=";")
    
    df = df[["lat", "long", "fna"]].copy()
    df["lat"] = df["lat"].astype(float)
    df["long"] = df["long"].astype(float)
    df["fna"] = df["fna"].astype(str)
    return df  

df = load_data()

# Haversine distance function
def haversine_vectorized(lat1, lon1, lat2_arr, lon2_arr):
    
    R = 6371  # Radius of the Earth in kilometers
    lat1_r = np.radians(lat1)
    lon1_r = np.radians(lon1)
    lat2_r = np.radians(lat2_arr)
    lon2_r = np.radians(lon2_arr)

    dlat = lat2_r - lat1_r
    dlon = lon2_r - lon1_r

    a = np.sin(dlat / 2)**2 + np.cos(lat1_r) * np.cos(lat2_r) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c


# Sidebar for user input
st.sidebar.header("Buscar establecimientos públicos de salud")
radius_km = st.sidebar.number_input("Radio (km) para buscar", min_value=0.1, max_value=100.0, value=1.0, step=0.1)
top_n = st.sidebar.number_input("Máx. resultados a mostrar", min_value=1, max_value=200, value=20, step=1)
show_all_markers = st.sidebar.checkbox("Mostrar todos los establecimientos (espere)", value=False)


# Create folium map centered on data mean
center_lat = df["lat"].mean()
center_lon = df["lon"].mean()
m = folium.Map(location=[center_lat, center_lon], zoom_start=12)


# Handle map click to find nearby establishments
if show_all_markers:
    mc = MarkerCluster().add_to(m)
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=(row["lat"], row["long"]),
            radius=4,
            tooltip=row["fna"],
            color="#666666",
            fill=True,
            fill_opacity=0.7
        ).add_to(mc)

st.markdown("**Instrucciones:** hace _click_ en el mapa para seleccionar un punto; el app mostrará establecimientos dentro del radio seleccionado.")
map_data = st_folium(m, width=900, height=600)  

