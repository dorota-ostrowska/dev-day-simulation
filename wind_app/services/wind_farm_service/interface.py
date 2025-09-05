from abc import ABC, abstractmethod

import pandas as pd


class AbstractWindFarmService(ABC):
    """Abstract base class for wind farm services."""

    @abstractmethod
    def load_wind_farm_data(self) -> pd.DataFrame:
        """Get data frame with wind farm information."""
        raise NotImplementedError("This method should be implemented by subclasses.")
