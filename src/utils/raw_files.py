from pathlib import Path


RAW_DIR = Path("data/raw")


def latest_geojson(dataset: str) -> Path:
    folder = RAW_DIR / dataset
    files = sorted(folder.glob("*.geojson"))

    if not files:
        raise FileNotFoundError(
            f"No GeoJSON files found in {folder}"
        )

    return files[-1]
