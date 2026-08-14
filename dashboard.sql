--content for dashboard
--LIVE
SELECT
    event_id,
    magnitude,
    place,
    event_time,
    latitude,
    longitude,
    depth_km,
    status
FROM earthquake_info
WHERE magnitude >= %s
  AND event_time >= %s
  AND place ILIKE %s;


-----------------------------------------------------------------------------
-- General Analytics
--Total earthquakes
SELECT
    COUNT(*) AS total_earthquakes
FROM earthquake_info;

--largest eartquake
SELECT
    event_id,
    place,
    magnitude,
    event_time
FROM earthquake_info
ORDER BY magnitude DESC
LIMIT 1;

--avg magnitude
SELECT
    AVG(magnitude) AS average_magnitude
FROM earthquake_info;

--most active regions

SELECT
    place,
    COUNT(*) AS earthquake_count
FROM earthquake_info
GROUP BY place
ORDER BY earthquake_count DESC
LIMIT 10;


-- Magnitude distribution

SELECT
    CASE
        WHEN magnitude < 3 THEN 'Minor'
        WHEN magnitude < 5 THEN 'Moderate'
        ELSE 'Strong'
    END AS magnitude_category,
    COUNT(*) AS earthquake_count
FROM earthquake_info
GROUP BY magnitude_category
ORDER BY earthquake_count DESC;

-- Day-over-day earthquake count change

WITH daily_counts AS (
    SELECT
        DATE(event_time) AS earthquake_date,
        COUNT(*) AS earthquake_count
    FROM earthquake_info
    GROUP BY DATE(event_time)
)

SELECT
    earthquake_date,
    earthquake_count,
    LAG(earthquake_count) OVER (
        ORDER BY earthquake_date
    ) AS previous_day_count,
    earthquake_count - LAG(earthquake_count) OVER (
        ORDER BY earthquake_date
    ) AS count_change
FROM daily_counts
ORDER BY earthquake_date;


--Pakistan specific queries
SELECT
    event_id,
    magnitude,
    place,
    event_time,
    latitude,
    longitude,
    depth_km,
    status
FROM earthquake_info
WHERE latitude BETWEEN 24 AND 37
  AND longitude BETWEEN 60 AND 77
ORDER BY event_time DESC;

--recent pak earthquake
SELECT
    event_id,
    place,
    magnitude,
    depth_km,
    event_time
FROM earthquake_info
WHERE latitude BETWEEN 24 AND 37
  AND longitude BETWEEN 60 AND 77
ORDER BY event_time DESC
LIMIT 5;

--total pak earthquake (shows max 30 days and counting because of the data)
SELECT
    COUNT(*) AS pakistan_earthquake_count
FROM earthquake_info
WHERE latitude BETWEEN 24 AND 37
  AND longitude BETWEEN 60 AND 77;

  --largest ewartquake of pak
  SELECT
    event_id,
    place,
    magnitude,
    depth_km,
    event_time
FROM earthquake_info
WHERE latitude BETWEEN 24 AND 37
  AND longitude BETWEEN 60 AND 77
ORDER BY magnitude DESC
LIMIT 1;

--avg magnitude compared ot the world
SELECT
    AVG(
        CASE
            WHEN latitude BETWEEN 24 AND 37
             AND longitude BETWEEN 60 AND 77
            THEN magnitude
        END
    ) AS pakistan_average_magnitude,

    AVG(magnitude) AS global_average_magnitude
FROM earthquake_info;

--pak earthquake into categories
SELECT
    CASE
        WHEN magnitude < 3 THEN 'Minor'
        WHEN magnitude < 5 THEN 'Moderate'
        ELSE 'Strong'
    END AS magnitude_category,
    COUNT(*) AS earthquake_count
FROM earthquake_info
WHERE latitude BETWEEN 24 AND 37
  AND longitude BETWEEN 60 AND 77
GROUP BY magnitude_category
ORDER BY earthquake_count DESC;
