import pandas as pd
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.neighbors import BallTree
from typing import List

from data.constants import (
    PATH,
    RADIUS_EARTH,
    COL_LAT,
    COL_LONG,
    EST_SALUD,
    KM_DISTANCE,
)

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
    
    lat1_r = np.radians(lat1)
    lon1_r = np.radians(lon1)
    lat2_r = np.radians(lat2_arr)
    lon2_r = np.radians(lon2_arr)

    dlat = lat2_r - lat1_r
    dlon = lon2_r - lon1_r

    a = np.sin(dlat / 2)**2 + np.cos(lat1_r) * np.cos(lat2_r) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return RADIUS_EARTH * c

# Load data 
def load_data(PATH):
    df = pd.read_csv(PATH, delimiter=";")
    df = df[[COL_LAT , COL_LONG, EST_SALUD]].copy()
    df[COL_LAT] = df[COL_LAT].astype(float)
    df[COL_LONG] = df[COL_LONG].astype(float)
    df[EST_SALUD] = df[EST_SALUD].astype(str)
    
    return df

df = load_data()
coords_rad = np.vstack([np.radians(df[COL_LAT].values), np.radians(df[COL_LONG].values)]).T
tree = BallTree(coords_rad, metric="haversine")

@app.post("/api/salud", response_model=SaludResponseModel)
def post_establecimientos(req: SaludRequestModel) -> SaludResponseModel:

    point_rad = np.radians([[req.lat, req.long]])
    radius_rad = req.radius_km / RADIUS_EARTH # 
    indices = tree.query_radius(point_rad, r=radius_rad)[0]

    distances_km = haversine_vectorized(
        req.lat, req.long, 
        df.iloc[indices][COL_LAT].values, 
        df.iloc[indices][COL_LONG].values
    )

    df_results = df.iloc[indices].copy()
    df_results[KM_DISTANCE] = distances_km
    df_results = df_results.sort_values(by=KM_DISTANCE).head(req.top_n)

    results = [
        SaludResultModel(
            lat=row[COL_LAT],
            long=row[COL_LONG], 
            fna=row[EST_SALUD],
            distance_km=row[KM_DISTANCE]
        )
        for _, row in df_results.iterrows()
    ]

    return SaludResponseModel(request=req, results=results)