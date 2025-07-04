# The Ørsted Trial: A Day in the Life of a Software Developer 🤓
This repo contains materials for a 1-day Ørsted workshop, giving IT students hands-on experience in agile, team collaboration, bug fixing, and handling changing requirements. Work on real-world scenarios to explore the dynamic nature of software development.

## Technologies 🛠
- Python 🐍
- Flask 🌶️
- Pandas 🐼
- Openpyxl 📈
- Requests 🤌

## Prerequisites 📋
Before you begin, ensure you have the following installed:
- [Visual Studio Code](https://code.visualstudio.com/download)
- [Python 3.13.2](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)

## Getting started 🎬
1. Create a virtual environment.
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# on Windows:
venv\Scripts\activate.bat
# on macOS and Linux:
source venv/bin/activate
```

2. Install necessary requirements.
```bash
pip install -r requirements.txt
```

3. Get OpenWeather API key.
To access weather data, you need a free API key from OpenWeather:

- Go to [https://openweathermap.org/](https://openweathermap.org/) and click **Sign In** to create an account.
- After logging in, navigate to the [API keys section](https://home.openweathermap.org/api_keys).
![alt text](docs/images/my_api_keys.png)
- Provide a name of your key (e.g., `my-weather-key`), click **Create key**. 
![alt text](docs/images/create_key.png)
- Copy your unique API key (the long string).
![alt text](docs/images/copy_key.png)
- Store this key in your configuration file `private_config.py` in the `src` folder.
![alt text](docs/images/store_key.png)
> ⚠️ **Security Warning**: Keep your API key private! Never commit it to version control or share it publicly. The `private_config.py` file is already in `.gitignore` to prevent accidental commits.
