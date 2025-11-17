import streamlit as st
import geopandas as gpd
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
frome folium.plugins import MarkerCluster


st.title("Map Salud")

# Load geospatial data
gdf = gpd.read_file("establecimientos-salud-publicos.csv")

gdf = gdf[["lat","long","fna"]]

# Copiamos y convertimos columnas
gdf = gdf.copy()

# Fuerza conversiones a tipos nativos
gdf["lat"] = gdf["lat"].astype(float)
gdf["long"] = gdf["long"].astype(float)
gdf["fna"] = gdf["fna"].astype(str)

# Convertir a lista de dicts para pydeck
data = gdf.to_dict(orient="records")


#Definir la capa de puntos
layer = pdk.Layer("ScatterplotLayer",
                  data=data,
                  get_position='[long, lat]',
                  get_radius=100,
                  )

#Definir la vista inicial del mapa
view_state = pdk.ViewState(latitude=gdf['lat'].mean(), longitude=gdf['long'].mean(), zoom=12, pitch=0)


st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{fna}"}))

