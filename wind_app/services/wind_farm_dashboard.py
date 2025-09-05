"""
Wind Farm Dashboard Service

Main dashboard logic that combines data loading, weather information,
and power calculations to create a comprehensive wind farm monitoring system.
Processes raw data into formatted dashboard displays and performance metrics.

Features:
- Real-time weather data integration
- Power generation estimates
- Performance analytics
- Country-level statistics
"""

from datetime import datetime
from typing import Any

import numpy as np
from pandas import DataFrame

from wind_app.services.weather_service import WeatherService
from wind_app.services.wind_farm_service.interface import AbstractWindFarmService
from wind_app.utils import log


class WindFarmDashboard:
    """
    Complete wind farm dashboard that handles data loading, processing, and formatting

    This class combines data loading, weather fetching, power calculations,
    and dashboard formatting into one simple, easy-to-understand module.
    """

    def __init__(
        self,
        wind_farm_service: AbstractWindFarmService,
        weather_service: WeatherService | None = None,
    ) -> None:
        """
        Initialize the wind farm dashboard

        Args:
            data_file_path: Path to the Excel file containing wind farm data
        """
        self._wind_farm_service = wind_farm_service
        self._weather_service = weather_service if weather_service else WeatherService()

    def process_wind_farm_data(self, wind_farm_data: DataFrame) -> None:
        """Add real-time weather information to wind farm data"""
        log("📊 Loading wind farm data...")

        if wind_farm_data.empty:
            log("❌ No wind farm data loaded")
            return

        log(f"✅ Loaded {len(wind_farm_data)} wind farms")
        log("🌤️  Fetching real-time weather data...")

        # Add current wind speeds for each farm
        wind_farm_data["Current wind speed"] = wind_farm_data.apply(
            lambda farm: self._weather_service.get_current_wind_speed(
                farm["Latitude"], farm["Longitude"]
            ),
            axis=1,
        )

        # Calculate estimated power output based on wind speeds
        log("⚡ Calculating power output...")
        wind_farm_data["Estimated power"] = wind_farm_data.apply(
            lambda farm: self.calculate_turbine_power(
                wind_speed=farm["Current wind speed"],
                max_capacity=farm["Overall capacity"],
            )
            if farm["Current wind speed"] is not None
            else None,
            axis=1,
        )

        log("✅ Data processing complete!")

    def get_dashboard_data(self) -> dict[str, Any]:
        """
        Get all formatted data needed for the dashboard display

        Returns:
            Dictionary with all dashboard data ready for templates
        """

        # Load base wind farm data from Excel
        wind_farm_data = self._wind_farm_service.load_wind_farm_data()
        self.process_wind_farm_data(wind_farm_data=wind_farm_data)

        # If still no data, return empty dashboard
        if wind_farm_data is None or wind_farm_data.empty:
            return self.get_empty_dashboard_data()

        # Calculate country statistics
        country_stats = self._calculate_country_statistics(wind_farm_data)

        # Prepare all dashboard sections
        return {
            "wind_farms": self._prepare_wind_farm_cards(wind_farm_data),
            "country_performance": self._prepare_country_cards(country_stats),
            "fleet_summary": self._calculate_fleet_summary(wind_farm_data),
            "status_metrics": self._get_status_metrics(
                country_stats=country_stats, wind_farm_data=wind_farm_data
            ),
        }

    def calculate_turbine_power(self, wind_speed: float, max_capacity: float) -> float:
        """
        Calculate estimated power output based on wind speed using a simplified power curve

        Args:
            wind_speed: Current wind speed in m/s
            max_capacity: Maximum power capacity in MW

        Returns:
            Estimated power output in MW
        """
        # Handle missing or invalid wind speed
        if not wind_speed or wind_speed <= 0:
            return 0.0

        # Wind turbine power curve (simplified for offshore turbines)
        if wind_speed < 3 or wind_speed > 25:
            return 0.0  # Too weak or too strong (safety shutdown)
        elif wind_speed >= 12:
            return max_capacity  # Full power at high wind speeds
        else:
            # Power curve points for interpolation
            power_curve = {
                4: 0.1,  # 10% power at 4 m/s
                6: 0.3,  # 30% power at 6 m/s
                8: 0.6,  # 60% power at 8 m/s
                10: 0.9,  # 90% power at 10 m/s
                12: 1.0,  # 100% power at 12+ m/s
            }

            # Find the right power factor using linear interpolation
            speeds = list(power_curve.keys())
            for i, speed in enumerate(speeds):
                if wind_speed <= speed:
                    if i == 0:  # Between 3-4 m/s
                        power_factor = power_curve[speed] * (wind_speed - 3)
                    else:  # Linear interpolation between points
                        speed_low = speeds[i - 1]
                        speed_high = speed
                        power_low = power_curve[speed_low]
                        power_high = power_curve[speed]
                        power_factor = power_low + (power_high - power_low) * (
                            wind_speed - speed_low
                        ) / (speed_high - speed_low)

                    return max_capacity * power_factor

            return max_capacity  # Fallback for 10-12 m/s range

    def _calculate_country_statistics(
        self, wind_farm_data: DataFrame
    ) -> dict[Any, Any]:
        """Calculate aggregated statistics by country"""
        fixed_wind_farm_data = wind_farm_data.copy()
        fixed_wind_farm_data["Estimated power"].replace(
            to_replace=np.nan, value=0, inplace=True
        )
        return (
            fixed_wind_farm_data.groupby("Country")
            .agg({"Overall capacity": "sum", "Estimated power": "sum"})
            .to_dict("index")
        )

    def _prepare_wind_farm_cards(
        self, wind_farm_data: DataFrame
    ) -> list[dict[str, Any]]:
        """Prepare individual wind farm cards with formatted data"""
        wind_farm_cards = []

        for _, farm in wind_farm_data.iterrows():
            # Get values with safe defaults
            current_wind_speed = farm.get("Current wind speed", None)
            estimated_power = farm.get("Estimated power", None)
            overall_capacity = farm.get("Overall capacity", 0) or 0

            # Calculate efficiency percentage
            efficiency = (
                (
                    (estimated_power / overall_capacity * 100)
                    if overall_capacity > 0
                    else 0
                )
                if estimated_power is not None
                else None
            )

            # Prepare card data
            farm_card = {
                "name": farm.get("Name", "Unknown"),
                "country": farm.get("Country", "Unknown"),
                "current_wind_speed": round(current_wind_speed, 1)
                if current_wind_speed is not None
                else _NO_DATA_SYMBOL,
                "estimated_power": round(estimated_power, 1)
                if estimated_power is not None
                else _NO_DATA_SYMBOL,
                "overall_capacity": round(overall_capacity, 0),
                "number_of_turbines": int(farm.get("Number of turbines", 0)),
                "efficiency": round(efficiency, 1)
                if efficiency is not None
                else _NO_DATA_SYMBOL,
                "performance_rating": self.get_performance_rating(efficiency)
                if efficiency is not None
                else _NO_DATA_SYMBOL,
                "progress_width": min(round(efficiency, 1), 100)
                if efficiency is not None
                else _NO_DATA_SYMBOL,
            }

            wind_farm_cards.append(farm_card)

        return wind_farm_cards

    def _prepare_country_cards(self, country_stats) -> list[dict[str, Any]]:
        """Prepare country performance cards"""
        country_cards = []

        for country, stats in country_stats.items():
            overall_capacity = stats.get("Overall capacity", 0)
            estimated_power = stats.get("Estimated power", 0)

            # Calculate capacity factor
            capacity_factor = (
                (estimated_power / overall_capacity * 100)
                if overall_capacity > 0
                else 0
            )

            country_card = {
                "name": country,
                "total_capacity": round(overall_capacity, 1),
                "current_output": round(estimated_power, 1),
                "capacity_factor": round(capacity_factor, 1),
                "performance_level": self.get_country_performance_level(
                    capacity_factor
                ),
                "progress_width": min(round(capacity_factor, 1), 100),
            }

            country_cards.append(country_card)

        return country_cards

    def _calculate_fleet_summary(self, wind_farm_data: DataFrame) -> dict[str, Any]:
        """Calculate fleet-wide summary metrics"""
        total_capacity = wind_farm_data["Overall capacity"].sum()
        total_generation = wind_farm_data["Estimated power"].fillna(0).sum()

        # Calculate fleet efficiency
        fleet_efficiency = (
            (total_generation / total_capacity * 100) if total_capacity > 0 else 0
        )

        # Calculate environmental impact estimates
        co2_avoided_per_hour = total_generation * 0.82  # tons CO2 per MWh
        homes_powered = (
            total_generation * 1000
        ) / 2.5  # Average home consumption 2.5 kW

        return {
            "total_capacity": round(total_capacity, 1),
            "total_generation": round(total_generation, 1),
            "fleet_efficiency": round(fleet_efficiency, 1),
            "co2_avoided": round(co2_avoided_per_hour, 0),
            "homes_powered": round(homes_powered, 0),
            "progress_width": min(round(fleet_efficiency, 1), 100),
        }

    def _get_status_metrics(
        self, *, country_stats, wind_farm_data: DataFrame
    ) -> dict[str, Any]:
        """Get metrics for the status bar"""
        return {
            "active_farms": len(wind_farm_data),
            "countries": len(country_stats),
            "total_capacity": round(wind_farm_data["Overall capacity"].sum(), 1),
            "last_updated": datetime.now().strftime("%B %d, %Y at %I:%M %p"),
        }

    def get_performance_rating(self, efficiency: float) -> str:
        """Get performance rating based on efficiency percentage"""
        if efficiency >= 80:
            return "Excellent"
        elif efficiency >= 60:
            return "Very Good"
        elif efficiency >= 40:
            return "Good"
        elif efficiency >= 20:
            return "Fair"
        else:
            return "Low"

    def get_country_performance_level(self, capacity_factor: float) -> str:
        """Get performance level for countries based on capacity factor"""
        if capacity_factor >= 70:
            return "Excellent"
        elif capacity_factor >= 40:
            return "Good"
        elif capacity_factor >= 20:
            return "Fair"
        else:
            return "Low"

    def get_empty_dashboard_data(self) -> dict[str, Any]:
        """Return empty dashboard data structure for error cases"""
        return {
            "wind_farms": [],
            "country_performance": [],
            "fleet_summary": {
                "total_capacity": 0,
                "total_generation": 0,
                "fleet_efficiency": 0,
                "co2_avoided": 0,
                "homes_powered": 0,
                "progress_width": 0,
            },
            "status_metrics": {
                "active_farms": 0,
                "countries": 0,
                "total_capacity": 0,
                "last_updated": "No data available",
            },
        }


_NO_DATA_SYMBOL = "-"  # Symbol for missing data in templates
