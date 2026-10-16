import streamlit as st
import plotly.express as px


def show_top_lines_chart(df):

    line_delay = (
        df.groupby("line_number", as_index=False)
        .agg(
            avg_delay=("arrival_delay_minutes", "mean")
        )
        .sort_values("avg_delay", ascending=False)
        .head(20)
    )

    fig = px.bar(
        line_delay,
        x="line_number",
        y="avg_delay",
        labels={
            "line_number": "Line",
            "avg_delay": "Average Delay (min)"
        }
    )

    fig.update_xaxes(type="category")

    st.plotly_chart(fig, use_container_width=True)




def show_top_stops_chart(df):

    stop_delay = (
        df.groupby("stop_name", as_index=False)
        .agg(
            avg_delay=("arrival_delay_minutes", "mean")
        )
        .sort_values("avg_delay", ascending=False)
        .head(10)
    )

    fig = px.bar(
        stop_delay,
        x="avg_delay",
        y="stop_name",
        orientation="h",
        title="Top 10 Stops by Average Delay",
        labels={
            "avg_delay": "Average Delay (min)",
            "stop_name": "Stop"
        }
    )

    fig.update_yaxes(
        categoryorder="total ascending"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


def show_delay_distribution(df):

    delay_df = df.dropna(
        subset=["arrival_delay_minutes"]
    )

    if delay_df.empty:
        st.info("No delay data available.")
        return

    fig = px.histogram(
        delay_df,
        x="arrival_delay_minutes",
        nbins=30,
        title="Distribution of Arrival Delays",
        labels={
            "arrival_delay_minutes": "Arrival Delay (min)"
        }
    )

    fig.update_layout(
        xaxis_title="Arrival Delay (minutes)",
        yaxis_title="Number of Observations",
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )