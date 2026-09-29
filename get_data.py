import requests
import pandas as pd
from datetime import datetime
from google.transit import gtfs_realtime_pb2


URL = (
    "https://api.entur.io/realtime/v1/"
    "gtfs-rt/trip-updates?datasource=RUT"
)

HEADERS = {
    "ET-Client-Name": "student-oslo-transit-project"
}


# 1. Download data
response = requests.get(
    URL,
    headers=HEADERS,
    timeout=30
)

response.raise_for_status()


# 2. Decode GTFS-Realtime data
feed = gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(response.content)


# 3. Create an empty list
rows = []

collected_at = datetime.now()


# 4. Loop through every trip
for entity in feed.entity:

    if not entity.HasField("trip_update"):
        continue

    trip_update = entity.trip_update

    trip_id = trip_update.trip.trip_id
    route_id = trip_update.trip.route_id

    # 5. Loop through every stop in the trip
    for stop_update in trip_update.stop_time_update:

        stop_id = stop_update.stop_id
        stop_sequence = stop_update.stop_sequence

        arrival_delay = None
        departure_delay = None
        arrival_time = None
        departure_time = None

        # Arrival information
        if stop_update.HasField("arrival"):

            if stop_update.arrival.HasField("delay"):
                arrival_delay = stop_update.arrival.delay

            if stop_update.arrival.HasField("time"):
                arrival_time = stop_update.arrival.time

        # Departure information
        if stop_update.HasField("departure"):

            if stop_update.departure.HasField("delay"):
                departure_delay = stop_update.departure.delay

            if stop_update.departure.HasField("time"):
                departure_time = stop_update.departure.time

        # 6. Save one row
        rows.append({
            "collected_at": collected_at,
            "trip_id": trip_id,
            "route_id": route_id,
            "stop_id": stop_id,
            "stop_sequence": stop_sequence,
            "arrival_delay_seconds": arrival_delay,
            "departure_delay_seconds": departure_delay,
            "arrival_time": arrival_time,
            "departure_time": departure_time
        })


# 7. Convert list → DataFrame
df = pd.DataFrame(rows)


# 8. Convert seconds → minutes
df["arrival_delay_minutes"] = (
    df["arrival_delay_seconds"] / 60
)

df["departure_delay_minutes"] = (
    df["departure_delay_seconds"] / 60
)
df["arrival_datetime"] = pd.to_datetime(
    df["arrival_time"],
    unit="s",
    utc=True
)

df["departure_datetime"] = pd.to_datetime(
    df["departure_time"],
    unit="s",
    utc=True
)
df["arrival_datetime_oslo"] = (
    df["arrival_datetime"]
    .dt.tz_convert("Europe/Oslo")
)

df["departure_datetime_oslo"] = (
    df["departure_datetime"]
    .dt.tz_convert("Europe/Oslo")
)

# Extract line number
df["line_number"] = (
    df["route_id"]
    .str.split(":")
    .str[-1]
)

# Round delay in minutes
df["arrival_delay_minutes"] = (
    df["arrival_delay_seconds"] / 60
).round(2)

# Save data
df.to_csv(
    "data/ruter_realtime.csv",
    index=False
)

print("Data saved successfully!")
print(df.head())# Extract line number
df["line_number"] = (
    df["route_id"]
    .str.split(":")
    .str[-1]
)

# Round delay in minutes
df["arrival_delay_minutes"] = (
    df["arrival_delay_seconds"] / 60
).round(2)

# Save data
df.to_csv(
    "data/ruter_realtime.csv",
    index=False
)

print("Data saved successfully!")
print(df.head())

