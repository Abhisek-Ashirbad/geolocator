from fastapi import APIRouter, HTTPException
from src.models import GeolocationRequest, GeolocationResponse
import requests
import time

router = APIRouter()

# Function to reverse geocode coordinates using Nominatim
def reverse_geocode(latitude: float, longitude: float) -> str:
    # Add a 1-second delay to respect Nominatim's rate limits
    time.sleep(1)
    
    # Nominatim API endpoint
    url = "https://nominatim.openstreetmap.org/reverse.php"
    # Parameters for the API request
    params = {
        "lat": latitude,
        "lon": longitude,
        "format": "json",  # Request JSON response
    }
    # Headers to identify your application (required by Nominatim)
    headers = {
        "User-Agent": "YourAppName/1.0 (your@email.com)"  # Replace with your app name and email
    }
    
    try:
        # Make the request
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the JSON response
        data = response.json()
        print("Nominatim API Response:", data)  # Debugging: Print the response
        
        # Extract the display name (full address)
        if "display_name" in data:
            return data["display_name"]
        else:
            return "Unknown location"
    except requests.exceptions.RequestException as e:
        # Log the error and raise an HTTPException
        print(f"Error calling Nominatim API: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch location data")

# Endpoint to receive geolocation
@router.post("/get-geolocation", response_model=GeolocationResponse)
async def get_geolocation(geolocation: GeolocationRequest):
    try:
        # Reverse geocode the coordinates
        place_name = reverse_geocode(geolocation.latitude, geolocation.longitude)
        # Return the received geolocation, place name, and a message
        return {
            "latitude": geolocation.latitude,
            "longitude": geolocation.longitude,
            "place_name": place_name,
            "message": "Geolocation data retrieved successfully.",
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))