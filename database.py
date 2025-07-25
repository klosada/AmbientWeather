import psycopg2
from psycopg2.extras import execute_values
from config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB

TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS ambient_weather_readings (
    id integer generated by default as identity not null,
    macaddress TEXT,
    location TEXT,
    temperaturef REAL,
    humidity REAL,
    feelslikef REAL,
    hourlyrain REAL,
    dailyrain REAL,
    windspeedmph REAL,
    uv REAL,
    utctime TIMESTAMPTZ,
    "localtime" TIMESTAMP,
    latitude REAL,
    longitude REAL
);
"""

def get_connection():
    return psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )

def init_db():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(TABLE_SCHEMA)
            conn.commit()
    except psycopg2.Error as e:
        print("Database initialization failed:", e)
        raise

def save_weather_data(data):
    if data is None or data.empty:
        return
    
    def safe_float(val):
        try:
            return float(val)
        except (ValueError, TypeError):
            return None

    values = [
        (
            row["MacAddress"], row["Location"], safe_float(row["TemperatureF"]), safe_float(row["Humidity"]), safe_float(row["FeelsLikeF"]),
            safe_float(row["HourlyRain"]), safe_float(row["DailyRain"]), safe_float(row["WindSpeedMPH"]), safe_float(row["UV"]),
            row["UTCTime"], row["LocalTime"], row["latitude"], row["longitude"]
        )
        for _, row in data.iterrows()
    ]
    insert_query = """
        INSERT INTO ambient_weather_readings (
            macaddress, location, temperaturef, humidity, feelslikef,
            hourlyrain, dailyrain, windspeedmph, uv, utctime, "localtime", 
            latitude, longitude
        ) VALUES %s
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            execute_values(cur, insert_query, values)
        conn.commit()