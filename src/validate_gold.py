from pathlib import Path
import pandas as pd

GOLD_DIR = Path("data/gold")

FILES = {
    "transport_routes": {
        "path": GOLD_DIR / "transport_routes/transport_routes.parquet",
        "required_columns": [
            "transport_mode",
            "source_system",
            "source_route_id",
            "route_length_m",
            "geometry",
        ],
    },
    "transport_stops": {
        "path": GOLD_DIR / "transport_stops/transport_stops.parquet",
        "required_columns": [
            "transport_mode",
            "source_system",
            "location_type",
            "source_location_id",
            "geometry",
        ],
    },
    "transport_summary": {
        "path": GOLD_DIR / "transport_summary/transport_summary.parquet",
        "required_columns": [
            "transport_mode",
            "source_system",
            "route_count",
            "location_count",
        ],
    },
}

def validate_transport_modes(df):
    expected_modes = {"bus", "rail", "taxi"}
    actual_modes = set(df["transport_mode"].dropna().unique())

    unexpected_modes = actual_modes - expected_modes

    if unexpected_modes:
        print(f"FAIL: Unexpected transport modes = {unexpected_modes}")
        return False

    print("PASS: Transport modes are valid")
    return True

def validate_route_lengths(df):
    if "route_length_m" not in df.columns:
        return True

    negative = (df["route_length_m"] < 0).sum()
    zero = (df["route_length_m"] == 0).sum()

    if negative > 0:
        print(f"FAIL: Negative route lengths = {negative}")
        return False

    if zero > 0:
        print(f"WARNING: Zero route lengths inherited from source = {zero}")
    else:
        print("PASS: Route lengths are positive")

    return True

def validate_geometry(df):
    if "geometry" not in df.columns:
        return True

    empty = (
        df["geometry"].isna()
        | df["geometry"].astype(str).str.contains(
            '"coordinates": []',
            regex=False,
        )
    ).sum()

    if empty > 0:
        print(f"WARNING: Empty geometries inherited from source = {empty}")
    else:
        print("PASS: Geometries are populated")

    return True


def validate_source_systems(name, df):
    expected = {
        "transport_routes": {
            "golden_arrow",
            "myciti",
            "taxi",
            "metrorail",
        },
        "transport_stops": {
            "golden_arrow",
            "myciti",
            "metrorail",
        },
        "transport_summary": {
            "golden_arrow",
            "myciti",
            "taxi",
            "metrorail",
        },
    }

    actual = set(df["source_system"].dropna().unique())
    unexpected = actual - expected[name]

    if unexpected:
        print(f"FAIL: Unexpected source systems = {unexpected}")
        return False

    print("PASS: Source systems are valid")
    return True


def validate_file(name, config):
    file = config["path"]

    print("\n" + "=" * 60)
    print(f"VALIDATING: {name}")
    print("=" * 60)

    if not file.exists():
        print("FAIL: File does not exist")
        return False

    df = pd.read_parquet(file)

    passed = True

    if len(df) == 0:
        print("FAIL: Table is empty")
        passed = False
    else:
        print(f"PASS: Rows = {len(df):,}")

    missing_columns = [
        column
        for column in config["required_columns"]
        if column not in df.columns
    ]

    if missing_columns:
        print(f"FAIL: Missing columns = {missing_columns}")
        passed = False
    else:
        print("PASS: Required columns present")

    if "transport_mode" in df.columns:
        if not validate_transport_modes(df):
            passed = False

    if not validate_route_lengths(df):
        passed = False

    if not validate_geometry(df):
        passed = False

    if not validate_source_systems(name, df):
        passed = False


    duplicates = df.duplicated().sum()

    if duplicates > 0:
        print(f"FAIL: Duplicate rows = {duplicates}")
        passed = False
    else:
        print("PASS: No duplicate rows")

    null_keys = df[config["required_columns"]].isna().sum().sum()

    if null_keys > 0:
        print(f"FAIL: NULL values in required columns = {null_keys}")
        passed = False
    else:
        print("PASS: Required columns contain no NULLs")

    return passed


def main():
    results = []

    for name, config in FILES.items():
        results.append(validate_file(name, config))

    print("\n" + "=" * 60)

    if all(results):
        print("GOLD VALIDATION PASSED")
    else:
        print("GOLD VALIDATION FAILED")

    print("=" * 60)


if __name__ == "__main__":
    main()