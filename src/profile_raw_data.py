import json
from collections import Counter
from pathlib import Path

RAW_DIR = Path("data/raw")
REPORT_DIR = Path("data/profiling")
REPORT_DIR.mkdir(parents=True, exist_ok=True)

REPORT_FILE = REPORT_DIR / "transport_data_profile.md"


def is_blank(value):
    return value is None or (
        isinstance(value, str) and not value.strip()
    )


def value_type(value):
    if value is None:
        return "null"

    if isinstance(value, bool):
        return "boolean"

    if isinstance(value, int):
        return "integer"

    if isinstance(value, float):
        return "float"

    return "string"


def load_features(path):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data.get("features", [])


def profile_dataset(path):
    features = load_features(path)

    fields = sorted({
        key
        for feature in features
        for key in feature.get("properties", {})
    })

    geometry_counts = Counter()
    missing_geometry = 0

    for feature in features:
        geometry = feature.get("geometry")

        if geometry is None:
            missing_geometry += 1
        else:
            geometry_counts[geometry.get("type", "UNKNOWN")] += 1

    field_stats = {}

    for field in fields:

        values = [
            feature.get("properties", {}).get(field)
            for feature in features
        ]

        non_blank = [
            value
            for value in values
            if not is_blank(value)
        ]

        unique_values = {
            repr(value)
            for value in non_blank
        }

        types = Counter(
            value_type(value)
            for value in non_blank
        )

        samples = []

        for value in non_blank:

            if repr(value) not in {
                repr(sample) for sample in samples
            }:
                samples.append(value)

            if len(samples) >= 5:
                break

        field_stats[field] = {
            "blank": len(values) - len(non_blank),
            "unique": len(unique_values),
            "types": dict(types),
            "samples": samples,
        }

    return {
        "file": str(path),
        "records": len(features),
        "fields": fields,
        "geometry": dict(geometry_counts),
        "missing_geometry": missing_geometry,
        "field_stats": field_stats,
    }


def get_unique_values(path, field):
    features = load_features(path)

    values = set()

    for feature in features:

        value = feature.get("properties", {}).get(field)

        if not is_blank(value):
            values.add(str(value).strip())

    return values


def check_golden_arrow(paths):

    routes = paths.get("golden_arrow_routes")
    stops = paths.get("golden_arrow_stops")

    if not routes or not stops:
        return []

    route_codes = get_unique_values(
        routes,
        "Route_No"
    )

    stop_route_codes = get_unique_values(
        stops,
        "ROUTECODE"
    )

    matched = route_codes & stop_route_codes

    orphan_stop_codes = (
        stop_route_codes - route_codes
    )

    routes_without_stops = (
        route_codes - stop_route_codes
    )

    return [
        "### Golden Arrow Route → Stop",
        "",
        f"- Unique route codes: **{len(route_codes):,}**",
        f"- Unique stop route codes: **{len(stop_route_codes):,}**",
        f"- Matching route codes: **{len(matched):,}**",
        f"- Stop codes without matching route: **{len(orphan_stop_codes):,}**",
        f"- Routes without matching stop code: **{len(routes_without_stops):,}**",
        "",
    ]


def check_taxi(paths):

    taxi = paths.get("taxi_routes")

    if not taxi:
        return []

    features = load_features(taxi)

    origins = set()
    destinations = set()
    route_pairs = Counter()

    for feature in features:

        properties = feature.get(
            "properties",
            {}
        )

        origin = properties.get("ORGN")
        destination = properties.get("DSTN")

        if not is_blank(origin):
            origin = str(origin).strip()
            origins.add(origin)

        if not is_blank(destination):
            destination = str(destination).strip()
            destinations.add(destination)

        if not is_blank(origin) and not is_blank(destination):

            pair = (
                str(origin).strip(),
                str(destination).strip()
            )

            route_pairs[pair] += 1

    duplicate_pairs = sum(
        1
        for count in route_pairs.values()
        if count > 1
    )

    return [
        "### Taxi Routes",
        "",
        f"- Unique origins: **{len(origins):,}**",
        f"- Unique destinations: **{len(destinations):,}**",
        f"- Unique origin → destination pairs: **{len(route_pairs):,}**",
        f"- Duplicate origin → destination pairs: **{duplicate_pairs:,}**",
        "",
    ]


def check_metrorail(paths):

    lines = paths.get("metrorail_lines")
    stations = paths.get("metrorail_stations")

    output = [
        "### Metrorail",
        ""
    ]

    if lines:

        line_ids = get_unique_values(
            lines,
            "LINEID"
        )

        output.append(
            f"- Unique railway line IDs: **{len(line_ids):,}**"
        )

    if stations:

        station_ids = get_unique_values(
            stations,
            "StationID"
        )

        output.append(
            f"- Unique station IDs: **{len(station_ids):,}**"
        )

        station_fields = profile_dataset(
            stations
        )["fields"]

        if "LINEID" not in station_fields:

            output.append(
                "- ⚠️ Stations do **not** contain a `LINEID` field."
            )

            output.append(
                "- A station → line relationship should not be invented."
            )

    output.append("")

    return output


def build_report():

    files = sorted(
        RAW_DIR.rglob("*.geojson")
    )

    if not files:

        print(
            f"No GeoJSON files found in {RAW_DIR}"
        )

        return

    print(
        f"Found {len(files)} GeoJSON files."
    )

    paths = {
        path.parent.name: path
        for path in files
    }

    profiles = []

    for path in files:

        print(
            f"Profiling {path}..."
        )

        try:

            profiles.append(
                profile_dataset(path)
            )

        except Exception as error:

            print(
                f"ERROR: {error}"
            )

    report = []

    report.append(
        "# Cape Town Public Transport"
    )

    report.append(
        "# Raw Data Profiling Report"
    )

    report.append("")

    report.append(
        "Generated automatically from `data/raw/`."
    )

    report.append("")

    # --------------------------------------------------
    # Dataset overview
    # --------------------------------------------------

    report.append(
        "## Dataset Overview"
    )

    report.append("")

    report.append(
        "| Dataset | Records | Geometry | Fields |"
    )

    report.append(
        "|---|---:|---|---:|"
    )

    for profile in profiles:

        geometry = ", ".join(
            f"{key}: {value:,}"
            for key, value
            in profile["geometry"].items()
        )

        report.append(
            f"| `{Path(profile['file']).parent.name}` "
            f"| {profile['records']:,} "
            f"| {geometry} "
            f"| {len(profile['fields'])} |"
        )

    report.append("")

    # --------------------------------------------------
    # Detailed profiling
    # --------------------------------------------------

    report.append(
        "## Dataset Details"
    )

    report.append("")

    for profile in profiles:

        dataset = Path(
            profile["file"]
        ).parent.name

        report.append(
            f"## {dataset}"
        )

        report.append("")

        report.append(
            f"Records: **{profile['records']:,}**"
        )

        report.append("")

        report.append(
            "### Geometry"
        )

        report.append("")

        for geometry, count in profile[
            "geometry"
        ].items():

            report.append(
                f"- {geometry}: **{count:,}**"
            )

        report.append(
            f"- Missing geometry: **"
            f"{profile['missing_geometry']:,}**"
        )

        report.append("")

        report.append(
            "### Fields"
        )

        report.append("")

        report.append(
            "| Field | Blank | Unique | Types | Samples |"
        )

        report.append(
            "|---|---:|---:|---|---|"
        )

        for field in profile["fields"]:

            stats = profile[
                "field_stats"
            ][field]

            types = ", ".join(
                f"{key}:{value}"
                for key, value
                in stats["types"].items()
            )

            samples = "; ".join(
                repr(value)
                for value in stats["samples"]
            )

            report.append(
                f"| `{field}` "
                f"| {stats['blank']:,} "
                f"| {stats['unique']:,} "
                f"| {types} "
                f"| {samples} |"
            )

        report.append("")

    # --------------------------------------------------
    # Relationship analysis
    # --------------------------------------------------

    report.append(
        "## Relationship Analysis"
    )

    report.append("")

    report.extend(
        check_golden_arrow(paths)
    )

    report.extend(
        check_taxi(paths)
    )

    report.extend(
        check_metrorail(paths)
    )

    # --------------------------------------------------
    # Engineering observations
    # --------------------------------------------------

    report.append(
        "## Engineering Observations"
    )

    report.append("")

    report.append(
        "1. Raw data should remain unchanged."
    )

    report.append(
        "2. Source-specific fields should be "
        "standardized in the Silver layer."
    )

    report.append(
        "3. Relationships should only be created "
        "when supported by source data or a documented "
        "spatial derivation."
    )

    report.append(
        "4. Taxi data currently represents routes "
        "with origin and destination fields; no "
        "separate taxi-stop dataset was extracted."
    )

    report.append(
        "5. Metrorail stations do not expose an obvious "
        "`LINEID` relationship."
    )

    report.append("")

    REPORT_FILE.write_text(
        "\n".join(report),
        encoding="utf-8"
    )

    print()
    print(
        f"Report created: {REPORT_FILE}"
    )


if __name__ == "__main__":
    build_report()