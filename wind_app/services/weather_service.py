"""
Weather Service Module

Handles integration with OpenWeatherMap API to fetch real-time weather data
for wind farm locations. Provides wind speed, direction and temperature data
for power generation calculations.

Example:
    service = WeatherService()
    weather_data = service.get_weather_data(56.6, 11.21)
"""

import httpx

from wind_app.utils import log

# NOTE: This import is used to load the API key from private_config.py.
#       If the file is not found and tests are not running - it raises an ImportError.
try:
    from wind_app.private_config import weather_api_key
except ImportError:
    import os

    are_tests_running = os.getenv("PYTEST_VERSION") is not None

    if not are_tests_running:
        raise

    weather_api_key = "some_not_existing_api_key_for_tests"


class WeatherService:
    """Simple service for fetching wind speed data from OpenWeatherMap API"""

    def __init__(self, http_client: httpx.Client | None = None) -> None:
        """Initialize the weather service with API key validation"""
        self.api_key = weather_api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

        if http_client is None:
            self.http_client = httpx.Client()
        else:
            self.http_client = http_client

        # Check if API key is properly configured
        if self.api_key == "your_api_key_here":
            raise ValueError(
                "Please set your OpenWeather API key in src/private_config.py"
            )
        if not self.api_key:
            raise ValueError("OpenWeather API key is missing")

    def get_current_wind_speed(self, latitude: float, longitude: float) -> float | None:
        """
        Get current wind speed for specific coordinates

        Args:
            latitude: Location latitude (-90.0 to 90.0)
            longitude: Location longitude (-180.0 to 180.0)

        Returns:
            Wind speed in meters per second, or 0 if request fails
        """
        # Prepare API request parameters
        request_params: dict[str, str | float] = {
            "lat": latitude,
            "lon": longitude,
            "appid": self.api_key,
            "units": "metric",  # Use metric units (m/s for wind speed)
        }

        try:
            # Make API request
            response = self.http_client.get(
                self.base_url, params=request_params, timeout=10
            )
            response.raise_for_status()  # Raise exception for HTTP errors

            # TODO: use LLM to prepare data model for the response
            # .      Implement WeatherData class inheriting from typing.TypedDict
            # .      and use it as type of weather_data variable
            # .      This will allow to use IDE autocompletion and type checking

            # Parse JSON response
            weather_data = response.json()
            wind_speed = weather_data["wind"]["speed"]

            log(f"✅ Wind speed for ({latitude}, {longitude}): {wind_speed} m/s")
            return wind_speed

        except httpx.RequestError as error:
            log(f"❌ Weather API request failed: {error}")
            return None

        except KeyError:
            log("❌ Wind data not found in weather response")
            return None

        except Exception as error:
            log(f"❌ Unexpected error getting wind speed: {error}")
            return None
