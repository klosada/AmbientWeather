import psycopg2
from config import DATABASE_URL
from psycopg2.extras import execute_values

TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS weather_readings (
    id SERIAL PRIMARY KEY,
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
    "localtime" TIMESTAMPTZ
);
"""

def init_db():
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            conn.set_client_encoding('UTF8') 
            with conn.cursor() as cur:
                cur.execute(TABLE_SCHEMA)
                conn.commit() 
    except psycopg2.Error as e:
        print("Database initialization failed:", e)
        raise

def save_weather_data(data):
    if data is None or data.empty:
        return
    
    # Convert DataFrame to list of tuples for insertion
    values = [
        (
            row["MacAddress"], row["Location"], row["TemperatureF"], row["Humidity"], row["FeelsLikeF"],
            row["HourlyRain"], row["DailyRain"], row["WindSpeedMPH"], row["UV"],
            row["UTCTime"], row["LocalTime"]
        )
        for _, row in data.iterrows()
    ]

    insert_query = """
        INSERT INTO weather_readings (
            macaddress, location, temperaturef, humidity, feelslikef,
            hourlyrain, dailyrain, windspeedmph, uv, utctime, "localtime"
        ) VALUES %s
    """

    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            execute_values(cur, insert_query, values)
        conn.commit()
