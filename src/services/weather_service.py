import requests
from private_config import weather_api_key

class WeatherService:
    """Service for fetching weather data from OpenWeatherMap API"""
    
    def __init__(self) -> None:
        self.api_key = weather_api_key
        if self.api_key == "your_api_key_here":
            raise ValueError("Please create 'secrets.py' file in the root folder and set your OpenWeather API key")
        if not self.api_key:
            raise ValueError("OpenWeather API key not found in environment variables")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_wind_speed_data(self, lat: float, lon: float) -> float | None:
        """
        Get weather data for specific coordinates
        Args:
            lat: Latitude of the location
            lon: Longitude of the location
        Returns:
            Float with wind speed data or None if request fails
        """
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            wind_speed = data['wind']['speed']  # wind speed in m/s
            return wind_speed
        except requests.RequestException as e:
            print(f"Failed to fetch weather data: {e}")
            return None
        