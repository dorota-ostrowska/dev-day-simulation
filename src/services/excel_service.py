import pandas as pd

class ExcelService:
    """Service for handling wind farm data from Excel files"""

    def __init__(self, file_path: str) -> None:
        """
        Initialize Excel service with file path
        """
        self.file_path = file_path

    def load_windfarm_data(self) -> pd.DataFrame:
        """
        Load wind farms data from Excel file
        """
        try:
            df = pd.read_excel(
                self.file_path,
                dtype={
                    'ID': str,
                    'Name': str,
                    'Overall capacity': float,
                    'Number of turbines': int,
                    'Country': str,
                    'Latitude': float,
                    'Longitude': float,
                }
            )
            return df
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            return pd.DataFrame()
