
### Interactive Dashboard

The project includes a Python dashboard built with Plotly Dash. It allows users to explore historical Falcon 9 launch outcomes interactively.

**Dashboard features**
- Filter launches by launch site.
- Adjust the payload mass range in kilograms.
- Compare recorded successful and unsuccessful landing outcomes.
- Explore the relationship between payload mass and landing outcome.

The dashboard is intended for exploratory analysis. It describes patterns in historical data rather than predicting the safety or outcome of a future launch.

**Run locally**

```bash
git clone https://github.com/olafisoyetope44-ship-it/Applied-Data-Capstone.git
cd Applied-Data-Capstone
python -m venv .venv
```

Activate the environment:

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Install the dashboard dependencies and start the application:

```bash
python -m pip install -r requirements.txt
python app.py
```

Open the local address displayed in the terminal.

"""
from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

DATA_PATH = Path(__file__).resolve().parent / "dataset_part_2.csv"
if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Could not find {DATA_PATH.name}. Keep it in the same directory as app.py."
    )

df = pd.read_csv(DATA_PATH)
required_columns = {"LaunchSite", "PayloadMass", "Class", "BoosterVersion"}
missing = required_columns.difference(df.columns)
if missing:
    raise ValueError(f"The launch dataset is missing required columns: {sorted(missing)}")

df["Landing outcome"] = df["Class"].map({1: "Successful landing", 0: "Unsuccessful landing"})
df["LaunchSite"] = df["LaunchSite"].fillna("Unknown")
df["BoosterVersion"] = df["BoosterVersion"].fillna("Unknown")
min_payload = float(df["PayloadMass"].min())
max_payload = float(df["PayloadMass"].max())
launch_sites = sorted(df["LaunchSite"].dropna().unique().tolist())
site_options = [{"label": "All launch sites", "value": "All sites"}] + [
    {"label": site, "value": site} for site in launch_sites
]

app = Dash(__name__)
server = app.server

app.layout = html.Main(
    [
        html.H1("SpaceX Falcon 9 Launch Outcomes"),
        html.P(
            "Explore historical first-stage landing outcomes by launch site and payload mass. "
            "This dashboard is descriptive and does not predict the safety of future launches."
        ),
        html.Label("Launch site", htmlFor="site-dropdown"),
        dcc.Dropdown(
            id="site-dropdown",
            options=site_options,
            value="All sites",
            clearable=False,
        ),
        html.Label("Payload mass range (kg)", htmlFor="payload-slider"),
        dcc.RangeSlider(
            id="payload-slider",
            min=int(min_payload // 1000 * 1000),
            max=int((max_payload // 1000 + 1) * 1000),
            step=500,
            value=[min_payload, max_payload],
            marks=None,
            tooltip={"placement": "bottom", "always_visible": True},
        ),
        html.Div(
            [
                dcc.Graph(id="landing-outcome-chart"),
                dcc.Graph(id="payload-outcome-chart"),
            ],
            className="chart-grid",
        ),
        html.Footer(
            "Source: dataset_part_2.csv included in this repository. "
            "Landing outcome is the recorded Class label."
        ),
    ],
    style={"maxWidth": "1150px", "margin": "0 auto", "padding": "24px"},
)


@app.callback(
    Output("landing-outcome-chart", "figure"),
    Output("payload-outcome-chart", "figure"),
    Input("site-dropdown", "value"),
    Input("payload-slider", "value"),
)
def update_charts(selected_site, payload_range):
    low, high = payload_range
    filtered = df[df["PayloadMass"].between(low, high, inclusive="both")].copy()
    if selected_site != "All sites":
        filtered = filtered[filtered["LaunchSite"] == selected_site]

    if filtered.empty:
        empty_fig = px.scatter(title="No launches match these filters")
        return empty_fig, empty_fig

    outcome_counts = (
        filtered.groupby("Landing outcome", dropna=False)
        .size()
        .reset_index(name="Launches")
    )
    pie = px.pie(
        outcome_counts,
        names="Landing outcome",
        values="Launches",
        hole=0.35,
        title="Landing outcomes in the selected records",
    )

    scatter = px.scatter(
        filtered,
        x="PayloadMass",
        y="Class",
        color="Landing outcome",
        symbol="Landing outcome",
        hover_data=["FlightNumber", "Date", "LaunchSite", "Orbit", "BoosterVersion"],
        labels={
            "PayloadMass": "Payload mass (kg)",
            "Class": "Landing success label (1 = success)",
        },
        title="Payload mass and recorded landing outcome",
    )
    scatter.update_yaxes(tickmode="array", tickvals=[0, 1], ticktext=["Unsuccessful", "Successful"])
    scatter.update_layout(legend_title_text="Landing outcome")
    return pie, scatter


if __name__ == "__main__":
    app.run(debug=True)
