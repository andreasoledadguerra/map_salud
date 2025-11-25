# streamlit_app.py
import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import pandas as pd
import numpy as np

BASE_URL_MAP_SALUD = "http://localhost:8003"
url_map_salud = f"{BASE_URL_MAP_SALUD}/api/salud"

st.set_page_config(page_title="Map Salud (cliente)", layout="wide", page_icon="🏥")
st.title("Map Salud")

# Cargar CSV local para mostrar markers 
@st.cache_data
def load_df(path="establecimientos-salud-publicos.csv"):
    df = pd.read_csv(path, sep=None, engine="python", on_bad_lines="warn")
    df = df[["lat","long","fna"]].copy()
    df["lat"] = df["lat"].astype(float)
    df["long"] = df["long"].astype(float)
    df["fna"] = df["fna"].astype(str)
    return df

df = load_df()

# Sidebar controls
radius_km = st.sidebar.number_input("Radio (km)", min_value=0.1, max_value=50.0, value=1.0, step=0.1)
top_n = st.sidebar.number_input("Max resultados", min_value=1, max_value=200, value=10, step=1)
show_all = st.sidebar.checkbox("Mostrar todos los marcadores", value=False)

# Build initial map
center_lat = float(df["lat"].mean())
center_lon = float(df["long"].mean())
m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

if show_all:
    for _, r in df.iterrows():
        folium.CircleMarker(location=[r["lat"], r["long"]], radius=3, tooltip=r["fna"], color="#333").add_to(m)

st.markdown("Haz click en el mapa para seleccionar un punto y consultar la API.")

map_data = st_folium(m, width=900, height=600)

if map_data and map_data.get("last_clicked"):
    click = map_data["last_clicked"]
    lat = click["lat"]
    lng = click["lng"]  # Folium devuelve "lng", lo mantenemos como variable
    st.sidebar.success(f"Clicked: {lat:.6f}, {lng:.6f}")

    # Llamar al endpoint POST 
    payload = {
        "lat": float(lat),
        "long": float(lng),  
        "radius_km": float(radius_km), 
        "top_n": int(top_n)
    }
    
    # Debug: mostrar payload
    st.sidebar.write("📤 Enviando payload:", payload)
    
    try:
        resp = requests.post(url_map_salud, json=payload, timeout=5.0)
        resp.raise_for_status()
        data = resp.json()
        st.sidebar.success("✅ API respondió correctamente")
    except Exception as e:
        st.error(f"Error llamando al API: {e}")
        # Mostrar detalles del error si es 422
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_detail = e.response.json()
                st.error("Detalles del error:")
                st.write(error_detail)
            except:
                st.error(f"Respuesta cruda: {e.response.text}")
        data = None

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