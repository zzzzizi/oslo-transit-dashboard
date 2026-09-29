# 🚌 Oslo Transit Dashboard

An interactive dashboard for exploring real-time public transport delays in Oslo, Norway.

The project retrieves GTFS-Realtime data from Entur, processes the data with Python and pandas, combines real-time observations with static stop information, and presents the results through an interactive Streamlit dashboard.

## 📊 Project Overview

The dashboard provides an overview of current public transport performance in the Oslo area.

It allows users to explore:

- Active public transport trips
- Average arrival delays
- Number of observations delayed by more than 5 minutes
- On-time performance
- Average delay by line
- Delay distributions
- Individual public transport lines
- Stop-level delay information
- Stop locations on an interactive map

## 🏗️ Data Pipeline

The project follows this pipeline:

```text
Entur GTFS-Realtime API
        ↓
GTFS-Realtime Protocol Buffers
        ↓
Python
        ↓
pandas
        ↓
Join with static GTFS stop data
        ↓
Streamlit Dashboard
        ↓
Metrics + Charts + Map + Tables
```

## 📡 Data Sources

### Real-time transport data

Real-time trip updates are retrieved from the Entur GTFS-Realtime API for Ruter services.

The feed contains information such as:

- Trip ID
- Line ID
- Stop ID
- Stop sequence
- Arrival delay
- Departure delay

### Static stop data

Static GTFS data is used to translate technical stop identifiers such as:

```text
NSR:Quay:10481
```

into human-readable stop information.

The static dataset provides:

- Stop name
- Latitude
- Longitude
- Stop ID

The real-time and static datasets are joined using `stop_id`.

## 🛠️ Technologies

- Python
- pandas
- Streamlit
- Plotly
- Requests
- GTFS-Realtime
- Protocol Buffers
- Git / GitHub

## 📁 Project Structure

```text
oslo-transit-dashboard/
│
├── data/
│   └── stops.csv
│
├── app.py
├── get_data.py
├── get_stop.py
├── requirements.txt
├── README.md
└── .gitignore
```

### `app.py`

Runs the Streamlit dashboard and processes the data used for visualization.

### `get_data.py`

Retrieves and processes real-time GTFS trip updates from Entur.

### `get_stop.py`

Retrieves static GTFS stop information used to map stop IDs to stop names and geographic coordinates.

### `data/stops.csv`

Contains the stop lookup information used by the dashboard.

## 🔗 Combining Real-Time and Static Data

Real-time GTFS data contains technical stop identifiers.

For example:

```text
Line: RUT:Line:74
Stop: NSR:Quay:10481
Delay: 20 seconds
```

The static GTFS dataset contains information about the same stop:

```text
Stop ID: NSR:Quay:10481
Stop Name: ...
Latitude: ...
Longitude: ...
```

The datasets are combined using a pandas left join:

```python
df = df.merge(
    stops_df,
    on="stop_id",
    how="left"
)
```

This allows the dashboard to display meaningful stop information instead of only technical identifiers.

## 🚀 Running the Project Locally

Clone the repository:

```bash
git clone https://github.com/zzzzizi/oslo-transit-dashboard.git
cd oslo-transit-dashboard
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Start the dashboard:

```bash
streamlit run app.py
```

The application should then open in your browser.

## 📈 Dashboard Features

### Summary Metrics

The dashboard calculates metrics such as:

- Number of active trips
- Average arrival delay
- Observations delayed by more than 5 minutes
- Observations within ±1 minute of schedule

### Line Analysis

Users can select an individual transport line and explore its current delay information.

### Delay Visualization

Plotly charts are used to visualize delay patterns across public transport lines.

### Stop Map

GTFS latitude and longitude information is used to display stop locations geographically.

## 🎯 Project Purpose

This project was created as a portfolio project to demonstrate practical skills in:

- Working with public APIs
- Processing real-time transport data
- Decoding GTFS-Realtime Protocol Buffers
- Data cleaning and transformation
- Combining multiple datasets
- pandas joins and aggregations
- Interactive data visualization
- Dashboard development
- Git-based version control

## 🔮 Future Improvements

Possible future extensions include:

- More advanced map visualizations
- Additional filters for lines and transport modes
- Historical delay analysis
- Improved dashboard design
- Persistent historical data storage
- Cloud deployment
- Additional transport performance indicators

## 📄 Data Attribution

Public transport data is provided by Entur and Ruter. This project is an independent portfolio project and is not an official Entur or Ruter application.
