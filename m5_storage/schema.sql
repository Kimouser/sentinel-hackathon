-- M5 storage schema. Auto-loaded by the postgis container on first start
-- (see docker-compose.yml init mount).

CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS sightings (
    id              BIGSERIAL PRIMARY KEY,
    cam_id          TEXT NOT NULL,
    plate           TEXT,
    track_id        TEXT,
    confidence      REAL,
    plate_confidence REAL,
    ts              TIMESTAMPTZ NOT NULL,
    location        GEOGRAPHY(POINT, 4326) NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_sightings_plate_ts ON sightings (plate, ts);
CREATE INDEX IF NOT EXISTS idx_sightings_location ON sightings USING GIST (location);

CREATE TABLE IF NOT EXISTS watchlist (
    plate       TEXT PRIMARY KEY,
    reason      TEXT NOT NULL,
    added_by    TEXT,
    added_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS alerts (
    id          BIGSERIAL PRIMARY KEY,
    plate       TEXT NOT NULL REFERENCES watchlist(plate),
    sighting_id BIGINT NOT NULL REFERENCES sightings(id),
    fired_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    mock_enrichment JSONB
);

-- A plate's route is just its ordered sightings -- no separate table needed,
-- M4 builds the polyline on read with ST_MakeLine(location ORDER BY ts).
