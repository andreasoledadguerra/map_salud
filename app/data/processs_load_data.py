import pandas as pd

from app.data.constants import (
    PATH,
    COL_LAT,
    COL_LONG,
    EST_SALUD,
)

## Load data 
#def load_data(path=PATH) -> pd.DataFrame:
#    df = pd.read_csv(PATH, delimiter=";")
#    df = df[[COL_LAT , COL_LONG, EST_SALUD]].copy()
#    df[COL_LAT] = df[COL_LAT].astype(float)
#    df[COL_LONG] = df[COL_LONG].astype(float)
#    df[EST_SALUD] = df[EST_SALUD].astype(str)
#    
#    return df





# Function to load data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, delimiter=";")
    df = df[["lat", "long", "fna"]].copy()
    df["lat"] = df["lat"].astype(float)
    df["long"] = df["long"].astype(float)
    df["fna"] = df["fna"].astype(str)
    
    return df