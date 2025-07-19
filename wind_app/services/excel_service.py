"""
Excel Service Module

Handles loading and parsing of wind farm data from Excel files.
Provides structured access to wind farm information including locations,
capacities, and operational parameters.

The Excel file should contain columns:
- ID: Unique identifier for each wind farm
- Name: Wind farm name
- Overall capacity: Total capacity in MW
- Number of turbines: Count of turbines
- Country: Location country
- Latitude: Geographic latitude
- Longitude: Geographic longitude
"""

import os

import pandas as pd

from wind_app.utils import log


class WindFarmDataLoader:
    """Simple service for loading wind farm data from Excel files"""

    def __init__(self, data_file_path: str) -> None:
        """
        Initialize the data loader with file path

        Args:
            data_file_path: Path to the Excel file containing wind farm data
        """
        self.data_file_path = data_file_path

    def load_wind_farm_data(self) -> pd.DataFrame:
        """
        Load wind farm data from Excel file with proper column types

        Returns:
            DataFrame containing wind farm information, or empty DataFrame if loading fails
        """
        # Check if file exists
        if not os.path.exists(self.data_file_path):
            log(f"❌ Data file not found: {self.data_file_path}")
            return pd.DataFrame()

        try:
            log(f"📊 Loading wind farm data from: {self.data_file_path}")

            # Define expected column types for data validation
            column_types = {
                "ID": str,
                "Name": str,
                "Overall capacity": float,
                "Number of turbines": int,
                "Country": str,
                "Latitude": float,
                "Longitude": float,
            }

            # Load Excel file with specified column types
            wind_farm_data = pd.read_excel(self.data_file_path, dtype=column_types)

            # Validate that we have data
            if wind_farm_data.empty:
                log("⚠️  Excel file is empty")
                return pd.DataFrame()

            log(f"✅ Successfully loaded {len(wind_farm_data)} wind farms")
            return wind_farm_data

        except FileNotFoundError:
            log(f"❌ Excel file not found: {self.data_file_path}")
            return pd.DataFrame()

        except pd.errors.EmptyDataError:
            log("❌ Excel file is empty or contains no data")
            return pd.DataFrame()

        except Exception as error:
            log(f"❌ Error loading Excel file: {error}")
            return pd.DataFrame()
