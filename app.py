import streamlit as st
import pandas as pd
import plotly.express as px
import requests

from pathlib import Path
from datetime import datetime
from google.transit import gtfs_realtime_pb2

from components.filters import (
    filter_line_data
)

from components.metrics import (
    show_main_metrics,
    show_line_metrics,
    show_transport_type_metrics
)
from components.maps import show_line_map, show_top_stops_map

from components.charts import show_top_lines_chart, show_top_stops_chart ,show_delay_distribution

from components.tables import show_observations_table

# Page settings

st.set_page_config(
    page_title="Oslo Transit Dashboard",

    layout="wide"
)

# Load data

STOPS_PATH = (
    Path(__file__).parent
    / "data"
    / "stops.csv"
)

ROUTES_PATH = (
    Path(__file__).parent
    / "data"
    / "routes.csv"
)

@st.cache_data
def load_stops():
    return pd.read_csv(STOPS_PATH)

@st.cache_data
def load_routes():
    return pd.read_csv(ROUTES_PATH)

routes_df = load_routes()
stops_df = load_stops()

def get_realtime_data():

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

# Title

st.title("Oslo Public Transport Dashboard")

st.caption(
    "Real-time public transport data from Entur / Ruter"
)


@st.fragment(run_every="60s")
def live_dashboard():

    try:
        df = get_realtime_data()

        updated_time = datetime.now().strftime(
        "%H:%M:%S"
        )

        st.caption(
        f"Last refreshed: {updated_time}"
        )

        show_main_metrics(df)

        show_transport_type_metrics(df)

        # Line filter
        st.divider()

        lines = sorted(
            df["line_number"]
            .dropna()
            .unique()
        )

        selected_line = st.selectbox(
            "Select line",
            lines
        )
        
        line_df = df[
            df["line_number"] == selected_line
        ].copy()

        filtered_line_df = filter_line_data(
            line_df
        )

        show_line_metrics(
            filtered_line_df,
            selected_line
        )

        # Map for selected line
 
        st.subheader(f"Line {selected_line} — Stop Map")

        show_line_map(filtered_line_df)

        st.subheader("Top 20 Lines by Average Delay")

        show_top_lines_chart(df)
      

        # Top delayed stops
        st.subheader("Top 10 Stops by Average Delay")

        chart_col, map_col = st.columns(2)

        with chart_col:
            show_top_stops_chart(df)

        with map_col:
            show_top_stops_map(df)  

        # Delay distribution
        st.subheader("Delay Distribution")
        show_delay_distribution(df)

        show_observations_table(filtered_line_df, selected_line)

    except Exception as e:
        st.error(
            f"Could not retrieve Entur data: {e}"
        )
        raise
        

live_dashboard()



