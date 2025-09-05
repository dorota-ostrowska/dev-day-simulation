import pandas as pd
import pytest
from pytest_mock import MockerFixture

from wind_app.services.weather_service import WeatherService
from wind_app.services.wind_farm_dashboard import _NO_DATA_SYMBOL, WindFarmDashboard
from wind_app.services.wind_farm_service.excel import WindFarmServiceExcel


@pytest.fixture
def mock_wind_farm_data() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "ID": ["ANH", "AVD"],
            "Name": ["Anholt", "Avedøre"],
            "Overall capacity": [400.0, 7.2],
            "Number of turbines": [111, 2],
            "Country": ["Denmark", "Denmark"],
            "Latitude": [56.6, 56.6],
            "Longitude": [11.21, 12.458333],
            "Current wind speed": [10.0, 8.0],
            "Estimated power": [360.0, 4.32],  # 90% and 60% of capacity
        }
    )


@pytest.fixture
def mock_wind_farm_service(mocker: MockerFixture, mock_wind_farm_data: pd.DataFrame):
    loader = mocker.Mock()
    loader.load_wind_farm_data.return_value = mock_wind_farm_data
    return loader


@pytest.fixture
def mock_weather_service(mocker: MockerFixture):
    service = mocker.Mock()
    service.get_current_wind_speed.return_value = 10.0
    return service


@pytest.fixture
def dashboard(
    mock_wind_farm_service: WindFarmServiceExcel, mock_weather_service: WeatherService
) -> WindFarmDashboard:
    dashboard = WindFarmDashboard(
        wind_farm_service=mock_wind_farm_service, weather_service=mock_weather_service
    )
    return dashboard


def test_calculate_turbine_power() -> None:
    wind_farm_service = WindFarmServiceExcel(data_file_path="dummy/path.xlsx")
    dashboard = WindFarmDashboard(wind_farm_service=wind_farm_service)
    test_cases = [
        (0, 100, 0),  # No wind
        (2, 100, 0),  # Below cut-in
        (4, 100, 10),  # 10% at 4 m/s
        (8, 100, 60),  # 60% at 8 m/s
        (12, 100, 100),  # 100% at rated speed
        (26, 100, 0),  # Safety shutdown
    ]

    for wind_speed, capacity, expected in test_cases:
        result = dashboard.calculate_turbine_power(wind_speed, capacity)
        assert result == pytest.approx(expected, rel=1e-2)


def test_performance_ratings(dashboard: WindFarmDashboard) -> None:
    # Test farm performance ratings
    assert dashboard.get_performance_rating(85) == "Excellent"
    assert dashboard.get_performance_rating(65) == "Very Good"
    assert dashboard.get_performance_rating(45) == "Good"
    assert dashboard.get_performance_rating(25) == "Fair"
    assert dashboard.get_performance_rating(15) == "Low"

    # Test country performance levels
    assert dashboard.get_country_performance_level(75) == "Excellent"
    assert dashboard.get_country_performance_level(45) == "Good"
    assert dashboard.get_country_performance_level(25) == "Fair"
    assert dashboard.get_country_performance_level(15) == "Low"


def test_get_dashboard_data(dashboard: WindFarmDashboard) -> None:
    # When
    data = dashboard.get_dashboard_data()
    # Then
    assert data["wind_farms"] == [
        {
            "name": "Anholt",
            "country": "Denmark",
            "current_wind_speed": 10.0,
            "estimated_power": 360.0,
            "overall_capacity": 400.0,
            "number_of_turbines": 111,
            "efficiency": 90.0,
            "performance_rating": "Excellent",
            "progress_width": 90.0,
        },
        {
            "name": "Avedøre",
            "country": "Denmark",
            "current_wind_speed": 10.0,
            "estimated_power": 6.5,
            "overall_capacity": 7.0,
            "number_of_turbines": 2,
            "efficiency": 90.0,
            "performance_rating": "Excellent",
            "progress_width": 90.0,
        },
    ]
    assert data["country_performance"] == [
        {
            "capacity_factor": 90.0,
            "current_output": 366.5,
            "name": "Denmark",
            "performance_level": "Excellent",
            "progress_width": 90.0,
            "total_capacity": 407.2,  # 400 + 7.2
        },
    ]
    assert float(data["fleet_summary"]["total_capacity"]) == 407.2
    assert data["status_metrics"]["active_farms"] == 2


def test_get_dashboard_data_with_empty_winds(
    mocker: MockerFixture, mock_wind_farm_service: WindFarmServiceExcel
) -> None:
    # When
    weather_service = mocker.Mock()
    weather_service.get_current_wind_speed.return_value = None  # simulate API failure
    dashboard = WindFarmDashboard(
        wind_farm_service=mock_wind_farm_service, weather_service=weather_service
    )
    data = dashboard.get_dashboard_data()
    # Then
    wind_farm_data = data["wind_farms"]

    for column in {
        "current_wind_speed",
        "estimated_power",
        "efficiency",
        "performance_rating",
        "progress_width",
    }:
        assert all(
            wind_farm_data[column] == _NO_DATA_SYMBOL
            for wind_farm_data in wind_farm_data
        )
