from pathlib import Path
import pandas as pd

SILVER_DIR = Path("data/processed")
GOLD_DIR = Path("data/gold/transport_routes")

def transform_golden_arrow():
    file = SILVER_DIR / "golden_arrow" / "golden_arrow_routes.parquet"
    df = pd.read_parquet(file)

    return pd.DataFrame({
        "transport_mode": "bus",
        "source_system": "golden_arrow",
        "source_route_id": df["route_id"],
        "route_name": df["route_name"],
        "origin": None,
        "destination": None,
        "operator": df["operator"],
        "route_length_m": df["length_m"],
        "geometry": df["geometry"],
    })

def transform_myciti():
    file = SILVER_DIR / "myciti/myciti_routes.parquet"
    df = pd.read_parquet(file)

    return pd.DataFrame({
        "transport_mode": "bus",
        "source_system": "myciti",
        "source_route_id": df["route_id"],
        "route_name": None,
        "origin": None,
        "destination": None,
        "operator": None,
        "route_length_m": df["shape_length_m"],
        "geometry": df["geometry"],
    })


def transform_taxi():
    file = SILVER_DIR / "taxi/taxi_routes.parquet"
    df = pd.read_parquet(file)

    return pd.DataFrame({
        "transport_mode": "taxi",
        "source_system": "taxi",
        "source_route_id": df["route_id"],
        "route_name": None,
        "origin": df["origin"],
        "destination": df["destination"],
        "operator": None,
        "route_length_m": df["shape_length_m"],
        "geometry": df["geometry"],
    })


def transform_metrorail():
    file = SILVER_DIR / "metrorail/metrorail_lines.parquet"
    df = pd.read_parquet(file)

    return pd.DataFrame({
        "transport_mode": "rail",
        "source_system": "metrorail",
        "source_route_id": df["line_id"],
        "route_name": df["line_name"],
        "origin": None,
        "destination": None,
        "operator": None,
        "route_length_m": df["shape_length_m"],
        "geometry": df["geometry"],
    })


def main():
    GOLD_DIR.mkdir(parents=True, exist_ok=True)

    golden_arrow = transform_golden_arrow()
    myciti = transform_myciti()
    taxi = transform_taxi()
    metrorail = transform_metrorail()

    transport_routes = pd.concat(
        [
            golden_arrow,
            myciti,
            taxi,
            metrorail,
        ],
        ignore_index=True,
    )

    output_file = GOLD_DIR / "transport_routes.parquet"

    transport_routes.to_parquet(
        output_file,
        index=False,
    )

    print("Gold transport routes transformation complete.")
    print(f"Total routes: {len(transport_routes)}")
    print()
    print("Routes by transport mode:")
    print(transport_routes["transport_mode"].value_counts())
    print()
    print("Created:")
    print(output_file)


if __name__ == "__main__":
    main()