# app/api/endpoints/establecimientos.py
import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException

from sklearn.neighbors import BallTree
from app.models.schemas import SaludRequestModel, SaludResponseModel, SaludResultModel
from app.data.process_load_data import load_data
from app.services.geospatial import haversine_vectorized


app = FastAPI()

df = load_data()
coords_rad = np.vstack([np.radians(df["lat"].values), np.radians(df["long"].values)]).T
tree = BallTree(coords_rad, metric="haversine")

# Endpoint para establecimientos de salud
@app.post("/api/salud", response_model=SaludResponseModel)
def post_establecimientos(req: SaludRequestModel) -> SaludResponseModel:
    #try: 
        lat = req.lat
        long = req.long 
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
    #except Exception as e:
    #    raise HTTPException(status_code=500, detail=str(e))