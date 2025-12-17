# streamlit_app.py
import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import pandas as pd
import numpy as np

from app.data.constants import (
    PATH,
    RADIUS_EARTH,
    COL_LAT,
    COL_LONG,
    EST_SALUD,
    KM_DISTANCE,
)

from app.data.processs_load_data import load_data

BASE_URL_MAP_SALUD = "http://localhost:8003"
url_map_salud = f"{BASE_URL_MAP_SALUD}/api/salud"

st.set_page_config(page_title="Map Salud (cliente)", layout="wide", page_icon="🏥")
st.title("Map Salud")

# Cargar CSV local para mostrar markers 
@st.cache_data


df = load_data(PATH)

# Sidebar controls
radius_km = st.sidebar.number_input("Radio (km)", min_value=0.1, max_value=50.0, value=1.0, step=0.1)
top_n = st.sidebar.number_input("Max resultados", min_value=1, max_value=200, value=10, step=1)
show_all = st.sidebar.checkbox("Mostrar todos los marcadores", value=False)

# Build initial map
center_lat = float(df[COL_LAT].mean())
center_lon = float(df[COL_LONG].mean())
m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

if show_all:
    for _, r in df.iterrows():
        folium.CircleMarker(location=[r["lat"], r["long"]], radius=3, tooltip=r["fna"], color="#333").add_to(m)

st.markdown("Haz click en el mapa para seleccionar un punto y consultar la API.")

map_data = st_folium(m, width=900, height=600)

if map_data and map_data.get("last_clicked"):
    click = map_data["last_clicked"]
    lat = click["lat"]
    lng = click["lng"]
    st.sidebar.success(f"Clicked: {lat:.6f}, {lng:.6f}")

    # Llamar al endpoint POST 
    payload = {
        "lat": float(lat),
        "long": float(lng),  
        "radius_km": float(radius_km), 
        "top_n": int(top_n)
    }

    resp = requests.post(url_map_salud, json=payload, timeout=5.0)
    data = resp.json()
    if data:
        # Mostrar resultados
        results = data.get("results", [])
        st.subheader("Resultados desde API")
        if not results:
            st.info("No se encontraron establecimientos dentro del radio especificado.")
        else:
            df_res = pd.DataFrame(results)
            st.dataframe(df_res)

            # Mostrar mapa centrado en el primer resultado
            
            m2 = folium.Map(location=[results[0]["lat"], results[0]["long"]], zoom_start=14)
            folium.Marker(
                location=[lat, lng],
                tooltip="Tu clic", 
                icon=folium.Icon(color="red")
            ).add_to(m2)
            for r in results:
                folium.CircleMarker(
                    location=[r["lat"], r["long"]],
                    radius=6, 
                    tooltip=f"{r['fna']} ({r['distance_km']:.3f} km)"
                ).add_to(m2)
            st_folium(m2, width=900, height=500)