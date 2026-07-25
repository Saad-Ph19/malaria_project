from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import glob
import plotly.graph_objects as go
import plotly.express as px

# Data
files = glob.glob("Climate_Data/*.csv")
print(files)

df_list = []

for file in files:
    df_list.append(pd.read_csv(file))

df = pd.concat(df_list, ignore_index=True)

# Create date field
df["Date"] = pd.to_datetime(
    dict(
        year=df["Year"],
        month=df["Month"],
        day=1
    )
)

# Available subcounties
subcounties = sorted(df["SubCounty"].unique())

# Figures
def empty_figure():

    fig = go.Figure()

    fig.update_layout(
        template="plotly_white",
        height=350,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        annotations=[
            dict(
                text="Loading...",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=18)
            )
        ]
    )

    return fig

# layout
layout = dbc.Container(

    [
        dbc.Row(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.Label(
                                "Subcounty:",
                                className="fw-bold mb-0"
                            ),
                            width="auto"
                        ),
                
                        dbc.Col(
                            dcc.Dropdown(
                                id="climate-subcounty-dropdown",
                                options=[
                                    {
                                        "label": s.replace(" Sub County", ""),
                                        "value": s
                                    }
                                    for s in subcounties
                                ],
                                value=subcounties[0],
                                clearable=False,
                            ),
                            width=4
                        )
                    ],
                    className="align-items-center mb-4"
                )
            ],
            className="mb-4",
        ),

        html.Hr(),

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
                            figure=empty_figure(),
                            config={"displayModeBar": False},
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
                            figure=empty_figure(),
                            config={"displayModeBar": False},
                        ),
                    ],
                    lg=6,
                ),
            ]
        ),

        html.Hr(),

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
                            figure=empty_figure(),
                            config={"displayModeBar": False},
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
                            figure=empty_figure(),
                            config={"displayModeBar": False},
                        ),
                    ],
                    lg=6,
                ),
            ]
        ),

    ],

    fluid=True,
)
# Callback
@callback(
    Output("temperature-chart", "figure"),
    Output("rainfall-chart", "figure"),
    Output("ndvi-chart", "figure"),
    Output("humidity-chart", "figure"),
    Input("climate-subcounty-dropdown", "value")
)
def update_climate_charts(selected_subcounty):

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
        humidity_fig,
    )
