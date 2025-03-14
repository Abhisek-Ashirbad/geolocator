from pydantic import BaseModel

# Pydantic model for request body
class GeolocationRequest(BaseModel):
    latitude: float
    longitude: float

# Pydantic model for response
class GeolocationResponse(BaseModel):
    latitude: float
    longitude: float
    place_name: str
    message: str