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

layout = dbc.Container(

    [

        # =====================================================
        # HEADER
        # =====================================================

        html.Div(
            [

                html.H2(
                    "Climate & Environmental Conditions Dashboard",
                    className="fw-bold mb-1",
                    style={"color": "white"},
                ),

                html.P(
                    "Monthly climate indicators across Siaya County subcounties",
                    className="mb-0",
                    style={"color": "#dbeafe"},
                ),

            ],
            className="p-4 rounded-4 mb-4",
            style={
                "background": "linear-gradient(135deg,#0f172a,#2563eb)"
            },
        ),

        # =====================================================
        # FILTER PANEL
        # =====================================================

        dbc.Card(

            dbc.CardBody(

                [

                    dbc.Row(

                        [

                            dbc.Col(

                                [

                                    html.Label(
                                        "Subcounty",
                                        className="fw-bold text-muted mb-2",
                                    ),

                                    dcc.Dropdown(
                                        id="climate-subcounty-dropdown",
                                        options=[
                                            {
                                                "label": s.replace(
                                                    " Sub County", ""
                                                ),
                                                "value": s,
                                            }
                                            for s in subcounties
                                        ],
                                        value=subcounties[0],
                                        clearable=False,
                                    ),

                                ],

                                lg=4,

                            ),

                            dbc.Col(

                                [

                                    html.Label(
                                        "Year",
                                        className="fw-bold text-muted mb-2",
                                    ),

                                    dcc.Dropdown(
                                        id="climate-year-dropdown",
                                        options=[
                                            {
                                                "label": str(year),
                                                "value": year,
                                            }
                                            for year in sorted(
                                                df["Year"].unique()
                                            )
                                        ],
                                        value=max(df["Year"].unique()),
                                        clearable=False,
                                    ),

                                ],

                                lg=2,

                            ),

                            dbc.Col(

                                [

                                    html.Div(
                                        [
                                            html.H6(
                                                "Dashboard Filters",
                                                className="fw-bold mb-1",
                                            ),

                                            html.P(
                                                "Select a subcounty and year to explore climate trends.",
                                                className="text-muted mb-0",
                                            ),
                                        ],
                                        className="pt-3",
                                    )

                                ],

                                lg=6,

                            ),

                        ],

                        className="align-items-end",

                    )

                ]

            ),

            className="border-0 shadow-sm mb-4",
            style={"borderRadius": "16px"},

        ),

        # =====================================================
        # KPI CARDS
        # =====================================================

        dbc.Row(

            [

                dbc.Col(

                    dbc.Card(

                        dbc.CardBody(

                            [

                                html.Div(
                                    "Average Temperature",
                                    className="text-muted",
                                ),

                                html.H3(
                                    "-- °C",
                                    className="fw-bold text-primary mb-0",
                                ),

                            ]

                        ),

                        className="border-0 shadow-sm",

                    ),

                    lg=3,
                    md=6,
                    className="mb-3",

                ),

                dbc.Col(

                    dbc.Card(

                        dbc.CardBody(

                            [

                                html.Div(
                                    "Total Rainfall",
                                    className="text-muted",
                                ),

                                html.H3(
                                    "-- mm",
                                    className="fw-bold text-primary mb-0",
                                ),

                            ]

                        ),

                        className="border-0 shadow-sm",

                    ),

                    lg=3,
                    md=6,
                    className="mb-3",

                ),

                dbc.Col(

                    dbc.Card(

                        dbc.CardBody(

                            [

                                html.Div(
                                    "Mean NDVI",
                                    className="text-muted",
                                ),

                                html.H3(
                                    "--",
                                    className="fw-bold text-primary mb-0",
                                ),

                            ]

                        ),

                        className="border-0 shadow-sm",

                    ),

                    lg=3,
                    md=6,
                    className="mb-3",

                ),

                dbc.Col(

                    dbc.Card(

                        dbc.CardBody(

                            [

                                html.Div(
                                    "Mean Humidity",
                                    className="text-muted",
                                ),

                                html.H3(
                                    "-- %",
                                    className="fw-bold text-primary mb-0",
                                ),

                            ]

                        ),

                        className="border-0 shadow-sm",

                    ),

                    lg=3,
                    md=6,
                    className="mb-3",

                ),

            ],

            className="mb-4",

        ),

        # =====================================================
        # TEMPERATURE
        # =====================================================

        dbc.Row(

            [

                dbc.Col(

                    dbc.Card(

                        dbc.CardBody(

                            [

                                html.H5(
                                    "Average Temperature",
                                    className="fw-bold mb-3",
                                ),

                                dcc.Graph(
                                    id="temperature-chart",
                                    figure=empty_figure(),
                                    config={
                                        "displayModeBar": False
                                    },
                                    style={"height": "420px"},
                                ),

                            ]

                        ),

                        className="border-0 shadow-sm h-100",

                    ),

                    lg=6,

                ),

                dbc.Col(

                    dbc.Card(

                        dbc.CardBody(

                            [

                                html.H5(
                                    "Monthly Rainfall",
                                    className="fw-bold mb-3",
                                ),

                                dcc.Graph(
                                    id="rainfall-chart",
                                    figure=empty_figure(),
                                    config={
                                        "displayModeBar": False
                                    },
                                    style={"height": "420px"},
                                ),

                            ]

                        ),

                        className="border-0 shadow-sm h-100",

                    ),

                    lg=6,

                ),

            ],

            className="mb-4",

        ),

        # =====================================================
        # NDVI + HUMIDITY
        # =====================================================

        dbc.Row(

            [

                dbc.Col(

                    dbc.Card(

                        dbc.CardBody(

                            [

                                html.H5(
                                    "Vegetation Index (NDVI)",
                                    className="fw-bold mb-3",
                                ),

                                dcc.Graph(
                                    id="ndvi-chart",
                                    figure=empty_figure(),
                                    config={
                                        "displayModeBar": False
                                    },
                                    style={"height": "420px"},
                                ),

                            ]

                        ),

                        className="border-0 shadow-sm h-100",

                    ),

                    lg=6,

                ),

                dbc.Col(

                    dbc.Card(

                        dbc.CardBody(

                            [

                                html.H5(
                                    "Relative Humidity",
                                    className="fw-bold mb-3",
                                ),

                                dcc.Graph(
                                    id="humidity-chart",
                                    figure=empty_figure(),
                                    config={
                                        "displayModeBar": False
                                    },
                                    style={"height": "420px"},
                                ),

                            ]

                        ),

                        className="border-0 shadow-sm h-100",

                    ),

                    lg=6,

                ),

            ]

        ),

    ],

    fluid=True,

    style={
        "backgroundColor": "#f8fafc",
        "padding": "25px",
        "minHeight": "100vh",
    },

)
# Callback
@callback(
    Output("temperature-chart", "figure"),
    Output("rainfall-chart", "figure"),
    Output("ndvi-chart", "figure"),
    Output("humidity-chart", "figure"),
    Input("climate-subcounty-dropdown", "value"),
    Input("climate-year-dropdown", "value")
)
def update_climate_charts(selected_subcounty, selected_year):

    dff = df[
        (df["SubCounty"] == selected_subcounty) &
        (df["Year"] == selected_year)
    ]

    temp_fig = px.line(
        dff,
        x="Month",
        y="Average_Temp",
        markers=True
    )

    rain_fig = px.bar(
        dff,
        x="Month",
        y="Precipitation"
    )

    ndvi_fig = px.area(
        dff,
        x="Month",
        y="Vegetation_NDVI"
    )

    humidity_fig = px.line(
        dff,
        x="Month",
        y="Humidity",
        markers=True
    )

    return (
        temp_fig,
        rain_fig,
        ndvi_fig,
        humidity_fig
    )
