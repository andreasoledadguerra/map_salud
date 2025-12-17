import numpy as np
from sklearn.neighbors import BallTree

from app.data.constants import RADIUS_EARTH


#def haversine_balltree(
#    lat_in: float,
#    lon_in: float,
#    lat_out: np.ndarray,
#    lon_out: np.ndarray
#) -> np.ndarray:
#    """
#    Calcula distancias Haversine usando BallTree.
#    Devuelve distancias en kilómetros.
#    """
#    point = np.radians([[lat_in, lon_in]])
#    coords = np.radians(np.column_stack((lat_out, lon_out)))
#
#    tree = BallTree(coords, metric="haversine")
#    distances, _ = tree.query(point, k=len(coords))
#
#    return distances[0] * RADIUS_EARTH