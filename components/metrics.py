import streamlit as st


def show_main_metrics(df):

    total_trips = df["trip_id"].nunique()

    average_delay = (
        df["arrival_delay_minutes"].mean()
    )

    delayed_over_5 = (
        df["arrival_delay_minutes"] > 5
    ).sum()

    on_time = (
        df["arrival_delay_minutes"]
        .between(-1, 1)
    ).sum()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Active Trips",
        f"{total_trips:,}"
    )

    col2.metric(
        "Average Delay",
        f"{average_delay:.1f} min"
    )

    col3.metric(
        "Delayed > 5 min",
        f"{delayed_over_5:,}"
    )

    col4.metric(
        "On Time ±1 min",
        f"{on_time:,}"
    )


def show_line_metrics(
    filtered_line_df,
    selected_line
):

    
    line_avg = (
        filtered_line_df[
            "arrival_delay_minutes"
        ].mean()
    )

    line_max = (
        filtered_line_df[
            "arrival_delay_minutes"
        ].max()
    )


    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Selected Line",
        selected_line
    )

    col2.metric(
        "Average Delay",
        f"{line_avg:.1f} min"
    )

    col3.metric(
        "Maximum Delay",
        f"{line_max:.1f} min"
    )
    # Check whether the filter returned anything
    if filtered_line_df.empty:
        st.info(
            "No observations match the selected delay filter."
        )
    


def show_transport_type_metrics(df):

    st.divider()

    st.caption("BY TRANSPORT TYPE")
    st.subheader("Different ways to move")
    st.caption("Average delay · minutes")

    delay_by_type = (
        df
        .dropna(
            subset=[
                "transport_type",
                "arrival_delay_minutes"
            ]
        )
        .groupby(
            "transport_type",
            as_index=False
        )
        .agg(
            avg_delay_minutes=(
                "arrival_delay_minutes",
                "mean"
            )
        )
    )

    transport_order = [
        "Bus",
        "Metro",
        "Tram",
        "Ferry"
    ]

    transport_icons = {
        "Bus": "🚌",
        "Metro": "🚇",
        "Tram": "🚋",
        "Ferry": "⛴️"
    }

    cols = st.columns(4)

    for col, transport in zip(
        cols,
        transport_order
    ):

        row = delay_by_type[
            delay_by_type["transport_type"]
            == transport
        ]

        with col:

            if not row.empty:

                avg_delay = (
                    row["avg_delay_minutes"]
                    .iloc[0]
                )

                st.metric(
                    f"{transport_icons[transport]} "
                    f"{transport}",
                    f"{avg_delay:.2f} min"
                )

            else:

                st.metric(
                    f"{transport_icons[transport]} "
                    f"{transport}",
                    "No data"
                )