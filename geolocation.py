
import math
import requests
from typing import Tuple, Optional

class LocationService:
    def __init__(self):
        # You can use a free geocoding service like OpenStreetMap Nominatim
        self.geocoding_base_url = "https://nominatim.openstreetmap.org/search"
    
    def get_coordinates(self, address: str) -> Optional[Tuple[float, float]]:
        """Get latitude and longitude from address"""
        try:
            params = {
                'q': address,
                'format': 'json',
                'limit': 1
            }
            response = requests.get(self.geocoding_base_url, params=params)
            data = response.json()
            
            if data:
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                return (lat, lon)
            return None
        except Exception as e:
            print(f"Geocoding error: {e}")
            return None
    
    def calculate_distance(self, coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
        """Calculate distance between two coordinates using Haversine formula (in km)"""
        lat1, lon1 = coord1
        lat2, lon2 = coord2
        
        # Convert latitude and longitude from degrees to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Radius of earth in kilometers
        r = 6371
        return c * r
    
    def calculate_delivery_charge(self, distance_km: float) -> float:
        """Calculate delivery charge based on distance"""
        if distance_km <= 5:
            return 2.99  # Base charge for nearby delivery
        elif distance_km <= 10:
            return 4.99
        elif distance_km <= 20:
            return 7.99
        elif distance_km <= 50:
            return 12.99
        else:
            return 19.99  # Maximum charge for far deliveries

# Store location (you should set this to your actual store coordinates)
STORE_LOCATION = (40.7128, -74.0060)  # Example: New York City coordinates
