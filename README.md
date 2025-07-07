<div align="center">

# 🤓 The Ørsted Trial: A Day in the Life of a Software Developer ⚡️

This repo contains materials for a 1-day Ørsted workshop, giving IT students hands-on experience in:

✅ agile teamwork

🐛 real-world debugging

🔄 handling changing requirements

🚢 simulating dynamic software dev environments

</div>

# 🌊 Wind Farm Dashboard

A beautiful, real-time dashboard for monitoring offshore wind farms built with Python and Flask. Perfect for learning web development, APIs, and data visualization!

## 🛠 Technologies
- 🐍 Python | Core language
- 🌶️ Flask | Lightweight web framework
- 🐼 Pandas | Data manipulation
- 📈 Openpyxl | Excel handling
- 🤌 Requests | API communication
- 🎀 HTML | Frontend styling
- 🥷 Jinja2 | Template rendering

## ✨ Features

- 🔄 Real-time wind speed data from OpenWeatherMap API
- 📊 Power generation estimates using turbine power curves
- 🗺️ Multi-country wind farm monitoring
- 📈 Performance analytics and visualizations
- 🎨 Beautiful, responsive dashboard interface

## 🚀 Quick start

### Prerequisites
Before you begin, ensure you have the following installed:
- [Visual Studio Code](https://code.visualstudio.com/download)
- [Python 3.13.2](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

### 1. Clone and setup ⚙️

```bash
# Clone the repository
git clone https://github.com/dorota-ostrowska/dev-day-simulation
cd dev-day-simulation

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Get your API key 🔑
To access weather data, you need a free API key from OpenWeather:

1. Go to [https://openweathermap.org/](https://openweathermap.org/) and create a free account.
2. After logging in, navigate to the [API keys section](https://home.openweathermap.org/api_keys).
3. Provide a name of your key (e.g., `my-weather-key`), click **Create key**. 
4. Copy your unique API key (the long string).
5. Store this key in your configuration file `private_config.py` in the `src` folder.

> ⚠️ **Security Warning**: Keep your API key private! Never commit it to version control or share it publicly. The `private_config.py` file is already in `.gitignore` to prevent accidental commits.

### 3. Run the application 🏃

```bash
# Start the development server
python main.py
```

Visit [http://localhost:5000](http://localhost:5000) to see your wind farm dashboard! 🎉

## 📁 Project Structure

```
wind-farm-dashboard/
├── main.py                         # Application entry point
├── requirements.txt                # Python dependencies
├── data/
│   └── windfarms.xlsx              # Wind farm data
├── src/
│   ├── __init__.py                 # Flask app factory
│   ├── private_config.py           # Your API key (not in git)
│   ├── routes/
│   │   └── home.py                 # Dashboard route handler
│   ├── services/
│   │   ├── wind_farm_dashboard.py  # Main dashboard logic
│   │   ├── excel_service.py        # Excel data loading
│   │   └── weather_service.py      # Weather API integration
│   └── templates/
│       ├── base.html               # HTML template base
│       └── home.html               # Dashboard template
└──  tests/                         # Test files
```

## 🧠 How it works

### Data flow ⚙️
1. **📂 Load Data**: Read wind farm information from Excel file
2. **🌬 Fetch Weather**: Get current wind speeds for each farm location
3. **⚡ Calculate Power**: Use wind turbine power curves to estimate output
4. **🖼 Format Display**: Prepare data for beautiful dashboard presentation
5. **🖥 Render Dashboard**: Show real-time wind farm performance

### Core components 🧩

- **WindFarmDashboard**: Main orchestration logic
- **WeatherService**: Talks to OpenWeatherMap
- **ExcelService**: Reads .xlsx data
- **Templates**: Clean UI with Jinja2 and HTML

## 📄 License

This project is part of `The Ørsted Trial: A Day in the Life of a Software Developer` workshop materials. It’s intended for educational, non-commercial use. 🌱

---

**Happy coding! 🚀 Build something amazing with renewable energy data!**

<div align="center">

**Made with 💚 for renewable energy**

</div>
