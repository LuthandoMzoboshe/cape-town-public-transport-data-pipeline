import json
from pathlib import Path

import pandas as pd


RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed/metrorail")

LINES_FILE = next((RAW_DIR / "metrorail_lines").glob("*.geojson"))
STATIONS_FILE = next((RAW_DIR / "metrorail_stations").glob("*.geojson"))


def load_geojson(path):
    with open(path) as f:
        return json.load(f)


def clean_text(value):
    value = str(value).strip()

    return value if value else None


def transform_lines(data):
    rows = []

    for feature in data["features"]:
        props = feature["properties"]

        rows.append({
            "line_id": props["LINEID"],
            "line_name": clean_text(props["LINENAME"]),
            "shape_length_m": props["Shape_Length"],
            "geometry": json.dumps(feature["geometry"]),
        })

    return pd.DataFrame(rows)


def transform_stations(data):
    rows = []

    for feature in data["features"]:
        props = feature["properties"]

        rows.append({
            "station_id": clean_text(props["StationID"]),
            "station_name": clean_text(props["StationNAm"]),
            "station_owner": clean_text(props["StationOwn"]),
            "sub_region": clean_text(props["SubRegion"]),
            "region_id": clean_text(props["RegionID"]),
            "station_category": clean_text(props["STATIONCAT"]),
            "latitude": props["Latitude"],
            "longitude": props["Longitude"],
            "geometry": json.dumps(feature["geometry"]),
        })

    return pd.DataFrame(rows)


def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    lines_data = load_geojson(LINES_FILE)
    stations_data = load_geojson(STATIONS_FILE)

    lines = transform_lines(lines_data)
    stations = transform_stations(stations_data)

    lines.to_parquet(
        PROCESSED_DIR / "metrorail_lines.parquet",
        index=False
    )

    stations.to_parquet(
        PROCESSED_DIR / "metrorail_stations.parquet",
        index=False
    )

    print("Metrorail Silver transformation complete.")
    print(f"Lines: {len(lines)}")
    print(f"Stations: {len(stations)}")
    print()
    print("Created:")
    print(PROCESSED_DIR / "metrorail_lines.parquet")
    print(PROCESSED_DIR / "metrorail_stations.parquet")


if __name__ == "__main__":
    main()