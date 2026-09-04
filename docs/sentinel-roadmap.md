# Sentinel Project Roadmap & Architecture

## Architecture Modules
*   **M1 (Camera Adapters):** Ingests HLS/RTSP streams, handles backoff/reconnection, writes frames to Redis.
*   **M2 (Event Bus):** MQTT broker for high-throughput system events.
*   **M3 (Detection):** YOLOv8/11-based pipeline. Reads from Redis, runs inference, extracts ANPR, publishes to MQTT.
*   **M4 (Correlation):** Matches plates across multiple cameras to build routes.
*   **M5 (Storage):** PostGIS database for spatial data, events, and pgvector embeddings.
*   **M6 (External Mocks):** Stubs for VAHAN/Gov DB enrichment.
*   **M7 (Operator Memory):** LLM-powered pgvector memory for dynamic alert rules.
*   **M8 (Dashboard):** Web UI for visualizing routes and camera health.

## Milestone Success Criteria (The "Done When" Bar)
*   **Day 1:** Standalone tests print PASS (Redis, MQTT, PostGIS).
*   **Day 2:** Adapters write continuous frames to Redis; reconnections flip `ONLINE` -> `RECONNECTING`.
*   **Day 3-4:** M3 extracts correct plate string from a recorded clip.
*   **Day 5:** M4 matches plates from two different clips, producing enriched events.
*   **Day 6:** Watchlist process fires an alert from multi-camera events.
*   **Day 7:** WebSocket test client receives M7 alert; LLM memory pipeline stores/retrieves rules via pgvector.
*   **Day 8:** E2E wiring. Live camera -> live plate -> live route row in DB.
*   **Day 9:** Full live pipeline showing mock VAHAN enrichment on an alert.
*   **Day 10:** Stack boots via `docker-compose`. Demo recorded.
*   **Day 11-12:** HLD, Architecture diagrams, PPT assembled. Final run-throughs.