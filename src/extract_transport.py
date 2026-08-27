import json
from datetime import datetime, timezone
from pathlib import Path

import requests


BASE_URL = (
    "https://gis.westerncape.gov.za/server2/rest/services/"
    "SpatialDataWarehouse/Transportation/MapServer"
)

DATASETS = {
    "myciti_routes": 9,
    "myciti_stops": 10,
    "golden_arrow_routes": 5,
    "golden_arrow_stops": 6,
    "metrorail_stations": 3,
    "metrorail_lines": 4,
    "taxi_routes": 24,
}


RAW_DIR = Path("data/raw")


def extract_layer(name: str, layer_id: int) -> None:
    print(f"\nExtracting: {name}")

    url = f"{BASE_URL}/{layer_id}/query"

    params = {
        "where": "1=1",
        "outFields": "*",
        "returnGeometry": "true",
        "f": "geojson",
    }

    response = requests.get(url, params=params, timeout=60)
    response.raise_for_status()

    data = response.json()

    output_dir = RAW_DIR / name
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    output_file = output_dir / f"{name}_{timestamp}.geojson"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

    feature_count = len(data.get("features", []))

    print(f"Records extracted: {feature_count}")
    print(f"Saved to: {output_file}")


def main() -> None:
    print("Cape Town Public Transport - Bronze Extraction")
    print("=" * 55)

    for name, layer_id in DATASETS.items():
        try:
            extract_layer(name, layer_id)
        except requests.RequestException as error:
            print(f"ERROR extracting {name}: {error}")
        except ValueError as error:
            print(f"ERROR parsing {name}: {error}")

    print("\nExtraction complete.")


if __name__ == "__main__":
    main()