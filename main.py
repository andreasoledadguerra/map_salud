import geopandas as gpd
import streamlit as st
import pydeck as pdk

st.title("Map Salud")

# Load geospatial data
gdf = gpd.read_file("establecimientos-salud-publicos.csv")
