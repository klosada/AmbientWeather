# AmbientWeather ETL Pipeline

This repository provides a complete ETL (Extract-Transform-Load) pipeline to fetch weather data from AmbientWeather sensors, store it in a PostgreSQL database, and publish it to an ArcGIS Online hosted feature layer.

## Overview

The project consists of the following steps:

1. Fetch live weather data from multiple IoT sensors using the AmbientWeather API.
2. Normalize and timestamp the data.
3. Store it in a PostgreSQL database.
4. Push the most recent records to ArcGIS Online for geospatial visualization.

The  data collection and GIS integration are automated every 30 mins via GitHub Actions. 

## File Structure

### `main.py`
This is the entry point. It:
- Initializes the database schema (if not already created).
- Fetches live sensor data via the API.
- Saves the data to PostgreSQL.
- Publishes the last 30 minutes of readings to ArcGIS.

### `sensor_api.py`
Responsible for:
- Querying the AmbientWeather REST API.
- Mapping MAC addresses to friendly sensor names and coordinates from `config.py`.
- Returning a timestamped, cleaned `pandas.DataFrame` of sensor readings.

### `database.py`
Handles database operations:
- Defines the PostgreSQL table schema (`ambient_weather_readings`).
- Initializes the table if needed.
- Converts and bulk inserts incoming weather records using `execute_values()`.

### `arcgis_connection.py`
Publishes recent weather readings to ArcGIS Online:
- Authenticates using `.env` or GitHub Actions secrets.
- Fetches readings from the database from the last 30 minutes.
- Converts them to ArcGIS features with geometry.
- Clears and uploads new features to a specific hosted layer via `item_id`.

### `config.py`
Loads environment variables and sensor metadata:
- Ambient Weather API keys.
- PostgreSQL connection details from Supabase.
- Predefined sensor locations (lat/lon) mapped to their MAC addresses.

### `fetch_and_insert.yaml`
GitHub Actions workflow for scheduling automatic runs, using secrets defined in the repo to inject credentials for continous data integration.

### `requirements.txt`
Python dependencies needed for GitHub Actions:
- `pandas`, `requests`, `psycopg2-binary`, `arcgis`, `python-dotenv`.

---

## Environment Variables

Make sure to define these in `.env` locally or as GitHub Actions secrets:

```env
### Supabase
PG_USER=your_db_username
PG_PASSWORD=your_password
PG_HOST=your_db_host
PG_PORT=6543
PG_DATABASE=your_db_type

### Ambient Weather
API_KEY=your_ambientweather_api_key
APP_KEY=your_ambientweather_app_key

### ArcGIS
ARCGIS_USERNAME=your_arcgis_username
ARCGIS_PASSWORD=your_arcgis_password

## New Supabase account was created under researchanalytics229@gmail.com
