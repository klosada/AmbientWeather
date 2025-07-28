from dotenv import load_dotenv
import os
from arcgis.gis import GIS
from arcgis.geometry import Geometry
from config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB
import psycopg2
import pandas as pd
import pytz

# ArcGIS Credentials
load_dotenv()  
username = os.environ["ARCGIS_USERNAME"]
password = os.environ["ARCGIS_PASSWORD"]
gis = GIS(url="https://garc.maps.arcgis.com/home", username=username, password=password)

from arcgis.features import FeatureLayer


# Fetch recent data from PostgreSQL
def fetch_weather_data():
    conn = psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )
    query = """
        SELECT *
        FROM ambient_weather_readings
        WHERE utctime > NOW() - INTERVAL '30 minutes'
        ORDER BY utctime;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    df['utctime'] = pd.to_datetime(df['utctime'], utc=True)
    df['localtime'] = pd.to_datetime(df['localtime'])

    return df


# Update hosted feature layer
def publish_to_arcgis(df: pd.DataFrame, item_id: str):
    if df.empty:
        return
    
    df = df.copy()
    df = df.reset_index(drop=True)
    df['record_id'] = df.index + 1

    df['geometry'] = df.apply(lambda row: Geometry({
        "x": float(row["longitude"]),
        "y": float(row["latitude"]),
        "spatialReference": {"wkid": 4326}
    }), axis=1)

    df = df.dropna(subset=['geometry'])
    df.spatial.set_geometry('geometry', inplace=True)


    item = gis.content.get(item_id)
    layer = item.layers[0]
    layer.manager.truncate()
    print("Adding new features...")
    fs = df.spatial.to_featureset()
    layer.edit_features(adds=fs)
    print(f"Updated layer: {item.title}")
   
# Main function
if __name__ == "__main__":
    latest_df = fetch_weather_data()
    if latest_df.empty:
        print("No recent data found.")
    else:
        publish_to_arcgis(latest_df, item_id="6ea917fd50bb413bb25cbc33d34c7119")
