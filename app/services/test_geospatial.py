import numpy as np
import pytest
import os
from geospatial import haversine_vectorized

def test_haversine_vectorized():
    
    # Test data
    lat1 = 10.0
    lon1 = 20.0
    lat2_arr = np.array([10.0, 11.0, 12.0])
    lon2_arr = np.array([20.0, 21.0, 22.0])

    # Calculate distances
    distances = haversine_vectorized(lat1, lon1, lat2_arr, lon2_arr)
    
    # Expected distances calculated manually or from a reliable source 
    expected_distances = np.array([0.0, 157.24938127194397, 314.4748056038168])

    # Assert that the calculated distances are close to the expected distances
    np.testing.assert_allclose(distances, expected_distances, rtol=1e-3)
    



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