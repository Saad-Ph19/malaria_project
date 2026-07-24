from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv("climate_data/climate_data.csv")

# Create date column
df["Date"] = pd.to_datetime(
    dict(
        year=df["Year"],
        month=df["Month"],
        day=1
    )
)

subcounties = sorted(df["SubCounty"].unique())

# =====================================================
# PAGE LAYOUT
# =====================================================

layout = dbc.Container(

    [

        # -------------------------------------------------
        # SUBCOUNTY DROPDOWN
        # -------------------------------------------------

        html.H4(
            "Climate Dashboard",
            className="fw-bold mb-3"
        ),

        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label(
                            "Select Subcounty",
                            className="fw-bold"
                        ),

                        dcc.Dropdown(
                            id="subcounty-dropdown",
                            options=[
                                {
                                    "label": s,
                                    "value": s
                                }
                                for s in subcounties
                            ],
                            value=subcounties[0],
                            clearable=False,
                        ),
                    ],
                    lg=4,
                ),
            ],
            className="mb-4",
        ),

        html.Hr(),

        # -------------------------------------------------
        # TEMPERATURE + RAINFALL
        # -------------------------------------------------

        dbc.Row(
            [

                dbc.Col(
                    [
                        html.H5(
                            "Average Temperature",
                            className="fw-bold mb-3"
                        ),

                        dcc.Graph(
                            id="temperature-chart",
                            config={
                                "displayModeBar": False
                            }
                        ),
                    ],
                    lg=6,
                ),

                dbc.Col(
                    [
                        html.H5(
                            "Monthly Rainfall",
                            className="fw-bold mb-3"
                        ),

                        dcc.Graph(
                            id="rainfall-chart",
                            config={
                                "displayModeBar": False
                            }
                        ),
                    ],
                    lg=6,
                ),

            ]
        ),

        html.Hr(),

        # -------------------------------------------------
        # NDVI + HUMIDITY
        # -------------------------------------------------

        dbc.Row(
            [

                dbc.Col(
                    [
                        html.H5(
                            "NDVI",
                            className="fw-bold mb-3"
                        ),

                        dcc.Graph(
                            id="ndvi-chart",
                            config={
                                "displayModeBar": False
                            }
                        ),
                    ],
                    lg=6,
                ),

                dbc.Col(
                    [
                        html.H5(
                            "Relative Humidity",
                            className="fw-bold mb-3"
                        ),

                        dcc.Graph(
                            id="humidity-chart",
                            config={
                                "displayModeBar": False
                            }
                        ),
                    ],
                    lg=6,
                ),

            ]
        ),

    ],

    fluid=True,
)

# =====================================================
# CALLBACK
# =====================================================

@callback(
    Output("temperature-chart", "figure"),
    Output("rainfall-chart", "figure"),
    Output("ndvi-chart", "figure"),
    Output("humidity-chart", "figure"),
    Input("subcounty-dropdown", "value"),
)
def update_climate_plots(selected_subcounty):

    dff = df[df["SubCounty"] == selected_subcounty]

    # Temperature
    temp_fig = px.line(
        dff,
        x="Date",
        y="Average_Temp",
        markers=True
    )

    temp_fig.update_layout(
        template="plotly_white",
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        yaxis_title="Temperature (°C)",
        xaxis_title=""
    )

    # Rainfall
    rain_fig = px.bar(
        dff,
        x="Date",
        y="Precipitation",
        color_discrete_sequence=["#1f77b4"]
    )

    rain_fig.update_layout(
        template="plotly_white",
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        yaxis_title="Rainfall (mm)",
        xaxis_title=""
    )

    # NDVI
    ndvi_fig = px.area(
        dff,
        x="Date",
        y="Vegetation_NDVI"
    )

    ndvi_fig.update_traces(
        line_color="green"
    )

    ndvi_fig.update_layout(
        template="plotly_white",
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        yaxis_title="NDVI",
        xaxis_title=""
    )

    # Humidity
    humidity_fig = px.line(
        dff,
        x="Date",
        y="Humidity",
        markers=True
    )

    humidity_fig.update_traces(
        fill="tozeroy"
    )

    humidity_fig.update_layout(
        template="plotly_white",
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        yaxis_title="Humidity (%)",
        xaxis_title=""
    )

    return (
        temp_fig,
        rain_fig,
        ndvi_fig,
        humidity_fig
    )
