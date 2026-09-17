from pathlib import Path
import pandas as pd

GOLD_DIR = Path("data/gold")
OUTPUT_DIR = GOLD_DIR / "transport_summary"


def load_routes():
    file = GOLD_DIR / "transport_routes/transport_routes.parquet"
    return pd.read_parquet(file)


def load_locations():
    file = GOLD_DIR / "transport_stops/transport_stops.parquet"
    return pd.read_parquet(file)


def build_summary(routes, locations):
    route_summary = (
        routes
        .groupby(["transport_mode", "source_system"])
        .agg(
            route_count=("source_route_id", "count"),
            route_length_total_m=("route_length_m", "sum"),
            route_length_avg_m=("route_length_m", "mean"),
            geometry_count=("geometry", "count"),
        )
        .reset_index()
    )

    location_summary = (
        locations
        .groupby(["transport_mode", "source_system"])
        .agg(
            location_count=("source_location_id", "count"),
            named_location_count=("location_name", "count"),
        )
        .reset_index()
    )

    summary = route_summary.merge(
        location_summary,
        on=["transport_mode", "source_system"],
        how="outer",
    )

    summary["location_count"] = summary["location_count"].fillna(0).astype(int)
    summary["named_location_count"] = summary["named_location_count"].fillna(0).astype(int)

    return summary[
        [
            "transport_mode",
            "source_system",
            "route_count",
            "location_count",
            "named_location_count",
            "route_length_total_m",
            "route_length_avg_m",
            "geometry_count",
        ]
    ]


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    routes = load_routes()
    locations = load_locations()

    summary = build_summary(routes, locations)

    output_file = OUTPUT_DIR / "transport_summary.parquet"
    summary.to_parquet(output_file, index=False)

    print("Gold transport summary transformation complete.")
    print(f"Summary rows: {len(summary)}")
    print()
    print(summary.to_string(index=False))
    print()
    print("Created:")
    print(output_file)


if __name__ == "__main__":
    main()