from flask import Blueprint, render_template

from src.processors.data_processor import WindFarmDataProcessor
from src.services.excel_service import ExcelService
from src.services.weather_service import WeatherService


home = Blueprint("home", __name__)


@home.route("/")
@home.route("/home")
def display_home():
    excel_service = ExcelService('data/windfarms.xlsx')
    weather_service = WeatherService()
    processor = WindFarmDataProcessor(excel_service, weather_service)
    
    wind_farm_data, country_stats = processor.process_data(), processor.get_country_comparison()
    
    return render_template(
        "home.html",
        wind_farms=wind_farm_data.to_dict('records'),
        country_stats=country_stats
    )
