# M5 — Storage Layer (PostGIS)

**Responsibility:** persistence for sightings, watchlist entries, and fired alerts. A plate's
route is not a separate table -- it's built on read from ordered sightings
(`ST_MakeLine(location ORDER BY ts)`), which is exactly what M4's correlation engine and M8's
GIS view will call.

**Input:** writes from M4 (sightings, alerts) and the watchlist admin action.

**Output:** queryable sightings/routes for M4 and M8.

**Standalone test:** `python test_standalone.py` — inserts sample sightings + a watchlist row,
queries the route-building shape M4 will use, asserts it's correct. No other module required.

**Depends on:** nothing. Stand up on Day 1 in parallel with M2.
