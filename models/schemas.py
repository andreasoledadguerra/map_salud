from pydantic import BaseModel
from typing import List

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