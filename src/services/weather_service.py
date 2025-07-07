"""
Weather Service Module

Handles integration with OpenWeatherMap API to fetch real-time weather data
for wind farm locations. Provides wind speed, direction and temperature data
for power generation calculations.

Example:
    service = WeatherService()
    weather_data = service.get_weather_data(56.6, 11.21)
"""

import requests
from src.private_config import weather_api_key


class WeatherService:
    """Simple service for fetching wind speed data from OpenWeatherMap API"""

    def __init__(self) -> None:
        """Initialize the weather service with API key validation"""
        self.api_key = weather_api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

        # Check if API key is properly configured
        if self.api_key == "your_api_key_here":
            raise ValueError(
                "Please set your OpenWeather API key in src/private_config.py"
            )
        if not self.api_key:
            raise ValueError("OpenWeather API key is missing")

    def get_current_wind_speed(self, latitude: float, longitude: float) -> float:
        """
        Get current wind speed for specific coordinates

        Args:
            latitude: Location latitude (-90 to 90)
            longitude: Location longitude (-180 to 180)

        Returns:
            Wind speed in meters per second, or 0 if request fails
        """
        # Prepare API request parameters
        request_params = {
            "lat": latitude,
            "lon": longitude,
            "appid": self.api_key,
            "units": "metric",  # Use metric units (m/s for wind speed)
        }

        try:
            # Make API request
            response = requests.get(self.base_url, params=request_params, timeout=10)
            response.raise_for_status()  # Raise exception for HTTP errors

            # Parse JSON response
            weather_data = response.json()
            wind_speed = weather_data["wind"]["speed"]

            print(f"✅ Wind speed for ({latitude}, {longitude}): {wind_speed} m/s")
            return wind_speed

        except requests.RequestException as error:
            print(f"❌ Weather API request failed: {error}")
            return 0.0  # Return 0 instead of None for easier calculations

        except KeyError:
            print("❌ Wind data not found in weather response")
            return 0.0

        except Exception as error:
            print(f"❌ Unexpected error getting wind speed: {error}")
            return 0.0
