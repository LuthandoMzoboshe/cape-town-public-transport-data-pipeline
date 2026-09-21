
from pathlib import Path

import pandas as pd


SILVER_DIR = Path("data/processed")
GOLD_DIR = Path("data/gold/transport_stops")


COLUMNS = [
    "transport_mode",
    "source_system",
    "location_type",
    "source_location_id",
    "stop_code",
    "location_name",
    "classification",
    "route_code",
    "stop_sequence",
    "station_owner",
    "station_category",
    "sub_region",
    "region_id",
    "latitude",
    "longitude",
    "geometry",
]


def prepare_dataframe(df):
    df = df.copy()

    string_columns = [
        "transport_mode",
        "source_system",
        "location_type",
        "source_location_id",
        "stop_code",
        "location_name",
        "classification",
        "route_code",
        "station_owner",
        "station_category",
        "sub_region",
        "region_id",
    ]

    for column in string_columns:
        df[column] = df[column].astype("string")

    df["stop_sequence"] = pd.to_numeric(
        df["stop_sequence"],
        errors="coerce"
    ).astype("Int64")

    df["latitude"] = pd.to_numeric(
        df["latitude"],
        errors="coerce"
    )

    df["longitude"] = pd.to_numeric(
        df["longitude"],
        errors="coerce"
    )

    return df[COLUMNS]


def empty_string_series(index):
    return pd.Series(pd.NA, index=index, dtype="string")


def empty_integer_series(index):
    return pd.Series(pd.NA, index=index, dtype="Int64")


def empty_float_series(index):
    return pd.Series(float("nan"), index=index, dtype="float64")


def transform_golden_arrow():
    file = SILVER_DIR / "golden_arrow/golden_arrow_stops.parquet"
    df = pd.read_parquet(file)

    return prepare_dataframe(pd.DataFrame({
        "transport_mode": "bus",
        "source_system": "golden_arrow",
        "location_type": "stop",
        "source_location_id": df["stop_id"].astype("string"),
        "stop_code": df["stop_code"],
        "location_name": df["stop_name"],
        "classification": df["classification"],
        "route_code": df["route_code"],
        "stop_sequence": df["stop_sequence"],
        "station_owner": empty_string_series(df.index),
        "station_category": empty_string_series(df.index),
        "sub_region": empty_string_series(df.index),
        "region_id": empty_string_series(df.index),
        "latitude": empty_float_series(df.index),
        "longitude": empty_float_series(df.index),
        "geometry": df["geometry"],
    }))


def transform_myciti():
    file = SILVER_DIR / "myciti/myciti_stops.parquet"
    df = pd.read_parquet(file)

    return prepare_dataframe(pd.DataFrame({
        "transport_mode": "bus",
        "source_system": "myciti",
        "location_type": "stop",
        "source_location_id": df["stop_id"].astype("string"),
        "stop_code": empty_string_series(df.index),
        "location_name": df["stop_name"],
        "classification": empty_string_series(df.index),
        "route_code": empty_string_series(df.index),
        "stop_sequence": empty_integer_series(df.index),
        "station_owner": empty_string_series(df.index),
        "station_category": empty_string_series(df.index),
        "sub_region": empty_string_series(df.index),
        "region_id": empty_string_series(df.index),
        "latitude": empty_float_series(df.index),
        "longitude": empty_float_series(df.index),
        "geometry": df["geometry"],
    }))


def transform_metrorail():
    file = SILVER_DIR / "metrorail/metrorail_stations.parquet"
    df = pd.read_parquet(file)

    return prepare_dataframe(pd.DataFrame({
        "transport_mode": "rail",
        "source_system": "metrorail",
        "location_type": "station",
        "source_location_id": df["station_id"].astype("string"),
        "stop_code": empty_string_series(df.index),
        "location_name": df["station_name"],
        "classification": empty_string_series(df.index),
        "route_code": empty_string_series(df.index),
        "stop_sequence": empty_integer_series(df.index),
        "station_owner": df["station_owner"],
        "station_category": df["station_category"],
        "sub_region": df["sub_region"],
        "region_id": df["region_id"],
        "latitude": df["latitude"],
        "longitude": df["longitude"],
        "geometry": df["geometry"],
    }))


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

