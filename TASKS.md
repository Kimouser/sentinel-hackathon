# Sentinel Execution Ledger

- [x] **Day 1: Core Infrastructure** - Validated Redis, MQTT, PostGIS. Repo initialized.
- [ ] **Day 2: Ingestion Layer (M1)** - Wire `m1_adapters/run_adapters.py` + `monitor.py`. 
  - *Gate*: Verify Redis keys update continuously and status flips ONLINE/RECONNECTING.
- [ ] **Day 3-4: Detection Pipeline (M3)** - Implement `m3_detection/detector.py` using `models/yolov8n.pt` or `yolo11n.pt` on `assets/sample1.mp4`.
  - *Gate*: Script outputs valid bounding boxes and plate strings at 1-2fps decimation.
- [ ] **Day 5: Correlation Engine (M4/M5)** - Implement tracking ID persistence. 
  - *Gate*: System matches the vehicle `JK 16C 0038` across `sample1.mp4` and `sample2.mp4`.
- [ ] **Day 6: Watchlist & Alerts (M6)** - Implement `m4_correlation/watchlist.py`.
  - *Gate*: Ingest MQTT events, evaluate, emit alert payload to MQTT `alerts/matched`.
- [ ] **Day 7: Operator Memory (M7)** - Scaffold `m7_operator/memory_rules.py` using PostGIS `pgvector`.
  - *Gate*: Successfully store and retrieve a natural-language operational filter.
- [ ] **Day 8-10: End-to-End Integration & UI** - Wire M1->M3->M4->M7->M8.
  - *Gate*: `docker-compose up` brings up the whole stack; dashboard renders mock route.