import pandas as pd
import numpy as np
import os

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict, List


#Create FastAPI app
app = FastAPI()

#Base url for streamlit app
BASE_URL_MAP_SALUD = "http://localhost:8501"

#Streamlit API endpoint to get data
#url_map_salud = f"{BASE_URL_MAP_SALUD}/salud"


# Pydantic request / response  models
class SaludRequestModel(BaseModel):
    lat: float
    lon: float
    radius_km: float = 1.0
    top_n: int = 20

class SaludResultModel(BaseModel):
    lat: float
    lon: float
    fna: str
    distance_km: float
    
class SaludResponseModel(BaseModel):
    request: SaludRequestModel
    results: List[SaludResultModel]
    
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
    
# Decorator to define FastAPI endpoint
#@app.get("/establecimientos", response_model=SaludResponseModel)
#def get_establecimientos(lat: float, lon: float, radius_km: float = 1.0, top_n: int = 20) -> SaludResponseModel:
#    params = {
#        "lat": lat,
#        "lon": lon,
#        "radius_km": radius_km,
#        "top_n": top_n
#    }
#    response = requests.get(url_map_salud, params=params)
#    response.raise_for_status()
#    data = response.json()
#    return SaludResponseModel(**data)