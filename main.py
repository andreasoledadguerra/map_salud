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

