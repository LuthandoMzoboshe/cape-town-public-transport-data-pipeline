# cape-town-public-transport-data-pipeline

WTC Verification Code: WTC-F2WVRL37


## Gold Layer

The Gold layer provides standardized analytical datasets across the transport systems.

### Transport Routes

`data/gold/transport_routes/transport_routes.parquet`

The `transport_routes` table standardizes route and line records from Golden Arrow, MyCiTi, taxi routes, and Metrorail lines.

Common fields include:

- `transport_mode`
- `source_system`
- `source_route_id`
- `route_name`
- `origin`
- `destination`
- `operator`
- `route_length_m`
- `geometry`

Source-specific fields that are not available for a transport system are retained as `NULL` rather than inferred.

### Transport Stops

`data/gold/transport_stops/transport_stops.parquet`

The `transport_stops` table standardizes physical transport locations across Golden Arrow, MyCiTi, and Metrorail.

The `location_type` field distinguishes between:

- `stop` — Golden Arrow and MyCiTi
- `station` — Metrorail

The common `source_location_id` field preserves the original source identifier while allowing stops and stations to coexist in the same analytical table.

Taxi stops are not included because the source data does not contain a separate taxi stop dataset.

### Transport Summary

`data/gold/transport_summary/transport_summary.parquet`

The summary table contains one record per transport source system and provides:

- route/line count
- location count
- named location count
- total route length
- average route length
- geometry count

This table is intended for high-level analysis and dashboarding.

### Data Quality

The Gold layer includes automated validation through:

`src/validate_gold.py`

Validation checks include:

- required files and columns
- non-empty tables
- valid transport modes
- valid source systems
- duplicate rows
- required-field NULLs
- route length values
- geometry completeness

Source-level quality issues are preserved rather than fabricated or silently removed.

For example, one Golden Arrow route has a source-provided route length of `0` and an empty geometry. The validator reports these as warnings while retaining the original record.
