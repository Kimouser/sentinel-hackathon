"""
M5 standalone test. Passes with zero cameras, models, or other modules running --
just this script talking to the postgis container from docker-compose.yml.

Usage:
    pip install psycopg2-binary
    docker-compose up -d postgis   # schema.sql auto-loads on first start
    python m5_storage/test_standalone.py
"""
import psycopg2
from datetime import datetime, timezone

DSN = "host=localhost port=5432 dbname=sentinel user=sentinel password=sentinel_dev"

SAMPLE_SIGHTINGS = [
    # (cam_id, plate, track_id, confidence, plate_confidence, ts, lon, lat)
    ("cam_04", "GJ05AB1234", "t_231", 0.88, 0.91, datetime.now(timezone.utc), 73.1812, 22.3072),
    ("cam_11", "GJ05AB1234", "t_450", 0.85, 0.88, datetime.now(timezone.utc), 73.2100, 22.3300),
]


def main():
    conn = psycopg2.connect(DSN)
    cur = conn.cursor()

    for cam_id, plate, track_id, conf, plate_conf, ts, lon, lat in SAMPLE_SIGHTINGS:
        cur.execute(
            """
            INSERT INTO sightings (cam_id, plate, track_id, confidence, plate_confidence, ts, location)
            VALUES (%s, %s, %s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography)
            """,
            (cam_id, plate, track_id, conf, plate_conf, ts, lon, lat),
        )

    cur.execute(
        "INSERT INTO watchlist (plate, reason, added_by) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
        ("GJ05AB1234", "demo watchlist entry", "test_standalone.py"),
    )
    conn.commit()

    # Prove the route-building query M4 will actually use
    cur.execute(
        """
        SELECT cam_id, ts, ST_X(location::geometry), ST_Y(location::geometry)
        FROM sightings
        WHERE plate = %s
        ORDER BY ts
        """,
        ("GJ05AB1234",),
    )
    rows = cur.fetchall()
    assert len(rows) == 2, f"expected 2 sightings, got {len(rows)}"

    cur.execute("SELECT plate FROM watchlist WHERE plate = %s", ("GJ05AB1234",))
    assert cur.fetchone() is not None, "watchlist row not found"

    cur.close()
    conn.close()
    print(f"PASS: M5 storage insert/query works. Route for GJ05AB1234: {rows}")


if __name__ == "__main__":
    main()
