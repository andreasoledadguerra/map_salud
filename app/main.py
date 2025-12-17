import pandas as pd
import numpy as np
from fastapi import FastAPI, requests
from pydantic import BaseModel
from sklearn.neighbors import BallTree
from typing import List

from app.data.constants import (
    PATH,
    RADIUS_EARTH,
    COL_LAT,
    COL_LONG,
    EST_SALUD,
    KM_DISTANCE,
)

from process_stream import load_data
#from app.models.schemas import SaludRequestModel,SaludResponseModel,SaludResultModel

app = FastAPI()





df = load_data(PATH)

#
#distances = haversine_balltree()



@app.post("/api/salud", response_model=SaludResponseModel)
def post_establecimientos(req: SaludRequestModel) -> SaludResponseModel:

    point_rad = np.radians([[req.lat, req.long]])
    radius_rad = req.radius_km / RADIUS_EARTH # 
    indices = tree.query_radius(point_rad, r=radius_rad)[0]

    distances_km = haversine_balltree(
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