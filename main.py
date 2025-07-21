from logger import logger
from sensor_api import get_sensor_data
from database import save_weather_data, init_db
from arcgis_connection import publish_to_arcgis

def main():
    logger.info("Initializing database...")
    init_db()
    logger.info("Fetching sensor data...")
    readings = get_sensor_data()

    if not readings.empty:
        logger.info(f"Fetched {len(readings)} readings. Saving to database...")
        save_weather_data(readings)
        publish_to_arcgis(readings, item_id="6ea917fd50bb413bb25cbc33d34c7119")
        logger.info("Data saved successfully.")
    else:
        logger.warning("No data fetched.")

if __name__ == "__main__":
    main()
