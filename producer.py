import json
import time
import requests
from kafka import KafkaProducer

USGS_API_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.geojson"
KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "earthquake-events"
POLL_INTERVAL_SECONDS = 60

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

sent_ids = set()

def fetch_earthquakes():
    response = requests.get(USGS_API_URL, timeout=30)
    response.raise_for_status()
    return response.json().get("features", [])

while True:
    try:
        earthquakes = fetch_earthquakes()
        new_count = 0
        for earthquake in earthquakes:
            eq_id = earthquake.get("id")
            if eq_id not in sent_ids:
                producer.send(KAFKA_TOPIC, earthquake)
                sent_ids.add(eq_id)
                new_count += 1
        
        producer.flush()
        print(f"Fetched {len(earthquakes)} total, published {new_count} new events")
    except Exception as error:
        print(f"Error: {error}")
    
    time.sleep(POLL_INTERVAL_SECONDS)