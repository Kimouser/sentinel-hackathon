# Sentinel — Day 1 Foundation

This is the very first slice of the build: M2 (event bus) and M5 (storage), both standalone,
both with zero dependency on cameras, models, or each other. Everything else in the roadmap
gets built and tested against these two contracts.

## Quickstart

```bash
# 1. Start both services
docker-compose up -d

# 2. Install test dependencies
pip install paho-mqtt jsonschema psycopg2-binary

# 3. Prove M2 (event bus) works standalone
python m2_bus/test_roundtrip.py
# expect: "PASS: M2 event bus round-trips the frozen schema correctly."

# 4. Prove M5 (storage) works standalone
python m5_storage/test_standalone.py
# expect: "PASS: M5 storage insert/query works. Route for GJ05AB1234: [...]"
```

If both print PASS, Day 1 is done. Next: M1 (camera adapters) against your real cameras,
using the HLS profile confirmed from `feedtest_pro.py` — see the main roadmap doc for the
full module list and day-by-day schedule.

## Structure

```
sentinel/
├── docker-compose.yml     # mosquitto + postgis
├── m2_bus/                 # event bus: schema, config, standalone test
└── m5_storage/              # storage: schema, standalone test
```

Each module folder is self-contained: its own README stating input/output contract, its own
standalone test, nothing that requires another module to be running. That's deliberate --
see §1 of the main roadmap doc ("Design rule for this build").
