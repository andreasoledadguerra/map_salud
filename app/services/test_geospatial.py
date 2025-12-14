import numpy as np
import pytest
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
    expected_distances = np.array([0.0, 155.941215, 311.622025])

    # Assert that the calculated distances are close to the expected distances
    np.testing.assert_allclose(distances, expected_distances, rtol=1e-3)
    