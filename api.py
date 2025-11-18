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