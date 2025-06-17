import requests
from datetime import datetime, timezone
import pytz
import pandas as pd

from config import AMBIENT_WEATHER_URL, SENSORS
from logger import logger


def get_sensor_data():
    """Get current readings from all sensors"""
    try:
        response = requests.get(AMBIENT_WEATHER_URL)
        if response.status_code != 200:
            logger.error(f"API Error: {response.status_code}")
            return None

        sensors = response.json()
        rows = []

        for device in sensors:
            mac = device.get('macAddress')
            data = device.get('lastData', {})

            if mac not in SENSORS:
                logger.warning(f"MAC {mac} not in configured sensor list. Skipping.")
                continue

            sensor_info = SENSORS[mac]

            # Get UTC time from API response if available, otherwise use current time
            if 'dateutc' in data:
                utc_time_str = data['dateutc']
                utc_time_str = utc_time_str.replace('Z', '')
                utc_time = datetime.fromisoformat(utc_time_str).replace(tzinfo=timezone.utc)
            else:
                # Fallback to current UTC time if API doesn't provide timestamp
                utc_time = datetime.now(timezone.utc)

            # Convert to Eastern Time (Local Time)
            local_tz = pytz.timezone('America/New_York')
            local_time = utc_time.astimezone(local_tz)

            row = {
                "Location": sensor_info["name"],
                "MacAddress": mac,
                "Latitude": sensor_info["lat"],
                "Longitude": sensor_info["lon"],
                "TemperatureF": data.get("tempf", "N/A"),
                "Humidity": data.get("humidity", "N/A"),
                "FeelsLikeF": data.get("feelsLike", "N/A"),
                "HourlyRain": data.get("hourlyrainin", "N/A"),
                "DailyRain": data.get("dailyrainin", "N/A"),
                "WindSpeedMPH": data.get("windspeedmph", "N/A"),
                "UV": data.get("uv", "N/A"),
                "UTCTime": utc_time.strftime("%Y-%m-%d %H:%M:%S"),
                "LocalTime": local_time.strftime("%Y-%m-%d %H:%M:%S %Z")
            }
            rows.append(row)

        return pd.DataFrame(rows)
    except Exception as e:
        logger.error(f"Error getting sensor data: {str(e)}", exc_info=True)
        return None