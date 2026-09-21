import json
from collections import Counter

from src.utils.raw_files import latest_geojson


def load(dataset):
    file = latest_geojson(dataset)

    with open(file, encoding="utf-8") as f:
        return json.load(f)["features"]


# -------------------------
# Golden Arrow
# -------------------------

routes = load("golden_arrow_routes")
stops = load("golden_arrow_stops")

route_codes = [
    f["properties"].get("Route_No", "").strip()
    for f in routes
]

stop_codes = [
    f["properties"].get("ROUTECODE", "").strip()
    for f in stops
]

route_codes = {x for x in route_codes if x}
stop_codes = {x for x in stop_codes if x}

duplicates = [
    code
    for code, count in Counter(
        f["properties"].get("Route_No")
        for f in routes
    ).items()
    if code and count > 1
]

print("\n=== GOLDEN ARROW ===")
print(f"Route records: {len(routes)}")
print(f"Unique route codes: {len(route_codes)}")
print(f"Stop records: {len(stops)}")
print(f"Unique stop route codes: {len(stop_codes)}")
print(f"Matching codes: {len(route_codes & stop_codes)}")
print(f"Duplicate route codes: {len(duplicates)}")


# -------------------------
# MyCiTi
# -------------------------

myciti_routes = load("myciti_routes")
myciti_stops = load("myciti_stops")

print("\n=== MYCITI ===")
print(f"Route records: {len(myciti_routes)}")
print(f"Stop records: {len(myciti_stops)}")

empty_route_fields = [
    "LNTH",
    "NEW_RT",
    "OD",
    "RT_OD",
    "SRVC_TYPE"
]

for field in empty_route_fields:
    empty = sum(
        not str(f["properties"].get(field, "")).strip()
        for f in myciti_routes
    )
    print(f"{field}: {empty}/{len(myciti_routes)} blank")


# -------------------------
# Taxi
# -------------------------

taxi = load("taxi_routes")

origins = {
    f["properties"].get("ORGN", "").strip()
    for f in taxi
    if f["properties"].get("ORGN")
}

destinations = {
    f["properties"].get("DSTN", "").strip()
    for f in taxi
    if f["properties"].get("DSTN")
}

pairs = {
    (
        f["properties"].get("ORGN"),
        f["properties"].get("DSTN")
    )
    for f in taxi
    if f["properties"].get("ORGN")
    and f["properties"].get("DSTN")
}

print("\n=== TAXI ===")
print(f"Route records: {len(taxi)}")
print(f"Unique origins: {len(origins)}")
print(f"Unique destinations: {len(destinations)}")
print(f"Unique origin → destination pairs: {len(pairs)}")


# -------------------------
# Metrorail
# -------------------------

lines = load("metrorail_lines")
stations = load("metrorail_stations")

station_fields = set()

for feature in stations:
    station_fields.update(feature["properties"].keys())

print("\n=== METRORAIL ===")
print(f"Lines: {len(lines)}")
print(f"Stations: {len(stations)}")
print(f"Station has LINEID: {'LINEID' in station_fields}")

print("\nAnalysis complete.")

