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
    ## These two sensors are down and will be moved to rec centers
    # "40:91:51:64:78:95": {
    #     "name": "Decatur1",
    #     "lat": 33.804459,
    #     "lon": -84.287715
    # },
    # "F8:B3:B7:83:5A:BD": {
    #     "name": "Decatur2",
    #     "lat": 33.804693,
    #     "lon": -84.288019
    # },
    "48:E7:29:5F:3C:C9": {
        "name": "Oakhurst Rec Center",
        "lat": 33.760820, 
        "lon": -84.308795
    },
    "C4:D8:D5:3B:83:75": {
        "name": "Sycamore Rec Center",
        "lat": 33.774204,
        "lon": -84.292998
    }  
    # # ARC1 is indoors and will be moved.
    # "F8:B3:B7:83:84:9A": {
    #     "name": "ARC1",
    #     "lat": 33.804693,
    #     "lon": -84.288019
    # }
}