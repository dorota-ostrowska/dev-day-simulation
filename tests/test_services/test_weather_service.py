from unittest.mock import MagicMock

import pytest

from wind_app.services.weather_service import WeatherService


@pytest.fixture
def mock_http_client() -> MagicMock:
    return MagicMock()


@pytest.fixture
def weather_service(mock_http_client: MagicMock) -> WeatherService:
    return WeatherService(http_client=mock_http_client)


def test_weather_service_initialization(weather_service: WeatherService) -> None:
    """Test if WeatherService initializes properly"""
    assert weather_service.base_url == "https://api.openweathermap.org/data/2.5/weather"
    assert weather_service.api_key is not None


def test_get_current_wind_speed(
    weather_service: WeatherService, mock_http_client: MagicMock
) -> None:
    """Test mocked weather data retrieval"""

    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = {"wind": {"speed": 10.5}}
    mock_http_client.get.return_value = mock_response

    # Coordinates for Anholt wind farm
    lat, lon = 56.6, 11.21

    wind_speed = weather_service.get_current_wind_speed(latitude=lat, longitude=lon)

    # Check value
    assert wind_speed == 10.5  # m/s


@pytest.mark.integration_test
def test_get_real_current_wind_speed() -> None:
    """Test weather data retrieval for Anholt wind farm"""

    weather_service = WeatherService()

    # Coordinates for Anholt wind farm
    lat, lon = 56.6, 11.21

    wind_speed = weather_service.get_current_wind_speed(lat, lon)

    # Check data types and ranges
    assert isinstance(wind_speed, (int, float))

    # Check reasonable value ranges
    assert 0 <= wind_speed <= 50  # m/s
