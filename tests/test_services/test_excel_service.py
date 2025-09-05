import pandas as pd
import pytest

from wind_app.services.wind_farm_service.excel import WindFarmServiceExcel


@pytest.fixture
def test_data_loader() -> WindFarmServiceExcel:
    return WindFarmServiceExcel("tests/test_data/test_windfarms.xlsx")


def test_load_wind_farm_data(test_data_loader: WindFarmServiceExcel):
    df = test_data_loader.load_wind_farm_data()

    # Basic DataFrame checks
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df) == 2  # Check for exactly 2 rows

    # Check column names
    expected_columns = [
        "ID",
        "Name",
        "Overall capacity",
        "Number of turbines",
        "Country",
        "Latitude",
        "Longitude",
    ]
    assert all(col in df.columns for col in expected_columns)

    # Check specific values for Anholt
    anholt = df[df["ID"] == "ANH"].iloc[0]
    assert anholt["Name"] == "Anholt"
    assert anholt["Overall capacity"] == 400
    assert anholt["Number of turbines"] == 111
    assert anholt["Country"] == "Denmark"
    assert anholt["Latitude"] == 56.6
    assert anholt["Longitude"] == 11.21

    # Check specific values for Avedøre
    avedore = df[df["ID"] == "AVD"].iloc[0]
    assert avedore["Name"] == "Avedøre"
    assert avedore["Overall capacity"] == 7.2
    assert avedore["Number of turbines"] == 2
    assert avedore["Country"] == "Denmark"
    assert avedore["Latitude"] == 56.6
    assert avedore["Longitude"] == pytest.approx(12.458333, rel=1e-6)
