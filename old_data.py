import json
import requests
import psycopg2

connection = psycopg2.connect(
    host="localhost",
    database="earthquake_monitor",
    user="postgres",
    password="Hamzaabrar2006",
    port="5432"
)
cursor = connection.cursor()

url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"

print("Fetching last 30 days of earthquake data...")
response = requests.get(url, timeout=60)
response.raise_for_status()
earthquakes = response.json()["features"]
print(f"Received {len(earthquakes)} earthquakes")

def clean_earthquake(earthquake):
    properties = earthquake["properties"]
    coordinates = earthquake["geometry"]["coordinates"]
    cleaned_data = {
        "event_id": earthquake["id"],
        "magnitude": properties.get("mag"),
        "place": properties.get("place"),
        "event_time": properties.get("time"),
        "updated_time": properties.get("updated"),
        "longitude": coordinates[0],
        "latitude": coordinates[1],
        "depth_km": coordinates[2],
        "significance": properties.get("sig"),
        "tsunami": bool(properties.get("tsunami")),
        "status": properties.get("status"),
        "magnitude_type": properties.get("magType"),
        "event_type": properties.get("type"),
        "felt": properties.get("felt"),
        "cdi": properties.get("cdi"),
        "mmi": properties.get("mmi"),
        "alert": properties.get("alert"),
        "station_count": properties.get("nst"),
        "minimum_distance": properties.get("dmin"),
        "rms": properties.get("rms"),
        "gap": properties.get("gap"),
        "url": properties.get("url"),
        "detail_url": properties.get("detail")
    }
    return cleaned_data

inserted = 0
skipped = 0

for earthquake in earthquakes:
    cleaned_data = clean_earthquake(earthquake)

    cursor.execute(
        "INSERT INTO raw_earthquake_data (data) VALUES (%s)",
        (json.dumps(earthquake),)
    )

    try:
        cursor.execute("""
            INSERT INTO earthquake_info (
                event_id, magnitude, place, event_time, updated_time,
                longitude, latitude, depth_km, significance, tsunami,
                status, magnitude_type, event_type, felt, cdi, mmi,
                alert, station_count, minimum_distance, rms, gap, url, detail_url
            ) VALUES (
                %(event_id)s, %(magnitude)s, %(place)s,
                TO_TIMESTAMP(%(event_time)s / 1000.0),
                TO_TIMESTAMP(%(updated_time)s / 1000.0),
                %(longitude)s, %(latitude)s, %(depth_km)s,
                %(significance)s, %(tsunami)s, %(status)s,
                %(magnitude_type)s, %(event_type)s, %(felt)s,
                %(cdi)s, %(mmi)s, %(alert)s, %(station_count)s,
                %(minimum_distance)s, %(rms)s, %(gap)s,
                %(url)s, %(detail_url)s
            )
            ON CONFLICT (event_id) DO NOTHING
        """, cleaned_data)
        inserted += 1
    except Exception as error:
        print(f"Skipped: {cleaned_data['event_id']} | Error: {error}")
        skipped += 1
        connection.rollback()
        continue

    connection.commit()

print(f"Done. Inserted: {inserted}, Skipped: {skipped}")
cursor.close()
connection.close()