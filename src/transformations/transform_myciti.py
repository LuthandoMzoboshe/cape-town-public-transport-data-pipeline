import json
from pathlib import Path

import pandas as pd


RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed/myciti")

ROUTES_FILE = RAW_DIR / "myciti_routes/myciti_routes_20260831T124830Z.geojson"
STOPS_FILE = RAW_DIR / "myciti_stops/myciti_stops_20260831T124830Z.geojson"


def load_geojson(path):
    with open(path) as f:
        return json.load(f)


def transform_routes(data):
    rows = []

    for feature in data["features"]:
        props = feature["properties"]

        rows.append({
            "route_id": props["OBJECTID"],
            "shape_length_m": props["Shape_Length"],
            "source_length_m": props["SHAPESTLen"],
            "geometry": json.dumps(feature["geometry"]),
        })

    return pd.DataFrame(rows)


def transform_stops(data):
    rows = []

    for feature in data["features"]:
        props = feature["properties"]

        stop_name = str(props["NAME"]).strip()

        rows.append({
            "stop_id": props["OBJECTID"],
            "stop_name": stop_name if stop_name else None,
            "geometry": json.dumps(feature["geometry"]),
        })

    return pd.DataFrame(rows)


def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    routes_data = load_geojson(ROUTES_FILE)
    stops_data = load_geojson(STOPS_FILE)

    routes = transform_routes(routes_data)
    stops = transform_stops(stops_data)

    routes.to_parquet(
        PROCESSED_DIR / "myciti_routes.parquet",
        index=False
    )

    stops.to_parquet(
        PROCESSED_DIR / "myciti_stops.parquet",
        index=False
    )

    print("MyCiTi Silver transformation complete.")
    print(f"Routes: {len(routes)}")
    print(f"Stops: {len(stops)}")
    print()
    print("Created:")
    print(PROCESSED_DIR / "myciti_routes.parquet")
    print(PROCESSED_DIR / "myciti_stops.parquet")


if __name__ == "__main__":
    main()