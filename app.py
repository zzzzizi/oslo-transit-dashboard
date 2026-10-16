import streamlit as st
import pandas as pd

from pathlib import Path
from datetime import datetime

from services.realtime import get_realtime_data
from components.filters import (
    filter_line_data
)
from components.metrics import (
    show_main_metrics,
    show_line_metrics,
    show_transport_type_metrics
)
from components.maps import show_line_map, show_top_stops_map
from components.charts import (
    show_top_lines_chart, 
    show_top_stops_chart,
    show_delay_distribution
)
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



# Title

st.title("Oslo Public Transport Dashboard")

st.caption(
    "Real-time public transport data from Entur / Ruter"
)


@st.fragment(run_every="60s")
def live_dashboard():

    try:
        df = get_realtime_data(stops_df, routes_df)

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

        show_observations_table(filtered_line_df, selected_line)

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



    except Exception as e:
        st.error(
            f"Could not retrieve Entur data: {e}"
        )
        raise
        

live_dashboard()



