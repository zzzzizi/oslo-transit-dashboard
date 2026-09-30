import streamlit as st


def filter_line_data(line_df):

    delay_filter = st.radio(
        "Delay status",
        [
            "All",
            "On time",
            "1-5 min delay",
            ">5 min delay"
        ],
        horizontal=True
    )

    if delay_filter == "On time":

        filtered_line_df = line_df[
            line_df[
                "arrival_delay_minutes"
            ].between(-1, 1)
        ].copy()

    elif delay_filter == "1-5 min delay":

        filtered_line_df = line_df[
            (
                line_df["arrival_delay_minutes"] > 1
            )
            & (
                line_df["arrival_delay_minutes"] <= 5
            )
        ].copy()

    elif delay_filter == ">5 min delay":

        filtered_line_df = line_df[
            line_df["arrival_delay_minutes"] > 5
        ].copy()

    else:

        filtered_line_df = line_df.copy()

    if filtered_line_df.empty:

        st.info(
            "No observations match "
            "the selected delay filter."
        )

    return filtered_line_df