import streamlit as st


def show_observations_table(filtered_line_df, selected_line):

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
        display_df["arrival_delay_minutes"].round(2)
    )

    display_df = display_df.rename(
        columns={
            "stop_name": "Stop",
            "arrival_delay_seconds": "Delay (seconds)",
            "arrival_delay_minutes": "Delay (minutes)"
        }
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )