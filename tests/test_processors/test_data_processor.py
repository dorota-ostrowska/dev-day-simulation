import pytest
from pytest_mock import mocker
import pandas as pd

from src.processors.data_processor import WindFarmDataProcessor
from src.services.excel_service import ExcelService
from src.services.weather_service import WeatherService

@pytest.fixture
def mock_excel_service(mocker):
    """Create mock Excel service with test data"""
    service = mocker.Mock(spec=ExcelService)
    test_data = {
        'ID': ['ANH', 'AVD', 'HKW', 'ARK'],
        'Name': ['Anholt', 'Avedøre', 'Hornsea', 'Arkona'],
        'Overall capacity': [400.0, 7.2, 1320.0, 385.0],
        'Number of turbines': [111, 2, 174, 60],
        'Country': ['Denmark', 'Denmark', 'UK', 'Germany'],
        'Latitude': [56.6, 56.6, 53.8833, 54.7833],
        'Longitude': [11.21, 12.458333, 1.9167, 13.9833]
    }
    service.load_windfarm_data.return_value = pd.DataFrame(test_data)
    return service

@pytest.fixture
def mock_weather_service(mocker):
    """Create mock weather service"""
    service = mocker.Mock(spec=WeatherService)
    service.get_wind_speed_data.return_value = 10.0  
    return service

@pytest.fixture
def processor(mock_excel_service, mock_weather_service):
    """Create WindFarmDataProcessor with mock services"""
    return WindFarmDataProcessor(mock_excel_service, mock_weather_service)

def test_process_data(processor):
    """Test data processing pipeline"""
    df = processor.process_data()
    
    # Check if DataFrame was created
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df) == 4
    
    # Check if new columns were added
    assert 'Current wind speed' in df.columns
    assert 'Estimated power' in df.columns
    
    # Check wind speed data
    assert all(df['Current wind speed'] == 10.0)

def test_power_calculation():
    """Test power curve calculations"""
    test_cases = [
        (2, 100, 0),      # Below cut-in
        (4, 100, 10),     # 10% at 4 m/s
        (8, 100, 60),     # 60% at 8 m/s
        (12, 100, 100),   # 100% at rated speed
        (26, 100, 0)      # Safety shutdown
    ]
    
    for wind_speed, capacity, expected in test_cases:
        result = WindFarmDataProcessor._estimate_power(wind_speed, capacity)
        assert result == pytest.approx(expected, rel=1e-2)

def test_country_comparison(processor):
    """Test country statistics aggregation"""
    processor.process_data()
    stats = processor.get_country_comparison()
    
    # Test presence of all countries
    expected_countries = ['Denmark', 'UK', 'Germany']
    assert all(country in stats for country in expected_countries)

    # Test all countries have required fields
    for country in stats.values():
        assert 'Overall capacity' in country
        assert 'Estimated power' in country
    
    # Test Denmark values
    denmark = stats['Denmark']
    assert denmark['Overall capacity'] == pytest.approx(407.2)  # 400 + 7.2
    
    # Test UK values
    uk = stats['UK']
    assert uk['Overall capacity'] == pytest.approx(1320.0)
    
    # Test Germany values
    germany = stats['Germany']
    assert germany['Overall capacity'] == pytest.approx(385.0)
