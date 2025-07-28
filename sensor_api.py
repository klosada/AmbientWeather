
import requests
import pytz
import pandas as pd
from logger import logger
from datetime import datetime, timezone
from config import AMBIENT_WEATHER_URL, SENSORS

def get_sensor_data():
    try:
        response = requests.get(AMBIENT_WEATHER_URL)
        if response.status_code != 200:
            logger.error(f"API Error: {response.status_code}")
            return None

        sensors = response.json()
        rows = []

        utc_time = datetime.now(timezone.utc)
        local_tz = pytz.timezone('America/New_York')
        local_time = utc_time.astimezone(local_tz).replace(tzinfo=None)

        for device in sensors:
            mac = device.get('macAddress')
            data = device.get('lastData', {})

            if mac not in SENSORS:
                logger.warning(f"MAC {mac} not in configured sensor list. Skipping.")
                continue
            sensor_info = SENSORS[mac]

# add the other data variables here
            row = {
                "Location": sensor_info["name"],
                "MacAddress": mac,
                "latitude": sensor_info["lat"],
                "longitude": sensor_info["lon"],
                "TemperatureF": data.get("tempf", "N/A"),
                "Humidity": data.get("humidity", "N/A"),
                "FeelsLikeF": data.get("feelsLike", "N/A"),
                "HourlyRain": data.get("hourlyrainin", "N/A"),
                "DailyRain": data.get("dailyrainin", "N/A"),
                "MonthlyRain": data.get("monthlyrainin", "N/A"),
                "YearlyRain": data.get("yearlyrainin", "N/A"),
                "WindSpeedMPH": data.get("windspeedmph", "N/A"),
                "WindGustMPH": data.get("windgustmph", "N/A"),
                "MaxDailyGust": data.get("maxdailygust", "N/A"),
                "WindDir": data.get("winddir", "N/A"),
                "BaromRelIn": data.get("baromrelin", "N/A"),
                "BaromAbsIn": data.get("baromabsin", "N/A"),
                "TempInF": data.get("tempinf", "N/A"),
                "HumidityIn": data.get("humidityin", "N/A"),
                "DewPoint": data.get("dewPoint", "N/A"),
                "UV": data.get("uv", "N/A"),
                "UTCTime": utc_time,
                "LocalTime": local_time.replace(tzinfo=None)
            }
            rows.append(row)

        return pd.DataFrame(rows)
    except Exception as e:
        logger.error(f"Error getting sensor data: {str(e)}", exc_info=True)
        return None