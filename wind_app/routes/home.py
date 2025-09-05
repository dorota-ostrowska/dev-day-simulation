from flask import Blueprint, render_template

from wind_app.services.wind_farm_dashboard import WindFarmDashboard
from wind_app.services.wind_farm_service.excel import WindFarmServiceExcel
from wind_app.utils import log

# Create blueprint for home page routes
home = Blueprint("home", __name__)


@home.route("/")
@home.route("/home")
def show_dashboard() -> str:
    """
    Display the wind farm dashboard with real-time data

    Returns:
        Rendered HTML template with wind farm data
    """
    try:
        # Initialize the unified wind farm dashboard
        log("🔧 Initializing wind farm dashboard...")
        wind_farm_service = WindFarmServiceExcel(data_file_path="data/windfarms.xlsx")
        dashboard = WindFarmDashboard(wind_farm_service=wind_farm_service)

        # Get all dashboard data (loading, processing, and formatting)
        dashboard_data = dashboard.get_dashboard_data()

        log("✅ Dashboard ready!")

        # Render template with processed data
        return render_template(
            template_name_or_list="home.html.j2",
            wind_farms=dashboard_data["wind_farms"],
            country_performance=dashboard_data["country_performance"],
            fleet_summary=dashboard_data["fleet_summary"],
            status_metrics=dashboard_data["status_metrics"],
        )

    except Exception as error:
        log(f"❌ Error loading dashboard: {error}")

        # Get empty dashboard data structure for error case
        dashboard = WindFarmDashboard("data/windfarms.xlsx")
        empty_data = dashboard.get_empty_dashboard_data()

        return render_template(
            "home.html.j2",
            wind_farms=empty_data["wind_farms"],
            country_performance=empty_data["country_performance"],
            fleet_summary=empty_data["fleet_summary"],
            status_metrics=empty_data["status_metrics"],
            error_message="Unable to load wind farm data. Please check your configuration and try again.",
        )
