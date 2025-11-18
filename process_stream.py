import pandas as pd
import numpy as np



def load_data(path="establecimientos-salud-publicos.csv"):
    df = pd.read_csv(path, delimiter=";")
    df = df[["lat", "long", "fna"]].copy()
    df["lat"] = df["lat"].astype(float)
    df["long"] = df["long"].astype(float)
    df["fna"] = df["fna"].astype(str)
    
    return df

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