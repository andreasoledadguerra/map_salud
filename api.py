#import pandas as pd
#import numpy as np
#import os
#import streamlit as st
#
#from fastapi import FastAPI
#from pydantic import BaseModel
#from sklearn.neighbors import BallTree
#from typing import List
#
#
#
##Create FastAPI app
#app = FastAPI()
#
##Base url for streamlit app
#BASE_URL_MAP_SALUD = "http://localhost:8004"
#
##Streamlit API endpoint to get data
#url_map_salud = f"{BASE_URL_MAP_SALUD}/api/salud"
#
#
#
## Pydantic request / response  models
#class SaludRequestModel(BaseModel):
#    lat: float
#    lon: float
#    radius_km: float = 1.0
#    top_n: int = 20
#
#class SaludResultModel(BaseModel):
#    lat: float
#    lon: float
#    fna: str
#    distance_km: float
#    
#class SaludResponseModel(BaseModel):
#    request: SaludRequestModel
#    results: List[SaludResultModel]
#    
## Haversine distance function
#def haversine_vectorized(lat1, lon1, lat2_arr, lon2_arr):
#    R = 6371
#    lat1_r = np.radians(lat1)
#    lon1_r = np.radians(lon1)
#    lat2_r = np.radians(lat2_arr)
#    lon2_r = np.radians(lon2_arr)
#
#    dlat = lat2_r - lat1_r
#    dlon = lon2_r - lon1_r
#
#    a = np.sin(dlat / 2)**2 + np.cos(lat1_r) * np.cos(lat2_r) * np.sin(dlon / 2)**2
#    c = 2 * np.arcsin(np.sqrt(a))
#    return R * c
# 
# # Load and prepare geospatial data
#def load_data(path="establecimientos-salud-publicos.csv"):
#    df = pd.read_csv(path, delimiter=";")
#    df = df[["lat", "long", "fna"]].copy()
#    df["lat"] = df["lat"].astype(float)
#    df["long"] = df["long"].astype(float)
#    df["fna"] = df["fna"].astype(str)
#    #df = df.rename(columns={"lon": "long"})
#    return df  
#
## Prepara BallTree sobre coordenadas en radianes (Haversine metric)
#df = load_data()
#coords_rad = np.vstack([np.radians(df["lat"].values), np.radians(df["long"].values)]).T
## BallTree espera (n_samples, n_features) as coords in radians with metric='haversine'
#tree = BallTree(coords_rad, metric="haversine")
# 
#
## Endpoint
#@app.post("/api/salud", response_model=SaludResponseModel)
#def post_establecimientos(req: SaludRequestModel) -> SaludResponseModel:
#    lat = req.lat
#    lon = req.lon
#    radius_km = float(req.radius_km)
#    top_n = int(req.top_n)
#
#    # Calcular distancias usando BallTree
#    point_rad = np.radians([[lat, lon]])
#    radius_rad = radius_km / 6371.0  # Convertir km a radianes
#    indices = tree.query_radius(point_rad, r=radius_rad)[0]
#
#    # Obtener distancias reales
#    distances_km = haversine_vectorized(lat, lon, df.iloc[indices]["lat"].values, df.iloc[indices]["lon"].values)
#
#    # Crear DataFrame de resultados
#    df_results = df.iloc[indices].copy()
#    df_results["distance_km"] = distances_km
#
#    # Ordenar y limitar resultados
#    df_results = df_results.sort_values(by="distance_km").head(top_n)
#
#    # Construir lista de resultados
#    results = [
#        SaludResultModel(
#            lat=row["lat"],
#            lon=row["lon"],
#            fna=row["fna"],
#            distance_km=row["distance_km"]
#        )
#        for _, row in df_results.iterrows()
#    ]
#
#    return SaludResponseModel(
#        request=req,
#        results=results
#    )

import pandas as pd
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.neighbors import BallTree
from typing import List

app = FastAPI()

# Modelos Pydantic
class SaludRequestModel(BaseModel):
    lat: float
    long: float 
    radius_km: float = 1.0
    top_n: int = 20

class SaludResultModel(BaseModel):
    lat: float
    long: float 
    fna: str
    distance_km: float
    
class SaludResponseModel(BaseModel):
    request: SaludRequestModel
    results: List[SaludResultModel]

# Haversine function
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

# Load data 
def load_data(path="establecimientos-salud-publicos.csv"):
    df = pd.read_csv(path, delimiter=";")
    df = df[["lat", "long", "fna"]].copy()
    df["lat"] = df["lat"].astype(float)
    df["long"] = df["long"].astype(float)
    df["fna"] = df["fna"].astype(str)
    
    return df

df = load_data()
coords_rad = np.vstack([np.radians(df["lat"].values), np.radians(df["long"].values)]).T
tree = BallTree(coords_rad, metric="haversine")

@app.post("/api/salud", response_model=SaludResponseModel)
def post_establecimientos(req: SaludRequestModel) -> SaludResponseModel:
    lat = req.lat
    long = req.long  # Ahora usamos long
    radius_km = req.radius_km
    top_n = req.top_n

    point_rad = np.radians([[lat, long]])
    radius_rad = radius_km / 6371.0
    indices = tree.query_radius(point_rad, r=radius_rad)[0]

    distances_km = haversine_vectorized(
        lat, long, 
        df.iloc[indices]["lat"].values, 
        df.iloc[indices]["long"].values
    )

    df_results = df.iloc[indices].copy()
    df_results["distance_km"] = distances_km
    df_results = df_results.sort_values(by="distance_km").head(top_n)

    results = [
        SaludResultModel(
            lat=row["lat"],
            long=row["long"], 
            fna=row["fna"],
            distance_km=row["distance_km"]
        )
        for _, row in df_results.iterrows()
    ]

    return SaludResponseModel(request=req, results=results)

#@app.get("/")
#def root():
#    return {"message": "Map Salud API", "status": "running", "endpoint": "/api/salud"}
#
#@app.get("/health")
#def health_check():
#    return {"status": "healthy", "data_points": len(df)}