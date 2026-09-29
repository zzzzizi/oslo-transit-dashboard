import io
import zipfile
import requests
import pandas as pd
from pathlib import Path


URL = (
    "https://storage.googleapis.com/"
    "marduk-production/outbound/gtfs/"
    "rb_rut-aggregated-gtfs.zip"
)

print("Downloading Ruter GTFS data...")

response = requests.get(URL, timeout=60)
response.raise_for_status()

print("Download complete.")


# Open ZIP directly from memory
with zipfile.ZipFile(io.BytesIO(response.content)) as z:

    print("Files inside GTFS:")
    print(z.namelist())

    # Read stops.txt
    with z.open("stops.txt") as f:
        stops = pd.read_csv(f)


print("\nOriginal columns:")
print(stops.columns.tolist())

print("\nExample stops:")
print(stops.head())

stops = stops[
    [
        "stop_id",
        "stop_name",
        "stop_lat",
        "stop_lon"
    ]
].copy()

stops = stops.rename(
    columns={
        "stop_lat": "latitude",
        "stop_lon": "longitude"
    }
)


DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)

stops.to_csv(
    DATA_DIR / "stops.csv",
    index=False
)

print("\nSaved stops.csv")
print("Number of stops:", len(stops))