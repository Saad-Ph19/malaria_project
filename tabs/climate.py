from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import glob
import plotly.graph_objects as go

# Data
files = glob.glob("Climate_Data/*.csv")

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

        html.H3(
            "Climate and Environmental Conditions",
            className="fw-bold mb-4"
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
                    ],
                    lg=4,
                ),
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
