# Oslo Transit Dashboard

A real-time dashboard for exploring public transport delays in Oslo, built with Python, pandas, Plotly, and Streamlit.

## About the Project

I built this project to work with real-world transport data and make it easier to understand how public transport is performing in Oslo.

The dashboard uses live GTFS-Realtime data from Entur and combines it with static transport information to show delays across different lines and stops. Users can explore current delays, compare transport lines, and view stop locations on an interactive map.

The project gave me practical experience in working with APIs, processing real-time data, and turning raw data into useful visualizations.

## Features

- **Real-time monitoring:** View active trips, average delays, and on-time performance.
- **Line analysis:** Compare delays across transport lines and explore individual routes.
- **Delay visualization:** Understand delay patterns through interactive charts.
- **Stop-level information:** Explore delays and stop locations on a map.
- **Interactive filters:** Focus on specific lines and transport modes.

## Tech Stack

- **Python & pandas:** Data processing, cleaning, and analysis
- **Streamlit:** Interactive dashboard development
- **Plotly:** Data visualization
- **Requests:** API integration
- **GTFS-Realtime & Protocol Buffers:** Real-time transport data
- **GitHub Actions:** Automated code checks

## How It Works

The dashboard retrieves real-time trip updates from Entur's GTFS-Realtime feed for Ruter services.

The raw data is decoded and processed using Python and pandas. It is then combined with static GTFS data to connect stop IDs with stop names and geographic coordinates.

The processed data is used to calculate delay metrics and create interactive charts, maps, and tables in Streamlit.

## Run Locally

Clone the repository:

```bash
git clone https://github.com/zzzzizi/oslo-transit-dashboard.git
cd oslo-transit-dashboard
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the dashboard:

```bash
streamlit run app.py
```

## What I Learned

This project helped me improve my skills in working with public APIs, handling real-time data, joining datasets, and building interactive applications.

I also gained more experience in organizing Python code into reusable components and using GitHub for version control and automated checks.

## Future Improvements

I plan to extend the project by storing historical delay data, analyzing transport reliability over time, and improving the dashboard's visualizations.

## Data Sources

Transport data is provided by [Entur](https://entur.no/) and [Ruter](https://ruter.no/).

This is an independent personal project and is not affiliated with either organization.
