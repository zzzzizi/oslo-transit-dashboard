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

# -----------------------------------
# Page settings
# -----------------------------------

st.set_page_config(
    page_title="Oslo Transit Dashboard",
    page_icon="🚌",
    layout="wide"
)


# -----------------------------------
# Load data
# -----------------------------------
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




# -----------------------------------
# Title
# -----------------------------------

st.title("🚌 Oslo Public Transport Dashboard")

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

        # -----------------------------------
        # Map for selected line
        # -----------------------------------

        st.subheader(f"Line {selected_line} — Stop Map")

        map_df = (
            filtered_line_df
            .groupby(
                [
                    "stop_id",
                    "stop_name",
                    "latitude",
                    "longitude"
                ],
                as_index=False
            )
            .agg(
                avg_delay_minutes=(
            "arrival_delay_minutes",
                    "mean"
                ),
                observations=(
            "trip_id",
                    "count"
                )
            )
        )

        # Remove stops without coordinates
        map_df = map_df.dropna(        
            subset=["latitude", "longitude"]
        )

        # Round values for display
        map_df["avg_delay_minutes"] = (
            map_df["avg_delay_minutes"].round(2)
        )

        # Interactive Plotly map
        fig_map = px.scatter_map(
            map_df,
            lat="latitude",
            lon="longitude",
            color="avg_delay_minutes",

            hover_name="stop_name",
            hover_data={
                "avg_delay_minutes": ":.2f",
                "observations": True,
                "latitude": False,
                "longitude": False
            },
            labels={
                "avg_delay_minutes": "Avg delay (min)",
                "observations": "Observations"
            },
            
            center={
                "lat": 59.9139,
                "lon": 10.7522
            },
            zoom=11,
            height=600,
            map_style="carto-positron"
  
        )

        st.plotly_chart(
            fig_map,
            use_container_width=True
        )

        # Average delay by line
        st.subheader("Top 20 Average Delay by Line")

        delay_by_line = (
            df
            .groupby(
                "line_number",
                as_index=False
            )
            ["arrival_delay_minutes"]
            .mean()
            .sort_values(
                "arrival_delay_minutes",
                ascending=False
            )
            .head(20)
        )

        fig = px.bar(
            delay_by_line,
            x="line_number",
            y="arrival_delay_minutes",
            labels={
                "line_number": "Line",
                "arrival_delay_minutes":
                    "Average delay (minutes)"
            }
        )

        fig.update_xaxes(
        type="category"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


        # Top delayed stops
        st.subheader("Top 30 Stops by Average Delay")

        delay_by_stop = (
            df
            .dropna(
                subset=[
                    "stop_name",
                    "latitude",
                    "longitude",
                    "arrival_delay_minutes"
                ]
            )
            .groupby(
                [
                    "stop_name",
                    "latitude",
                    "longitude",
                ],
                as_index=False
            )
            .agg(
                avg_delay_minutes=(
                    "arrival_delay_minutes",
                    "mean"
                ),
                observations=(
                    "trip_id",
                    "count"
                )
            )
            .sort_values(
                "avg_delay_minutes",
                ascending=False
            )
            .head(30)
        )

        chart_col, map_col = st.columns(2)

        with chart_col:
            fig_stops = px.bar(
                delay_by_stop,
                x="stop_name",
                y="avg_delay_minutes",
                labels={
                    "stop_name": "Stop",
                    "avg_delay_minutes":
                        "Average delay (minutes)"
                }
            )
            fig_stops.update_xaxes(
                type="category"
            )

            st.plotly_chart(
                fig_stops,
                use_container_width=True
            )

            with map_col:

                fig_stops_map = px.scatter_map(
                    delay_by_stop,
                    lat="latitude",
                    lon="longitude",
                    color="avg_delay_minutes",
                    hover_name="stop_name",
                    hover_data={
                        "avg_delay_minutes": ":.2f",
                        "observations": True,
                        "latitude": False,
                        "longitude": False
                    },
                    labels={
                        "avg_delay_minutes":
                           "Avg delay (min)",
                        "observations":
                            "Observations"
                   },
                    center={
                        "lat": 59.9139,
                        "lon": 10.7522
                    },
                    zoom=9,
                    height=500,
                    map_style="carto-positron"
                )

                fig_stops_map.update_layout(
                    margin={
                        "r": 0,
                        "t": 0,
                        "l": 0,
                        "b": 0
                   }
                )

                st.plotly_chart(
                    fig_stops_map,
                    use_container_width=True
                )

        # Delay distribution
        st.subheader("Delay Distribution")

        fig2 = px.histogram(
            df.dropna(
                subset=["arrival_delay_minutes"]
            ),
            x="arrival_delay_minutes",
            nbins=40,
            labels={
                "arrival_delay_minutes": "Delay (minutes)"
            }
        )

        st.plotly_chart(
           fig2,
            use_container_width=True
        )

        st.subheader(
            f"Current Observations — Line {selected_line}"
        )

        display_df = filtered_line_df[
            [
                "stop_name",
                "arrival_delay_seconds",
                "arrival_delay_minutes"
            ]
        ].copy()


        display_df["arrival_delay_minutes"] = (
            display_df[
                "arrival_delay_minutes"
           ].round(2)
        )


        display_df = display_df.rename(
            columns={
                "stop_name": "Stop",
                "arrival_delay_seconds":
                    "Delay (seconds)",
                "arrival_delay_minutes":
                    "Delay (minutes)"
            }
        )


        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
           )




    except Exception as e:
        st.error(
            f"Could not retrieve Entur data: {e}"
        )
        raise
        

live_dashboard()



