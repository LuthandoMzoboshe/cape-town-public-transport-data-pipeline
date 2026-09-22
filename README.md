# cape-town-public-transport-data-pipeline

WTC Verification Code: WTC-F2WVRL37


Overview

An end-to-end data engineering project built using public transport data from the Western Cape Government GIS service.

The pipeline extracts data for Golden Arrow, MyCiTi, Metrorail, and taxi routes, profiles the source data, transforms it through Silver and Gold layers, and performs automated data quality validation.

Western Cape GIS API
        ↓
   Raw / Bronze
        ↓
     Profiling
        ↓
Relationship Analysis
        ↓
      Silver
        ↓
Silver Validation
        ↓
       Gold
        ↓
Gold Validation
Data Sources

The pipeline works with:

Golden Arrow routes and stops
MyCiTi routes and stops
Metrorail lines and stations
Taxi routes

The source data is obtained from the Western Cape Government GIS service.

Pipeline
1. Raw / Bronze

Source data is extracted as timestamped GeoJSON files and stored under:

data/raw/

Previous extracts are preserved rather than overwritten.

2. Profiling

The raw datasets are profiled to understand:

record counts
available fields
missing values
geometry types
dataset structure

The profiling report is generated in:

data/profiling/transport_data_profile.md

3. Relationship Analysis

The source datasets are analyzed to determine which relationships are actually supported by the available data.

Relationships are not invented when the source data does not provide enough information to establish them reliably.

4. Silver Layer

The Silver layer contains cleaned, source-specific Parquet datasets.

data/processed/
├── golden_arrow/
├── myciti/
├── taxi/
└── metrorail/

Silver validation checks row counts, missing values, duplicates, and expected outputs.

5. Gold Layer

The Gold layer provides standardized analytical datasets:

data/gold/
├── transport_routes/
├── transport_stops/
└── transport_summary/
Transport Routes

Standardizes route and line records across Golden Arrow, MyCiTi, taxi routes, and Metrorail.

Common fields include:

transport_mode
source_system
source_route_id
route_name
origin
destination
operator
route_length_m
geometry
Transport Stops

Combines Golden Arrow stops, MyCiTi stops, and Metrorail stations into a standardized location dataset.

location_type distinguishes between stop and station.

Taxi stops are not included because the source data does not contain a separate taxi stop dataset.

Transport Summary

Provides high-level metrics for each transport source system, including:

route/line count
location count
named location count
total route length
average route length
geometry count
Data Quality

Automated validation is performed using:

src/validate_silver.py
src/validate_gold.py

Checks include:

required files and columns
missing values
duplicate records
valid transport modes and source systems
route lengths
geometry completeness

Source-level data quality issues are preserved rather than silently removed.

For example, one Golden Arrow route contains a source-provided route length of 0 and an empty geometry. The validator reports this as a warning while retaining the original record.

Automated Pipeline

The entire pipeline can be run with:

python3 -m src.run_pipeline

The pipeline automatically runs extraction, profiling, relationship analysis, Silver transformations, Silver validation, Gold transformations, and Gold validation.

Results

The current pipeline produces:

3,598 route and line records
3,883 transport locations
4 transport-system summary records
Transport System	Routes / Lines	Locations
Golden Arrow	1,991	2,000
MyCiTi	131	1,810
Taxi	1,466	0
Metrorail	10	73
Technologies
Python
Pandas
Requests
GeoJSON
Apache Parquet
PyArrow
Git & GitHub
Project Structure
src/
├── transformations/
├── utils/
├── extract_transport.py
├── profile_raw_data.py
├── analyze_relationships.py
├── run_pipeline.py
├── validate_silver.py
└── validate_gold.py

data/
├── processed/
├── gold/
└── profiling/

Running the Project:

python3 -m src.run_pipeline

The pipeline completes successfully with Silver and Gold validation passing.
