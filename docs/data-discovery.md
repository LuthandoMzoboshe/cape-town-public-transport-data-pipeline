# Cape Town Public Transport Data Discovery

## 1. Project Scope

This project investigates publicly available Cape Town public transport data across three transport modes:

- Taxi
- MyCiTi bus
- Rail

The data is sourced from the City of Cape Town's GIS services and will be investigated before designing the database schema and building the data pipeline.

## 2. Data Sources

The project uses public GIS services provided by the City of Cape Town.

### City of Cape Town Open Data Services

Base service:

`https://citymaps.capetown.gov.za/agsext/rest/services/Theme_Based/`

The project currently uses two City GIS services:

- `ODP_SPLIT_6` — used for MyCiTi and taxi datasets
- `Transport` — used for railway datasets

The services expose ArcGIS REST endpoints that allow the project to query structured feature data and geographic geometry.

### Datasets Identified

| Transport Mode | Dataset | Service | Layer |
|---|---|---|---:|
| Taxi | Taxi Routes | ODP_SPLIT_6 | 11 |
| MyCiTi | MyCiTi Bus Routes | ODP_SPLIT_6 | 9 |
| MyCiTi | MyCiTi Bus Stops | ODP_SPLIT_6 | 10 |
| Rail | Railway Stations | Transport | 31 |
| Rail | Railway Lines | Transport | 30 |

## 3. Discovered Source Schemas

The initial API profiling was performed using attribute-only queries (`returnGeometry=false`) to inspect the tabular structure before processing geographic geometry.

### 3.1 Taxi Routes

**Geometry type:** Polyline

| Source Field | Meaning | Type |
|---|---|---|
| `OBJECTID` | Source object identifier | OID |
| `ORGN` | Origin | String |
| `DSTN` | Destination | String |
| `Shape__Length` | Source-provided route geometry length | Double |

Example records included routes such as:

- Bellville → Durbanville
- Bellville → Nyanga
- Bellville → Khayelitsha
- Gugulethu → Sea Point
- Langa → Cape Town

### 3.2 MyCiTi Bus Routes

**Geometry type:** Polyline

| Source Field | Meaning | Type |
|---|---|---|
| `OBJECTID` | Source object identifier | OID |
| `RT_NAME` | Route name | String |
| `RT_TYPE` | Route type | String |
| `RT_STS` | Route status | String |
| `RT_NMBR` | Route number | String |
| `Shape__Length` | Source-provided route geometry length | Double |

The initial sample contained active feeder routes such as route 101, 102, 103, 104 and 105.

### 3.3 MyCiTi Bus Stops

**Geometry type:** Point

| Source Field | Meaning | Type |
|---|---|---|
| `OBJECTID` | Source object identifier | OID |
| `STOP_NAME` | Stop name | String |
| `STOP_TYPE` | Stop type | String |
| `STOP_STS` | Stop status | String |
| `STOP_DSCR` | Stop description | String |

The sample contained stops such as La Paloma, Losperds, Pella Central, Bridgeway and Loxton East.

### 3.4 Railway Stations

**Geometry type:** Point

| Source Field | Meaning | Type |
|---|---|---|
| `OBJECTID` | Source object identifier | OID |
| `NAME` | Station name | String |

The sample contained stations including Netreg, Mandalay, Nolungile, Khayelitsha, Philippi and Mitchell's Plain.

### 3.5 Railway Lines

**Geometry type:** Polyline

| Source Field | Meaning | Type |
|---|---|---|
| `OBJECTID` | Source object identifier | OID |
| `SHAPE.STLength()` | Source-provided line geometry length | Double |
| `NAME` | Line name | String |
| `USG` | Usage | String |
| `TYPE` | Line type | String |



## 4. Initial Data Quality Observations

The initial samples revealed several characteristics that need to be investigated before the data is loaded into the final database.

### 4.1 API Transfer Limits

The API responses returned:

`"exceededTransferLimit": true`

when querying the datasets, indicating that the response did not contain all matching records.

The City of Cape Town service metadata reports a maximum record count of 2,000.

The ingestion pipeline will therefore need to account for API record limits and retrieve the complete dataset reliably rather than assuming a single request contains all records.

### 4.2 Repeated MyCiTi Route Records

The MyCiTi Bus Routes sample contained multiple records with the same route number and route name.

For example, route `101` appeared more than once with different `OBJECTID` values and different geometry lengths.

These records should not immediately be treated as duplicates because they may represent different route geometries or segments.

Further investigation is required before deduplication.

### 4.3 Missing Railway Line Names

The Railway Lines sample contained records where `NAME` was empty.

For example, some records had a populated `USG` and `TYPE` but no line name.

The final database should therefore not assume that the source `NAME` field is always populated.

### 4.4 Different Geometry Types

The datasets contain both point and polyline geometries:

- Taxi Routes — Polyline
- MyCiTi Bus Routes — Polyline
- MyCiTi Bus Stops — Point
- Railway Stations — Point
- Railway Lines — Polyline

The pipeline will need to handle these geometry types appropriately.

### 4.5 Source-Provided Length Values

The route and railway datasets provide geometry length fields such as `Shape__Length` and `SHAPE.STLength()`.

The units and interpretation of these values must be verified before converting them into a business-friendly measurement such as kilometres.

The pipeline should not assume the unit without validation.

### 4.6 Source Identifiers

Each dataset provides an `OBJECTID` generated by the source system.

These identifiers will be investigated to determine whether they are suitable as stable source identifiers or whether the final database should generate its own primary keys.