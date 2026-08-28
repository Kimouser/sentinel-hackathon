# M2 — Event Bus (Middleware)

**Responsibility:** carries small enriched-event JSON between M3 and M4, and status/heartbeat
events from M1 to M8. Metadata and control-plane only — raw video never crosses this bus
(see M1/M3 for the Redis latest-frame handoff).

**Input:** any publisher on `sentinel/*` (e.g. `sentinel/enriched/{cam_id}`, `sentinel/alerts`,
`sentinel/health/{cam_id}`).

**Output:** delivery to any subscriber on that topic, payload matching `schema.json`.

**Standalone test:** `python test_roundtrip.py` — dummy publisher/subscriber round-tripping
the frozen schema. No cameras, no models, no other module required.

**Depends on:** nothing.

**Status:** schema frozen once `test_roundtrip.py` passes. Every downstream module is written
against this JSON shape, not against M1/M3's actual implementation.
