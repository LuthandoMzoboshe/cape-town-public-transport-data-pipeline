from pathlib import Path
import pandas as pd

SILVER_DIR = Path("data/processed")
GOLD_DIR = Path("data/gold/transport_stops")


def transform_golden_arrow():
    file = SILVER_DIR / "golden_arrow/golden_arrow_stops.parquet"
    df = pd.read_parquet(file)

    return pd.DataFrame({
        "transport_mode": "bus",
        "source_system": "golden_arrow",
        "location_type": "stop",
        "source_location_id": df["stop_id"].astype("string"),
        "stop_code": df["stop_code"],
        "location_name": df["stop_name"],
        "classification": df["classification"],
        "route_code": df["route_code"],
        "stop_sequence": df["stop_sequence"],
        "station_owner": None,
        "station_category": None,
        "sub_region": None,
        "region_id": None,
        "latitude": None,
        "longitude": None,
        "geometry": df["geometry"],
    })


def transform_myciti():
    file = SILVER_DIR / "myciti/myciti_stops.parquet"
    df = pd.read_parquet(file)

    return pd.DataFrame({
        "transport_mode": "bus",
        "source_system": "myciti",
        "location_type": "stop",
        "source_location_id": df["stop_id"].astype("string"),
        "stop_code": None,
        "location_name": df["stop_name"],
        "classification": None,
        "route_code": None,
        "stop_sequence": None,
        "station_owner": None,
        "station_category": None,
        "sub_region": None,
        "region_id": None,
        "latitude": None,
        "longitude": None,
        "geometry": df["geometry"],
    })


def transform_metrorail():
    file = SILVER_DIR / "metrorail/metrorail_stations.parquet"
    df = pd.read_parquet(file)

    return pd.DataFrame({
        "transport_mode": "rail",
        "source_system": "metrorail",
        "location_type": "station",
        "source_location_id": df["station_id"].astype("string"),
        "stop_code": None,
        "location_name": df["station_name"],
        "classification": None,
        "route_code": None,
        "stop_sequence": None,
        "station_owner": df["station_owner"],
        "station_category": df["station_category"],
        "sub_region": df["sub_region"],
        "region_id": df["region_id"],
        "latitude": df["latitude"],
        "longitude": df["longitude"],
        "geometry": df["geometry"],
    })


def main():
    GOLD_DIR.mkdir(parents=True, exist_ok=True)

    golden_arrow = transform_golden_arrow()
    myciti = transform_myciti()
    metrorail = transform_metrorail()

    transport_stops = pd.concat(
        [golden_arrow, myciti, metrorail],
        ignore_index=True
    )

    output_file = GOLD_DIR / "transport_stops.parquet"
    transport_stops.to_parquet(output_file, index=False)

    print("Gold transport stops transformation complete.")
    print(f"Total locations: {len(transport_stops)}")
    print()
    print("Locations by transport mode:")
    print(transport_stops["transport_mode"].value_counts())
    print()
    print("Locations by type:")
    print(transport_stops["location_type"].value_counts())
    print()
    print("Created:")
    print(output_file)


if __name__ == "__main__":
    main()