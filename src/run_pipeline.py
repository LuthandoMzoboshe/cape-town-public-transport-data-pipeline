import subprocess
import sys


STAGES = [
    ("Bronze extraction", "src.extract_transport"),
    ("Raw data profiling", "src.profile_raw_data"),
    ("Relationship analysis", "src.analyze_relationships"),
    ("Golden Arrow Silver", "src.transformations.transform_golden_arrow"),
    ("MyCiTi Silver", "src.transformations.transform_myciti"),
    ("Taxi Silver", "src.transformations.transform_taxi"),
    ("Metrorail Silver", "src.transformations.transform_metrorail"),
    ("Silver validation", "src.validate_silver"),
    ("Gold routes", "src.transformations.transform_transport_routes"),
    ("Gold stops", "src.transformations.transform_transport_stops"),
    ("Gold summary", "src.transformations.transform_transport_summary"),
    ("Gold validation", "src.validate_gold"),
]


def run_stage(name, module):
    print()
    print("=" * 60)
    print(f"RUNNING: {name}")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, "-m", module],
        check=False,
    )

    if result.returncode != 0:
        print()
        print(f"PIPELINE FAILED: {name}")
        sys.exit(result.returncode)


def main():
    print("Cape Town Public Transport Data Pipeline")
    print("=" * 60)

    for name, module in STAGES:
        run_stage(name, module)

    print()
    print("=" * 60)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()
