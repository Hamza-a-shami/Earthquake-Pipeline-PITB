import json
from kafka import KafkaConsumer

import psycopg2

connection = psycopg2.connect(
    host="localhost",
    database="earthquake_monitor",
    user="postgres",
    password="Hamzaabrar2006",
    port="5432"
)
cursor = connection.cursor()

KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "earthquake-events"

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    value_deserializer=lambda data: json.loads(data.decode("utf-8"))
)


def clean_earthquake(earthquake):
    properties = earthquake["properties"] #because most of the fields are grouped inside properties in the json file
    coordinates = earthquake["geometry"]["coordinates"]
    #have better names for each field
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


print("Waiting for earthquakes...\n")

for message in consumer:
    earthquake = message.value
    cleaned_data = clean_earthquake(earthquake)

    print("Cleaned earthquake:")
    print(cleaned_data)


    cursor.execute(
        "INSERT INTO raw_earthquake_data (data)" \
        "VALUES (%s)",
        (json.dumps(earthquake),)
    )
    # to convert from millisecond we divide the times with 1000s
    #made sure to match by key and no acidental quotes break the code so use %s placeholders
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

    connection.commit()
    print(f"Inserted: {cleaned_data['event_id']} | mag {cleaned_data['magnitude']} | {cleaned_data['place']}")
