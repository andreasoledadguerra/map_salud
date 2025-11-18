import folium
import geopandas as gpd
import numpy as np
import pandas as pd
import requests
import uvicorn 

import streamlit as st

from fastapi import FastAPI
from folium.plugins import MarkerCluster
from pydantic import BaseModel
from typing import Any, Dict, List
from streamlit_folium import st_folium


#Create FastAPI app
app = FastAPI()

#Base url for streamlit app
BASE_URL_MAP_SALUD = "http://localhost:8501"

#Streamlit API endpoint to get data
url_map_salud = f"{BASE_URL_MAP_SALUD}/salud"

# Pydantic response model for FastAPI endpoint
#class SaludResponseModel(BaseModel):
#    lat: float
#    lon: float
#    radius_km: float
#    top_n: int
#    results: List[Dict[str, Any]]
#
# Configure page
st.set_page_config(page_title="Map Salud", layout="wide", page_icon="🏥")

st.title("Map Salud - localizar establecimientos de salud públicos cercanos")
st.markdown("**Instrucciones:** hace _click_ en el mapa para seleccionar un punto geográfico.")


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
    R = 6371
    lat1_r = np.radians(lat1)
    lon1_r = np.radians(lon1)
    lat2_r = np.radians(lat2_arr)
    lon2_r = np.radians(lon2_arr)

    dlat = lat2_r - lat1_r
    dlon = lon2_r - lon1_r

    a = np.sin(dlat / 2)**2 + np.cos(lat1_r) * np.cos(lat2_r) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c


# Sidebar
st.sidebar.header("Buscar establecimientos públicos de salud")
radius_km = st.sidebar.number_input("Radio (km)", min_value=0.1, max_value=100.0, value=1.0, step=0.1)
top_n = st.sidebar.number_input("Máx. resultados", min_value=1, max_value=200, value=20, step=1)
show_all_markers = st.sidebar.checkbox("Mostrar todos los establecimientos", value=False)


# Create main map
center_lat = df["lat"].mean()
center_lon = df["long"].mean()

m = folium.Map(location=[center_lat, center_lon], zoom_start=12)


# Show all markers
if show_all_markers:
    mc = MarkerCluster().add_to(m)
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["long"]],
            radius=4,
            tooltip=row["fna"],
            color="#666666",
            fill=True,
            fill_opacity=0.7
        ).add_to(mc)


map_data = st_folium(m, width=900, height=600)


# Process click
if map_data and map_data.get("last_clicked"):
    clicked = map_data["last_clicked"]
    click_lat = clicked["lat"]
    click_lon = clicked["lng"]

    st.sidebar.success(f"Punto en lat: {click_lat:.6f}, lon: {click_lon:.6f}")

    # Calculate distances
    distances_km = haversine_vectorized(click_lat, click_lon, df["lat"].values, df["long"].values)
    df_results = df.copy()
    df_results["distance_km"] = distances_km

    # Filter
    nearby = df_results[df_results["distance_km"] <= radius_km]\
        .sort_values(by="distance_km")\
        .head(int(top_n))

    st.sidebar.write(f"Encontrados {len(nearby)} establecimientos dentro de {radius_km} km.")
    st.subheader("Establecimientos cercanos")
    st.dataframe(nearby.reset_index(drop=True))

    # New map for results
    m2 = folium.Map(location=[click_lat, click_lon], zoom_start=14)

    folium.Marker(
        location=[click_lat, click_lon],
        tooltip="Punto seleccionado",
        icon=folium.Icon(color="red", icon="info-sign")
    ).add_to(m2)

    # Mark nearby results
    for _, row in nearby.iterrows():
        folium.CircleMarker(
            location=[row["lat"], row["long"]],
            radius=6,
            color="blue",
            fill=True,
            fill_opacity=0.9,
            tooltip=f"{row['fna']} ({row['distance_km']:.2f} km)"
        ).add_to(m2)

    # Circle radius
    folium.Circle(
        location=[click_lat, click_lon],
        radius=radius_km * 1000,
        color="green",
        fill=False
    ).add_to(m2)

    st_folium(m2, width=900, height=600)

else:
    st.info("Haga click en el mapa para buscar establecimientos de salud públicos cercanos al lugar de su interés.")
