import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv("PG_USER")
POSTGRES_PASSWORD = os.getenv("PG_PASSWORD")
POSTGRES_HOST = os.getenv("PG_HOST")
POSTGRES_PORT = os.getenv("PG_PORT")
POSTGRES_DB = os.getenv("PG_DATABASE")


API_KEY = os.getenv("API_KEY")
APP_KEY = os.getenv("APP_KEY")
AMBIENT_WEATHER_URL = f"https://rt.ambientweather.net/v1/devices?applicationKey={APP_KEY}&apiKey={API_KEY}"

SENSORS = {
    "40:91:51:64:78:95": {
        "name": "Mattsensor",
        "lat": 33.804459,
        "lon": -84.287715
    },
    "F8:B3:B7:83:5A:BD": {
        "name": "Secondsensor",
        "lat": 33.804693,
        "lon": -84.288019
    }
}