import pandas as pd
import requests

from datetime import datetime
from google.transit import gtfs_realtime_pb2


def get_realtime_data(stops_df, routes_df):

    url = (
        "https://api.entur.io/realtime/v1/"
        "gtfs-rt/trip-updates?datasource=RUT"
    )

    headers = {
        "ET-Client-Name":
        "student-oslo-transit-project"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    # Decode GTFS-Realtime
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)

    rows = []

    collected_at = datetime.now()

    for entity in feed.entity:

        if not entity.HasField("trip_update"):
            continue

        trip_update = entity.trip_update

        trip_id = trip_update.trip.trip_id
        route_id = trip_update.trip.route_id

        for stop_update in trip_update.stop_time_update:

            stop_id = stop_update.stop_id
            stop_sequence = stop_update.stop_sequence

            arrival_delay = None
            departure_delay = None

            if stop_update.HasField("arrival"):

                if stop_update.arrival.HasField("delay"):
                    arrival_delay = (
                        stop_update.arrival.delay
                    )

            if stop_update.HasField("departure"):

                if stop_update.departure.HasField("delay"):
                    departure_delay = (
                        stop_update.departure.delay
                    )

            rows.append({
                "collected_at": collected_at,
                "trip_id": trip_id,
                "route_id": route_id,
                "stop_id": stop_id,
                "stop_sequence": stop_sequence,
                "arrival_delay_seconds":
                    arrival_delay,
                "departure_delay_seconds":
                    departure_delay
            })

    df = pd.DataFrame(rows)
    if df.empty:
        raise ValueError(
            "No trip updates received from Entur."
        )
    
    # Extract line number
    df["line_number"] = (
        df["route_id"]
        .astype(str)
        .str.split(":")
        .str[-1]
    )

    # Convert seconds → minutes
    df["arrival_delay_minutes"] = (
        df["arrival_delay_seconds"] / 60
    )

    # Add stop information
    df = df.merge(
        stops_df,
        on="stop_id",
        how="left"
    )

    df = df.merge(
        routes_df[
            [
                "route_id",
                "transport_type"
            ]
        ],
        on="route_id",
        how="left"
    )
    return df
