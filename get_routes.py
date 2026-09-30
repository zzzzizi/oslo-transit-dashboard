import io
import zipfile
import requests
import pandas as pd


URL = (
    "https://storage.googleapis.com/"
    "marduk-production/outbound/gtfs/"
    "rb_norway-aggregated-gtfs.zip"
)

headers = {
    "ET-Client-Name":
        "student-oslo-transit-project"
}


print("Downloading GTFS data...")

response = requests.get(
    URL,
    headers=headers,
    timeout=60
)

response.raise_for_status()


print("Opening GTFS archive...")

with zipfile.ZipFile(
    io.BytesIO(response.content)
) as gtfs_zip:

    routes = pd.read_csv(
        gtfs_zip.open("routes.txt")
    )


print(routes.head())

print(routes.columns)

# Keep only Ruter routes
ruter_routes = routes[
    routes["route_id"]
    .astype(str)
    .str.startswith("RUT:")
].copy()

print("\nRuter routes:")
print(
    ruter_routes[
        [
            "route_id",
            "route_short_name",
            "route_long_name",
            "route_type"
        ]
    ].head(20)
)

print("\nRoute types used by Ruter:")
print(
    ruter_routes["route_type"]
    .value_counts()
)

transport_type_map = {
    401: "Metro",
    702: "Bus",
    704: "Bus",
    705: "Bus",
    712: "Bus",
    902: "Tram",
    1008: "Ferry"
}

ruter_routes["transport_type"] = (
    ruter_routes["route_type"]
    .map(transport_type_map)
    .fillna("Other")
)

print("\nTransport types:")
print(
    ruter_routes[
        [
            "route_short_name",
            "route_type",
            "transport_type"
        ]
    ].head(30)
)

# Save routes lookup table
routes_lookup = ruter_routes[
    [
        "route_id",
        "route_short_name",
        "transport_type"
    ]
].copy()

routes_lookup.to_csv(
    "data/routes.csv",
    index=False
)

print("\nSaved data/routes.csv")