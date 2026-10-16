import streamlit as st
import plotly.express as px

def show_line_map(filtered_line_df):

    if filtered_line_df.empty:
        st.info("No stops to display.")
        return

    map_df = (
        filtered_line_df
        .groupby(
            ["stop_id", "stop_name", "latitude", "longitude"],
            as_index=False
        )
        .agg(
            avg_delay=("arrival_delay_minutes", "mean")
        )
    )

    if map_df.empty:
        st.info("No stop locations available.")
        return

    fig = px.scatter_map(
        map_df,
        lat="latitude",
        lon="longitude",
        hover_name="stop_name",
        color="avg_delay",
        zoom=11,
    
        height=500,
        center={"lat": 59.9139, "lon": 10.7522},
        map_style="carto-positron"
    )

    st.plotly_chart(fig, use_container_width=True)



def show_top_stops_map(df):

    stop_delay = (
        df.dropna(
            subset=[
                "stop_name",
                "latitude",
                "longitude",
                "arrival_delay_minutes"
            ]
        )
        .groupby(
            ["stop_name", "latitude", "longitude"],
            as_index=False
        )
        .agg(
            avg_delay=("arrival_delay_minutes", "mean")
        )
        .sort_values("avg_delay", ascending=False)
        .head(10)
    )

    if stop_delay.empty:
        st.info("No stop locations available.")
        return

    fig = px.scatter_map(
        stop_delay,
        lat="latitude",
        lon="longitude",
        hover_name="stop_name",
        color="avg_delay",
        size="avg_delay",
        size_max=20,
        zoom=10,
        center={"lat": 59.9139, "lon": 10.7522},
        map_style="carto-positron",
        title="Top 10 Delayed Stops",
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )