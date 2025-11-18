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




