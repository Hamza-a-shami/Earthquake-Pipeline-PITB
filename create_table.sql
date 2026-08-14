CREATE TABLE raw_earthquake_data(
    data JSONB,
    ingested_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE Earthquake_info(
    event_id VARCHAR(50) PRIMARY KEY,
    magnitude NUMERIC(4,2),
    place TEXT,
    event_time TIMESTAMPTZ, -- to keep the timezone
    updated_time TIMESTAMPTZ,
    longitude DOUBLE PRECISION,
    latitude DOUBLE PRECISION,
    depth_km DOUBLE PRECISION,
    significance INTEGER,
    tsunami BOOLEAN,
    status VARCHAR(30),
    magnitude_type VARCHAR(20),
    event_type VARCHAR(50),
    felt INTEGER,
    cdi DOUBLE PRECISION,
    mmi DOUBLE PRECISION,
    alert VARCHAR(20),
    station_count INTEGER,
    minimum_distance DOUBLE PRECISION,
    rms DOUBLE PRECISION,
    gap DOUBLE PRECISION,
    url TEXT,
    detail_url TEXT,
    ingested_at TIMESTAMPTZ DEFAULT NOW()
);

--we create a table that helps us track if pipeline is working properly

CREATE TABLE pipeline_run_check (
    run_id BIGSERIAL PRIMARY KEY,
    records_received INTEGER,
    records_inserted INTEGER,
    records_updated INTEGER,
    status BOOLEAN,
    error_type TEXT,
    recorded_at TIMESTAMPTZ DEFAULT NOW()
);


CREATE INDEX index_earthquake_time ON earthquake_info(event_time);
CREATE INDEX index_earthquake_mag ON earthquake_info(magnitude);
CREATE INDEX index_earthquake_alert ON earthquake_info(alert);
