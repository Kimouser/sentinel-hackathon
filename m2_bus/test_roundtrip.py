"""
M2 standalone test. Passes with zero cameras, models, or other modules running --
just this script talking to the mosquitto container from docker-compose.yml.

Usage:
    pip install paho-mqtt jsonschema
    docker-compose up -d mosquitto
    python m2_bus/test_roundtrip.py
"""
import json
import time
import threading
from pathlib import Path

import paho.mqtt.client as mqtt
from jsonschema import validate

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "sentinel/enriched/cam_04"

SCHEMA = json.loads((Path(__file__).parent / "schema.json").read_text())

SAMPLE_EVENT = {
    "cam_id": "cam_04",
    "timestamp": "2026-08-28T10:12:33Z",
    "vendor_profile": "hikvision_v1",
    "detections": [
        {
            "type": "vehicle",
            "bbox": [100, 200, 340, 420],
            "plate": "GJ05AB1234",
            "plate_confidence": 0.91,
            "track_id": "t_231",
            "confidence": 0.88,
        }
    ],
    "gps": {"lat": 22.3072, "lon": 73.1812},
}

received = threading.Event()
received_payload = {}


def on_message(client, userdata, msg):
    received_payload["data"] = json.loads(msg.payload.decode())
    received.set()


def main():
    sub = mqtt.Client(client_id="sentinel_m2_test_sub", callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    sub.on_message = on_message
    sub.connect(BROKER_HOST, BROKER_PORT)
    sub.subscribe(TOPIC)
    sub.loop_start()

    time.sleep(0.5)  # let the subscription register before we publish

    pub = mqtt.Client(client_id="sentinel_m2_test_pub", callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    pub.connect(BROKER_HOST, BROKER_PORT)
    pub.publish(TOPIC, json.dumps(SAMPLE_EVENT))
    pub.disconnect()

    ok = received.wait(timeout=5)
    sub.loop_stop()
    sub.disconnect()

    if not ok:
        raise SystemExit("FAIL: no message received within 5s -- is mosquitto running? (docker-compose up -d mosquitto)")

    validate(instance=received_payload["data"], schema=SCHEMA)
    assert received_payload["data"] == SAMPLE_EVENT, "round-tripped payload does not match what was sent"

    print("PASS: M2 event bus round-trips the frozen schema correctly.")


if __name__ == "__main__":
    main()
