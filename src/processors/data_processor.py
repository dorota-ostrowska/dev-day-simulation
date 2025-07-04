import pandas as pd

from src.services.excel_service import ExcelService
from src.services.weather_service import WeatherService


class WindFarmDataProcessor:
    def __init__(self, excel_service: ExcelService, weather_service: WeatherService) -> None:
        self.excel_service = excel_service
        self.weather_service = weather_service
        self.windfarms_df = None
        self.processed_data = None

    def process_data(self) -> pd.DataFrame:
        """Load and process wind farm data with current weather"""
        # Load base data
        self.windfarms_df = self.excel_service.load_windfarm_data()
        
        # Add current wind speeds
        self.windfarms_df['Current wind speed'] = self.windfarms_df.apply(
            lambda row: self.weather_service.get_wind_speed_data(
                row['Latitude'], 
                row['Longitude']
            ), 
            axis=1
        )
        
        # Calculate estimated current power output
        self.windfarms_df['Estimated power'] = self.calculate_power_output()
        
        return self.windfarms_df

    def calculate_power_output(self) -> pd.Series:
        """
        Calculate estimated power output based on wind speed
        Using simplified power curve
        """
        return self.windfarms_df.apply(
            lambda row: self._estimate_power(
                row['Current wind speed'], 
                row['Overall capacity']
            ), 
            axis=1
        )

    @staticmethod
    def _estimate_power(wind_speed: float, capacity: float) -> float:
        """
        Simplified power curve calculation for offshore wind turbines
        Args:
            wind_speed: Current wind speed in m/s
            capacity: Maximum power capacity in MW
        Returns:
            Estimated power output in MW
        Power curve:
            0-3 m/s:   0% (too weak)
            4 m/s:     10%
            6 m/s:     30%
            8 m/s:     60%
            10 m/s:    90%
            12-25 m/s: 100% (rated power)
            >25 m/s:   0% (shutdown for safety)
        """
        if wind_speed < 3 or wind_speed > 25:
            return 0
        elif wind_speed >= 12:
            return capacity
        else:
            # Create power curve points
            power_curve = {
                4: 0.1,  # 10%
                6: 0.3,  # 30%
                8: 0.6,  # 60%
                10: 0.9, # 90%
                12: 1.0  # 100%
            }
            
            # Find nearest points for interpolation
            speeds = list(power_curve.keys())
            for i, speed in enumerate(speeds):
                if wind_speed <= speed:
                    if i == 0:  # Between 3-4 m/s
                        return capacity * (power_curve[speed] * (wind_speed - 3))
                    else:  # Linear interpolation between points
                        speed_low = speeds[i-1]
                        speed_high = speed
                        power_low = power_curve[speed_low]
                        power_high = power_curve[speed]
                        power_factor = power_low + (power_high - power_low) * \
                            (wind_speed - speed_low) / (speed_high - speed_low)
                        return capacity * power_factor
            
            return capacity  # Fallback for 10-12 m/s range

    def get_country_comparison(self) -> dict:
        """Compare total capacity and current output by country"""
        if self.windfarms_df is None:
            self.process_data()
            
        return self.windfarms_df.groupby('Country').agg({
            'Overall capacity': 'sum',
            'Estimated power': 'sum'
        }).to_dict('index')
