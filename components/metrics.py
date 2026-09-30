import streamlit as st


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

                avg_delay = row[
                    "avg_delay_minutes"
                ].iloc[0]

                st.metric(
                    f"{transport_icons[transport]} {transport}",
                    f"{avg_delay:.2f} min"
                )

            else:

                st.metric(
                    f"{transport_icons[transport]} {transport}",
                    "No data"
                )