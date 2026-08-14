\# Earthquake Monitoring Dashboard



\## Overview



This project is a real-time earthquake monitoring system built using Python, Apache Kafka, PostgreSQL, and Tableau.



The system collects earthquake data from the USGS Earthquake API, streams the data through Kafka, stores it in PostgreSQL, and visualizes it using interactive Tableau dashboards. Historical earthquake data for the previous 30 days is also loaded into the database to provide context alongside live updates.





\## Features



\- Real-time earthquake data ingestion

\- Historical backfill for the previous 30 days

\- Kafka-based streaming pipeline

\- PostgreSQL data storage

\- Interactive Tableau dashboards

\- Pakistan-specific earthquake monitoring

\- SQL-based analytics



\---



\## Technology Stack



\- Python

\- Apache Kafka

\- PostgreSQL

\- Tableau Desktop

\- Docker

\- SQL



\---



\## Project Structure



```

earthquake-pipeline/

│

├── producer.py              # Fetches earthquake data from the USGS API

├── consumer.py              # Consumes Kafka messages and stores data

├── backfill.py              # Loads historical earthquake data

├── database.sql             # Database schema

├── dashboard\_queries.sql    # SQL queries used by Tableau

├── docker-compose.yml       # Kafka and Zookeeper containers

└── README.md

```





\## Database



The project stores earthquake information in PostgreSQL.



\### Main Tables



\### Earthquake\_info



Stores cleaned earthquake information.



Example fields:



\- event\_id

\- magnitude

\- place

\- event\_time

\- updated\_time

\- latitude

\- longitude

\- depth\_km

\- significance

\- tsunami

\- status

\- magnitude\_type

\- event\_type

\- felt

\- cdi

\- mmi

\- alert

\- station\_count

\- minimum\_distance

\- rms

\- gap

\- url

\- detail\_url

\- ingested\_at



\### raw\_earthquake\_data



Stores the original JSON payload received from the API.



\---



\## Data Pipeline



\### Historical Data



The `old\_data.py` script downloads earthquake data from the previous 30 days and inserts it into PostgreSQL.



\### Live Data



The producer file continuously requests new earthquake events from the USGS API and publishes them to a Kafka topic.



The consumer reads each event, cleans the data, and inserts it into the PostgreSQL database.



Duplicate earthquake events are ignored using PostgreSQL's `ON CONFLICT` constraint.



\---



\## Tableau Dashboards



\### 1. Live Map



Displays all earthquake events on an interactive world map.



Features:



\- Magnitude filter

\- Date filter

\- Bubble size based on magnitude

\- Color coded earthquake categories

\- Interactive tooltips



\---



\### 2. Analytics Dashboard



Provides summary statistics and trends.



Visualizations include:



\- Total earthquakes

\- Average magnitude

\- Earthquakes per day

\- Magnitude distribution

\- Top active regions



\---



\### 3. Pakistan Dashboard



Focuses on earthquake activity within Pakistan.



Includes:



\- Pakistan earthquake map

\- Recent earthquake events

\- Pakistan vs global average magnitude



\---



\## SQL Analytics



The project includes SQL queries for:



\- Total earthquake count

\- Largest earthquake

\- Average magnitude

\- Top active regions

\- Magnitude distribution

\- Daily earthquake trend

\- Pakistan earthquake analysis







