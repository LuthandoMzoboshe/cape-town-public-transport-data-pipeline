import json
from pathlib import Path

import pandas as pd

from src.utils.raw_files import latest_geojson


PROCESSED_DIR = Path("data/processed/taxi")

ROUTES_FILE = latest_geojson("taxi_routes")


def load_geojson(path):
    with open(path) as f:
        return json.load(f)


def clean_text(value):
    value = str(value).strip()

    return value if value else None


def transform_routes(data):
    rows = []

    for feature in data["features"]:
        props = feature["properties"]

        rows.append({
            "route_id": props["OBJECTID"],
            "origin": clean_text(props["ORGN"]),
            "destination": clean_text(props["DSTN"]),
            "shape_length_m": props["Shape_Length"],
            "source_length_m": props["SHAPESTLen"],
            "geometry": json.dumps(feature["geometry"]),
        })

    return pd.DataFrame(rows)


def main():
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    routes_data = load_geojson(ROUTES_FILE)
    routes = transform_routes(routes_data)

    output_file = PROCESSED_DIR / "taxi_routes.parquet"

    routes.to_parquet(
        output_file,
        index=False
    )

    print("Taxi Silver transformation complete.")
    print(f"Routes: {len(routes)}")
    print()
    print("Created:")
    print(output_file)


if __name__ == "__main__":
    main()