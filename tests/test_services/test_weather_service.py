import pytest
from src.services.weather_service import WeatherService

@pytest.fixture
def weather_service():
    return WeatherService()

def test_weather_service_initialization(weather_service):
    """Test if WeatherService initializes properly"""
    assert isinstance(weather_service, WeatherService)
    assert weather_service.base_url == "https://api.openweathermap.org/data/2.5/weather"
    assert weather_service.api_key is not None

def test_get_wind_speed_data(weather_service):
    """Test weather data retrieval for Anholt wind farm"""
    # Coordinates for Anholt wind farm
    lat, lon = 56.6, 11.21
    
    wind_speed = weather_service.get_wind_speed_data(lat, lon)
    
    # Check if we got data
    assert wind_speed is not None
    
    # Check data types and ranges
    assert isinstance(wind_speed, (int, float))
    
    # Check reasonable value ranges
    assert 0 <= wind_speed <= 50  # m/s

def test_invalid_coordinates(weather_service):
    """Test handling of invalid coordinates"""
    # Test with invalid latitude
    invalid_data = weather_service.get_wind_speed_data(91, 11.21)
    assert invalid_data is None
    
    # Test with invalid longitude
    invalid_data = weather_service.get_wind_speed_data(56.6, 181)
    assert invalid_data is None
    