import numpy as np
import pytest
import os
from geospatial import haversine_vectorized


# Haversine function
#def haversine_vectorized(lat1:float, lon1:float, lat2_arr:float, lon2_arr:float)->float:
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