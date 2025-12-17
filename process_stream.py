import pandas as pd
import numpy as np

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