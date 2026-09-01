import json
from pathlib import Path

import pandas as pd


RAW = Path("data/raw")
OUTPUT = Path("data/processed/golden_arrow")


def clean_value(value):
    if value is None:
        return None

    if isinstance(value, str):
        value = value.strip()
        return value if value else None

    return value


def load_geojson(folder):
    files = list(folder.glob("*.geojson"))

    if not files:
        raise FileNotFoundError(f"No GeoJSON file found in {folder}")

    with open(files[0], "r", encoding="utf-8") as f:
        return json.load(f)["features"]


def transform_routes():
    features = load_geojson(RAW / "golden_arrow_routes")

    records = []

    for feature in features:
        properties = feature["properties"]

        records.append({
    "route_id": properties.get("OBJECTID"),
    "route_code": clean_value(properties.get("Route_No")),
    "route_name": clean_value(properties.get("Route_name")),
    "operator": clean_value(properties.get("Bus_opera1")),
    "bearing": properties.get("Bearing"),
    "length_m": properties.get("Shape_Length"),
    "geometry": json.dumps(feature.get("geometry"))
})

    df = pd.DataFrame(records)

    df = df.drop_duplicates(subset=["route_id"])

    return df


def transform_stops():
    features = load_geojson(RAW / "golden_arrow_stops")

    records = []

    for feature in features:
        properties = feature["properties"]

        records.append({
    "stop_id": properties.get("OBJECTID"),
    "stop_code": clean_value(properties.get("BUSSTOPNO")),
    "stop_name": clean_value(properties.get("BUSSTOPDES")),
    "classification": clean_value(properties.get("CLASSIFICA")),
    "route_code": clean_value(properties.get("ROUTECODE")),
    "stop_sequence": properties.get("ORDINAL"),
    "geometry": json.dumps(feature.get("geometry"))
})

    df = pd.DataFrame(records)

    df = df.drop_duplicates(subset=["stop_id"])

    return df


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)

    print("Transforming Golden Arrow routes...")
    routes = transform_routes()

    print("Transforming Golden Arrow stops...")
    stops = transform_stops()

    routes_file = OUTPUT / "golden_arrow_routes.parquet"
    stops_file = OUTPUT / "golden_arrow_stops.parquet"

    routes.to_parquet(routes_file, index=False)
    stops.to_parquet(stops_file, index=False)

    print()
    print("Silver transformation complete.")
    print(f"Routes: {len(routes)}")
    print(f"Stops: {len(stops)}")
    print()
    print(f"Created: {routes_file}")
    print(f"Created: {stops_file}")


if __name__ == "__main__":
    main()