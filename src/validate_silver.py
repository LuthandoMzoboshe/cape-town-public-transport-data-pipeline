from pathlib import Path
import pandas as pd

SILVER = Path("data/processed/golden_arrow")

for file in SILVER.glob("*.parquet"):
    print("\n" + "=" * 60)
    print(f"FILE: {file.name}")
    print("=" * 60)

    df = pd.read_parquet(file)

    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print("\nColumns:")
    for column in df.columns:
        print(f"  - {column}")

    print("\nMissing values:")
    print(df.isna().sum())

    print("\nDuplicate rows:", df.duplicated().sum())

    print("\nSample:")
    print(df.head(3).to_string(index=False))