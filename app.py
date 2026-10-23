
"""Interactive SpaceX Falcon 9 landing-outcomes dashboard.

Run locally with: python app.py
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, dcc, html

DATA_PATH = Path(__file__).resolve().parent / "dataset_part_2.csv"

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Missing {DATA_PATH.name}. Keep it in the same folder as app.py."
    )

df = pd.read_csv(DATA_PATH)

required_columns = {"LaunchSite", "PayloadMass", "Class"}
missing = required_columns.difference(df.columns)

if missing:
    raise ValueError(f"Dataset is missing columns: {sorted(missing)}")

df["LaunchSite"] = df["LaunchSite"].fillna("Unknown")
df["Class"] = pd.to_numeric(df["Class"], errors="coerce")
df["PayloadMass"] = pd.to_numeric(df["PayloadMass"], errors="coerce")

# Keep records with known landing outcomes for accurate KPI calculations.
df = df[df["Class"].isin([0, 1])].copy()
df["Class"] = df["Class"].astype(int)

df["Landing outcome"] = df["Class"].map({
    1: "Successful landing",
    0: "Unsuccessful landing",
})

if df.empty:
    raise ValueError("No valid landing outcomes (Class 0 or 1) were found.")

min_payload = float(df["PayloadMass"].min()) if df["PayloadMass"].notna().any() else 0
max_payload = float(df["PayloadMass"].max()) if df["PayloadMass"].notna().any() else 0

if min_payload == max_payload:
    max_payload = min_payload + 500

launch_sites = sorted(df["LaunchSite"].unique())

site_options = [
    {"label": "All launch sites", "value": "All sites"}
] + [
    {"label": site, "value": site} for site in launch_sites
]

app = Dash(__name__)
server = app.server

CARD_STYLE = {
    "padding": "18px",
    "border": "1px solid #d9e2ec",
    "borderRadius": "12px",
    "backgroundColor": "white",
    "flex": "1",
    "minWidth": "150px",
}

def kpi_card(label, value, card_id):
    return html.Div(
        [
            html.P(label, style={"margin": "0", "color": "#526579"}),
            html.H2(value, id=card_id, style={"margin": "8px 0 0"}),
        ],
        style=CARD_STYLE,
    )


app.layout = html.Main(
    [
        html.H1("SpaceX Falcon 9 Launch Outcomes"),
        html.P(
            "Explore recorded first-stage landing outcomes by launch site "
            "and payload mass. This dashboard describes historical data; "
            "it does not predict the safety of future launches."
        ),

        html.Div(
            [
                kpi_card("Launch records", "—", "kpi-total"),
                kpi_card("Successful landings", "—", "kpi-success"),
                kpi_card("Unsuccessful landings", "—", "kpi-failure"),
                kpi_card("Landing success rate", "—", "kpi-rate"),
            ],
            style={
                "display": "flex",
                "flexWrap": "wrap",
                "gap": "12px",
                "margin": "24px 0",
            },
        ),

        html.Div(
            [
                html.Div(
                    [
                        html.Label("Launch site"),
                        dcc.Dropdown(
                            id="site-dropdown",
                            options=site_options,
                            value="All sites",
                            clearable=False,
                        ),
                    ],
                    style={"flex": "1", "minWidth": "220px"},
                ),
                html.Div(
                    [
                        html.Label("Payload mass range (kg)"),
                        dcc.RangeSlider(
                            id="payload-slider",
                            min=int(min_payload // 500 * 500),
                            max=int(max_payload // 500 + 1) * 500,
                            step=500,
                            value=[min_payload, max_payload],
                            marks=None,
                            tooltip={
                                "placement": "bottom",
                                "always_visible": True,
                            },
                        ),
                    ],
                    style={"flex": "2", "minWidth": "280px"},
                ),
            ],
            style={
                "display": "flex",
                "flexWrap": "wrap",
                "gap": "28px",
                "marginBottom": "28px",
            },
        ),

        html.Div(
            [
                dcc.Graph(id="landing-outcome-chart"),
                dcc.Graph(id="payload-outcome-chart"),
                dcc.Graph(id="site-success-chart"),
            ],
        ),

        html.P(
            "Source: dataset_part_2.csv in this repository. "
            "Class = 1 indicates a successful landing; Class = 0 indicates "
            "an unsuccessful landing. Percentages describe the filtered records."
        ),
    ],
    style={
        "maxWidth": "1250px",
        "margin": "0 auto",
        "padding": "24px",
        "fontFamily": "Arial, sans-serif",
        "backgroundColor": "#f5f8fc",
        "minHeight": "100vh",
    },
)


@app.callback(
    Output("kpi-total", "children"),
    Output("kpi-success", "children"),
    Output("kpi-failure", "children"),
    Output("kpi-rate", "children"),
    Output("landing-outcome-chart", "figure"),
    Output("payload-outcome-chart", "figure"),
    Output("site-success-chart", "figure"),
    Input("site-dropdown", "value"),
    Input("payload-slider", "value"),
)
def update_dashboard(selected_site, payload_range):
    low, high = payload_range

    filtered = df[
        df["PayloadMass"].between(low, high, inclusive="both")
    ].copy()

    if selected_site != "All sites":
        filtered = filtered[filtered["LaunchSite"] == selected_site]

    if filtered.empty:
        empty = px.scatter(title="No records match these filters")
        return "0", "0", "0", "N/A", empty, empty, empty

    total = len(filtered)
    successes = int((filtered["Class"] == 1).sum())
    failures = int((filtered["Class"] == 0).sum())
    success_rate = successes / total * 100

    counts = (
        filtered["Landing outcome"]
        .value_counts()
        .rename_axis("Landing outcome")
        .reset_index(name="Launches")
    )

    outcome_fig = px.pie(
        counts,
        names="Landing outcome",
        values="Launches",
        hole=0.4,
        title="Landing outcome distribution",
    )

    payload_data = filtered.dropna(subset=["PayloadMass"])

    payload_fig = px.strip(
        payload_data,
        x="PayloadMass",
        y="Landing outcome",
        color="Landing outcome",
        hover_data=[
            col for col in ["FlightNumber", "Date", "Orbit", "BoosterVersion"]
            if col in payload_data.columns
        ],
        title="Payload mass by landing outcome",
        labels={"PayloadMass": "Payload mass (kg)"},
    )

    site_summary = (
        filtered.groupby("LaunchSite")
        .agg(
            Launches=("Class", "size"),
            Successful=("Class", "sum"),
        )
        .reset_index()
    )
    site_summary["Success rate (%)"] = (
        site_summary["Successful"] / site_summary["Launches"] * 100
    )

    site_fig = px.bar(
        site_summary,
        x="LaunchSite",
        y="Success rate (%)",
        hover_data=["Launches", "Successful"],
        range_y=[0, 100],
        title="Landing success rate by launch site",
        labels={
            "LaunchSite": "Launch site",
            "Success rate (%)": "Success rate (%)",
        },
    )

    return (
        f"{total:,}",
        f"{successes:,}",
        f"{failures:,}",
        f"{success_rate:.1f}%",
        outcome_fig,
        payload_fig,
        site_fig,
    )


if __name__ == "__main__":
    app.run(debug=False)
