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
        #Filter Panels
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Label(
                                        "Subcounty",
                                        className="fw-bold text-muted mb-2"
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
                                lg=8,
                            ),
                            
                            dbc.Col(
                                [
                                    html.Label("Year",className="fw-bold text-muted mb-2"),
                                    dcc.Dropdown(
                                        id="climate-year-dropdown",
                                        options=
                                        [
                                            {
                                                "label": "All Years",
                                                "value": "ALL",
                                            }
                                        ]
                                        +
                                        [
                                            {
                                                "label": str(year),
                                                "value": year,
                                            }
                                            for year in sorted(df["Year"].unique())
                                        ],
                                        value="ALL",
                                        clearable=False,
                                    ),
                                ],
                                lg=4,
                            ),
                        ],
                    ),
                ]
            ),
            className="border-0 shadow-sm mb-4",
            style={"borderRadius": "16px",
            },

        ),

        # Temperature and rainfall
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Average Temperature",className="fw-bold mb-1",),
                                html.P("Monthly average air temperature for the selected subcounty and year.",className="text-muted mb-3",style={"fontSize": "14px"},),
                                dcc.Graph(id="temperature-chart",figure=empty_figure(),config={"displayModeBar": False},style={"height": "430px"},),
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
                                html.H5("Monthly Rainfall",className="fw-bold mb-1",),
                                html.P(
                                    "Monthly accumulated precipitation for the selected subcounty and year.",
                                    className="text-muted mb-3",
                                    style={"fontSize": "14px"},
                                ),

                                dcc.Graph(
                                    id="rainfall-chart",
                                    figure=empty_figure(),
                                    config={
                                        "displayModeBar": False
                                    },
                                    style={"height": "430px"},
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

        # NDVI and Humidity
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Vegetation Index (NDVI)",className="fw-bold mb-1",),
                                html.P(
                                    "Monthly vegetation greenness conditions derived from satellite observations.",
                                    className="text-muted mb-3",
                                    style={"fontSize": "14px"},
                                ),

                                dcc.Graph(
                                    id="ndvi-chart",
                                    figure=empty_figure(),
                                    config={
                                        "displayModeBar": False
                                    },
                                    style={"height": "430px"},
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
                                html.H5("Relative Humidity",className="fw-bold mb-1",),
                                html.P(
                                    "Monthly average atmospheric humidity for the selected subcounty and year.",
                                    className="text-muted mb-3",
                                    style={"fontSize": "14px"},
                                ),

                                dcc.Graph(
                                    id="humidity-chart",
                                    figure=empty_figure(),
                                    config={
                                        "displayModeBar": False
                                    },
                                    style={"height": "430px"},
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
        "padding": "20px",
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

    if selected_year == "ALL":
        for fig in [
            temp_fig,
            rain_fig,
            ndvi_fig,
            humidity_fig,
        ]:
            fig.update_xaxes(
                title="Year",
                tickformat="%Y",
                dtick="M12"
            )
    else:
        figs = [
            temp_fig,
            rain_fig,
            ndvi_fig,
            humidity_fig,
        ]
        month_labels = [
            "Jan", "Feb", "Mar", "Apr",
            "May", "Jun", "Jul", "Aug",
            "Sep", "Oct", "Nov", "Dec"
        ]
        for fig in figs:
            fig.update_xaxes(
                tickmode="array",
                tickvals=list(range(1, 13)),
                ticktext=month_labels
            )

    else:

        dff = df[
            (df["SubCounty"] == selected_subcounty)
            &
            (df["Year"] == selected_year)
        ].copy()

        x_column = "Month"

    temp_fig = px.line(
        dff,
        x=x_column,
        y="Average_Temp",
        markers=True
    )

    rain_fig = px.bar(
        dff,
        x=x_column,
        y="Precipitation"
    )

    ndvi_fig = px.area(
        dff,
        x=x_column,
        y="Vegetation_NDVI"
    )

    humidity_fig = px.line(
        dff,
        x=x_column,
        y="Humidity",
        markers=True
    )

    if selected_year == "ALL":

        for fig in [
            temp_fig,
            rain_fig,
            ndvi_fig,
            humidity_fig,
        ]:
            fig.update_xaxes(
                tickformat="%Y",
                dtick="M12"
            )

    return (
        temp_fig,
        rain_fig,
        ndvi_fig,
        humidity_fig
    )
