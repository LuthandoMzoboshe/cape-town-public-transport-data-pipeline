# Cape Town Public Transport
# Raw Data Profiling Report

Generated automatically from `data/raw/`.

## Dataset Overview

| Dataset | Records | Geometry | Fields |
|---|---:|---|---:|
| `golden_arrow_routes` | 1,991 | LineString: 1,933, MultiLineString: 58 | 13 |
| `golden_arrow_stops` | 2,000 | Point: 2,000 | 9 |
| `metrorail_lines` | 10 | LineString: 10 | 6 |
| `metrorail_stations` | 73 | Point: 73 | 21 |
| `myciti_routes` | 131 | LineString: 131 | 9 |
| `myciti_stops` | 1,810 | Point: 1,810 | 12 |
| `taxi_routes` | 1,466 | LineString: 1,466 | 6 |

## Dataset Details

## golden_arrow_routes

Records: **1,991**

### Geometry

- LineString: **1,933**
- MultiLineString: **58**
- Missing geometry: **0**

### Fields

| Field | Blank | Unique | Types | Samples |
|---|---:|---:|---|---|
| `Bearing` | 0 | 330 | integer:1991 | 274; 94; 339; 85; 277 |
| `Bus_opera1` | 0 | 1 | string:1991 | 'Golden Arrow' |
| `Check_` | 0 | 3 | integer:1991 | 18; 19; 0 |
| `GeomNull` | 1,467 | 1 | string:524 | '0' |
| `ID` | 0 | 1,988 | string:1991 | '24e4ca14-41e3-4d54-b63e-9ad01702c96b'; 'ee605836-8bd7-4a4f-845f-22368d12f77e'; '9d2c015d-4113-4da0-89bd-f9a715634df9'; '66d99d24-be19-4362-8c01-a1f71c184bc9'; '035f1459-5dc8-4894-beb7-1bf01d9097ca' |
| `MaxX` | 0 | 398 | integer:1991 | -53182; -53033; -53150; -33305; -37490 |
| `MaxY` | 0 | 465 | integer:1991 | -3753556; -3753547; -3753188; -3750896; -3755395 |
| `MinX` | 0 | 401 | integer:1991 | -57427; -57403; -54279; -53484; -53181 |
| `MinY` | 0 | 348 | integer:1991 | -3755428; -3755475; -3755394; -3759433; -3755859 |
| `OBJECTID` | 0 | 1,991 | integer:1991 | 1; 2; 3; 4; 5 |
| `Route_No` | 0 | 1,988 | string:1991 | 'AAA6'; 'AAA7'; 'AAE0'; 'ADA1'; 'ADB0' |
| `Route_name` | 0 | 1,988 | string:1991 | 'AAA6: CITY GOLDEN ACRE C LANE to SEA POINT'; 'AAA7: SEA POINT to CITY'; 'AAE0: CITY GOLDEN ACRE C LANE to SOMERSET HOSP'; 'ADA1: CITY GOLDEN ACRE D LANE to BELLVILLE'; 'ADB0: BISHOP LAVIS to CITY' |
| `Shape_Length` | 0 | 1,972 | float:1990, integer:1 | 6578.574958203401; 6504.6199321913455; 3176.024459994503; 29011.270917753776; 19500.73676643176 |

## golden_arrow_stops

Records: **2,000**

### Geometry

- Point: **2,000**
- Missing geometry: **0**

### Fields

| Field | Blank | Unique | Types | Samples |
|---|---:|---:|---|---|
| `BUSSTOPDES` | 0 | 663 | string:2000 | 'Golden Acre'; 'On Darling Street after Plein'; 'On Adderley Street 1st after Hout'; 'On Adderley Street 2nd after Hout'; 'On Riebeek Street after Adderley' |
| `BUSSTOPNO` | 14 | 679 | string:1986 | 'GABS008'; '745'; '239'; '802'; '3878' |
| `CLASSIFICA` | 0 | 2 | string:2000 | 'Station'; 'Stop' |
| `OBJECTID` | 0 | 2,000 | integer:2000 | 1; 2; 3; 4; 5 |
| `ORDINAL` | 0 | 80 | integer:2000 | 1; 2; 3; 4; 5 |
| `ROUTECODE` | 0 | 48 | string:2000 | 'AAA6'; 'AAA7'; 'AAE0'; 'ADA0'; 'ADA1' |
| `ROUTENAME` | 0 | 33 | string:2000 | 'CITY GOLDEN ACRE C LANE to SEA POINT'; 'SEA POINT to CITY'; 'CITY GOLDEN ACRE C LANE to SOMERSET HOSP'; 'BELLVILLE B LANE to CITY'; 'CITY GOLDEN ACRE D LANE to BELLVILLE' |
| `XCOORD` | 0 | 666 | integer:2000 | -53179; -53377; -53432; -53374; -53322 |
| `YCOORD` | 0 | 648 | integer:2000 | -3755390; -3755415; -3755256; -3755191; -3754967 |

## metrorail_lines

Records: **10**

### Geometry

- LineString: **10**
- Missing geometry: **0**

### Fields

| Field | Blank | Unique | Types | Samples |
|---|---:|---:|---|---|
| `ID` | 0 | 1 | integer:10 | 0 |
| `LINEID` | 0 | 10 | integer:10 | 1059; 1067; 1074; 1066; 1069 |
| `LINENAME` | 0 | 10 | string:10 | 'Cape Town-Chris Hani'; "Cape Town-Simin's Town"; 'Cape Town-Kapteinsklip'; 'Cape Town-Century City-Bellville'; 'Cape Town-Southfield-Retreat' |
| `Lenght` | 0 | 1 | integer:10 | 0 |
| `OBJECTID` | 0 | 10 | integer:10 | 1; 2; 3; 4; 5 |
| `Shape_Length` | 0 | 10 | float:10 | 38662.24169102337; 35973.923580874754; 31446.041606495084; 20382.02268596492; 23694.937473474733 |

## metrorail_stations

Records: **73**

### Geometry

- Point: **73**
- Missing geometry: **0**

### Fields

| Field | Blank | Unique | Types | Samples |
|---|---:|---:|---|---|
| `ENTITY_1` | 0 | 1 | string:73 | 'PRASA' |
| `LATITUDE_1` | 0 | 73 | float:73 | -33.96089032; -33.89777625; -33.93944056; -33.90629829; -33.96426596 |
| `LONGITUD_1` | 0 | 73 | float:73 | 18.5016223; 18.59307193; 18.60905681; 18.6274906; 18.70126312 |
| `Latitude` | 0 | 73 | float:73 | -33.96089; -33.897776; -33.939441; -33.906298; -33.964266 |
| `Longitude` | 0 | 73 | float:73 | 18.501622; 18.593072; 18.609057; 18.627491; 18.701263 |
| `OBJECTID` | 0 | 73 | integer:73 | 1; 2; 3; 4; 5 |
| `OID_` | 0 | 73 | integer:73 | 49; 51; 9; 6; 4 |
| `PLACENAM_2` | 0 | 73 | string:73 | 'ATHLONE'; 'AVONDALE'; 'BELHAR'; 'BELLVILLE'; 'BLACKHEATH' |
| `PLACENAM_3` | 1 | 72 | string:72 | 'ATHLONE'; 'AVONDALE'; 'BELHAR'; 'BELLVILLE'; 'BLACKHEATH' |
| `REMARKS_1` | 73 | 0 |  |  |
| `Rank` | 0 | 73 | integer:73 | 91; 324; 151; 5; 59 |
| `RegionID` | 0 | 1 | string:73 | 'WC' |
| `STATIONCAT` | 0 | 4 | string:73 | 'Intermediate'; 'Small'; 'Supercore'; 'Core' |
| `Station` | 0 | 73 | string:73 | 'ATHLONE'; 'AVONDALE'; 'BELHAR'; 'BELLVILLE'; 'BLACKHEATH' |
| `StationID` | 0 | 73 | string:73 | 'ATL'; 'AVD'; 'BOH'; 'BLE'; 'BKH' |
| `StationI_1` | 0 | 73 | string:73 | 'ATL'; 'AVD'; 'BOH'; 'BLE'; 'BKH' |
| `StationNAm` | 0 | 73 | string:73 | 'ATHLONE'; 'AVONDALE'; 'BELHAR'; 'BELLVILLE'; 'BLACKHEATH' |
| `StationOwn` | 0 | 4 | string:73 | 'PRASA STATION'; 'TRANSNET STATION BUT USED ONLY BY METRORAIL'; 'PRASA STATION/SMEYL (USED BY TRANSNET)'; 'PRASA STATION/SMEYL' |
| `Station__1` | 0 | 73 | string:73 | 'ATL'; 'AVD'; 'BOH'; 'BLE'; 'BKH' |
| `SubRegion` | 0 | 1 | string:73 | 'Western Cape' |
| `Total` | 0 | 73 | float:63, integer:10 | 33231379.6; 28781715; 28075343.9; 24754902.8; 23851954.9 |

## myciti_routes

Records: **131**

### Geometry

- LineString: **131**
- Missing geometry: **0**

### Fields

| Field | Blank | Unique | Types | Samples |
|---|---:|---:|---|---|
| `LNTH` | 131 | 0 |  |  |
| `NEW_RT` | 131 | 0 |  |  |
| `OBJECTID` | 0 | 131 | integer:131 | 1; 2; 3; 4; 5 |
| `OBJECTID_1` | 0 | 131 | integer:131 | 1; 2; 3; 4; 5 |
| `OD` | 131 | 0 |  |  |
| `RT_OD` | 131 | 0 |  |  |
| `SHAPESTLen` | 0 | 129 | float:131 | 8388.549891120114; 10577.924929567755; 4799.068867503414; 4565.107459294188; 6371.802258817573 |
| `SRVC_TYPE` | 131 | 0 |  |  |
| `Shape_Length` | 0 | 129 | float:131 | 8390.589909203385; 10580.484054173727; 4800.207627134665; 4566.1925356754655; 6373.537604057124 |

## myciti_stops

Records: **1,810**

### Geometry

- Point: **1,810**
- Missing geometry: **0**

### Fields

| Field | Blank | Unique | Types | Samples |
|---|---:|---:|---|---|
| `NAME` | 18 | 518 | string:1792 | 'Atlantis'; 'Arion'; 'Charel Uys North'; 'Montreal'; 'Tsitsikamma' |
| `NEW_STOP_N` | 1,810 | 0 |  |  |
| `OBJECTID` | 0 | 1,810 | integer:1810 | 1; 2; 3; 4; 5 |
| `OBJECTID_1` | 0 | 1,810 | integer:1810 | 1; 2; 3; 4; 5 |
| `PSTN` | 1,810 | 0 |  |  |
| `RAIL_STN` | 1,810 | 0 |  |  |
| `ROAD` | 1,810 | 0 |  |  |
| `SHLT_TYPE` | 1,810 | 0 |  |  |
| `STN_NAME` | 1,810 | 0 |  |  |
| `STN_TYPE` | 1,810 | 0 |  |  |
| `STOP_NAME` | 1,810 | 0 |  |  |
| `STOP_NMBR` | 1,810 | 0 |  |  |

## taxi_routes

Records: **1,466**

### Geometry

- LineString: **1,466**
- Missing geometry: **0**

### Fields

| Field | Blank | Unique | Types | Samples |
|---|---:|---:|---|---|
| `DSTN` | 19 | 488 | string:1447 | 'DURBANVILLE'; 'NYANGA'; 'KHAYELITSHA'; 'MOWBRAY'; 'CLAREMONT' |
| `OBJECTID` | 0 | 1,466 | integer:1466 | 1; 2; 3; 4; 5 |
| `OBJECTID_1` | 0 | 1,466 | integer:1466 | 1; 2; 3; 4; 5 |
| `ORGN` | 19 | 234 | string:1447 | 'BELLVILLE'; 'GUGULETU'; 'KHAYELITSHA'; 'MITCHELLS PLAIN - TOWN CENTRE'; 'LANGA' |
| `SHAPESTLen` | 0 | 1,411 | float:1466 | 10698.755195302632; 13093.74402609485; 18398.9711600458; 20651.04222279763; 12817.030617147171 |
| `Shape_Length` | 0 | 1,412 | float:1466 | 12918.668591667976; 15814.788629403229; 22221.73322562913; 24910.267147374274; 15462.341550952851 |

## Relationship Analysis

### Golden Arrow Route → Stop

- Unique route codes: **1,988**
- Unique stop route codes: **48**
- Matching route codes: **42**
- Stop codes without matching route: **6**
- Routes without matching stop code: **1,946**

### Taxi Routes

- Unique origins: **234**
- Unique destinations: **488**
- Unique origin → destination pairs: **1,122**
- Duplicate origin → destination pairs: **223**

### Metrorail

- Unique railway line IDs: **10**
- Unique station IDs: **73**
- ⚠️ Stations do **not** contain a `LINEID` field.
- A station → line relationship should not be invented.

## Engineering Observations

1. Raw data should remain unchanged.
2. Source-specific fields should be standardized in the Silver layer.
3. Relationships should only be created when supported by source data or a documented spatial derivation.
4. Taxi data currently represents routes with origin and destination fields; no separate taxi-stop dataset was extracted.
5. Metrorail stations do not expose an obvious `LINEID` relationship.
