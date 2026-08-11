from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import glob
import plotly.graph_objects as go
import plotly.express as px

# DATA
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

# EMPTY FIGURE
def empty_figure():

    fig = go.Figure()

    fig.update_layout(
        template="plotly_white",
        height=350,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),

        xaxis=dict(
            visible=False
        ),

        yaxis=dict(
            visible=False
        ),

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

# LAYOUT
layout = dbc.Container(
    [
        # FILTER PANEL
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [

                            # Subcounty filter
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
                                                    " Sub County",
                                                    ""
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


                            # Year filter
                            dbc.Col(
                                [
                                    html.Label(
                                        "Year",
                                        className="fw-bold text-muted mb-2"
                                    ),

                                    dcc.Dropdown(
                                        id="climate-year-dropdown",

                                        options=[
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

                                            for year in sorted(
                                                df["Year"].unique()
                                            )
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

            style={
                "borderRadius": "16px",
            },
        ),

        # TEMPERATURE AND RAINFALL
        dbc.Row(
            [

                # Temperature
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [

                                html.H5(
                                    "Average Temperature",
                                    className="fw-bold mb-1",
                                ),

                                html.P(
                                    "Monthly average air temperature for the selected subcounty and year.",
                                    className="text-muted mb-3",
                                    style={
                                        "fontSize": "14px"
                                    },
                                ),

                                dcc.Graph(
                                    id="temperature-chart",
                                    figure=empty_figure(),

                                    config={
                                        "displayModeBar": False
                                    },

                                    style={
                                        "height": "430px"
                                    },
                                ),

                            ]
                        ),

                        className="border-0 shadow-sm h-100",
                    ),

                    lg=6,
                ),


                # Rainfall
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [

                                html.H5(
                                    "Monthly Rainfall",
                                    className="fw-bold mb-1",
                                ),

                                html.P(
                                    "Monthly accumulated precipitation for the selected subcounty and year.",
                                    className="text-muted mb-3",
                                    style={
                                        "fontSize": "14px"
                                    },
                                ),

                                dcc.Graph(
                                    id="rainfall-chart",
                                    figure=empty_figure(),

                                    config={
                                        "displayModeBar": False
                                    },

                                    style={
                                        "height": "430px"
                                    },
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

        # NDVI AND HUMIDITY
        dbc.Row(
            [

                # NDVI
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [

                                html.H5(
                                    "Vegetation Index (NDVI)",
                                    className="fw-bold mb-1",
                                ),

                                html.P(
                                    "Monthly vegetation greenness conditions derived from satellite observations.",
                                    className="text-muted mb-3",
                                    style={
                                        "fontSize": "14px"
                                    },
                                ),

                                dcc.Graph(
                                    id="ndvi-chart",
                                    figure=empty_figure(),

                                    config={
                                        "displayModeBar": False
                                    },

                                    style={
                                        "height": "430px"
                                    },
                                ),

                            ]
                        ),

                        className="border-0 shadow-sm h-100",
                    ),

                    lg=6,
                ),


                # Humidity
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [

                                html.H5(
                                    "Relative Humidity",
                                    className="fw-bold mb-1",
                                ),

                                html.P(
                                    "Monthly average atmospheric humidity for the selected subcounty and year.",
                                    className="text-muted mb-3",
                                    style={
                                        "fontSize": "14px"
                                    },
                                ),

                                dcc.Graph(
                                    id="humidity-chart",
                                    figure=empty_figure(),

                                    config={
                                        "displayModeBar": False
                                    },

                                    style={
                                        "height": "430px"
                                    },
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

        # DATA SOURCE
        html.Div(
            [

                html.Hr(
                    style={
                        "borderColor": "#cbd5e1",
                    }
                ),

                html.P(
                    [
                        html.Strong("Data source: "),
                        "Google Earth",
                    ],

                    className="text-muted mb-1",

                    style={
                        "fontSize": "20px",
                    },
                ),

            ],

            className="mt-4 mb-3 px-2",
        ),

    ],

    fluid=True,

    style={
        "backgroundColor": "#f8fafc",
        "padding": "20px",
        "minHeight": "100vh",
    },
)

# CALLBACK
@callback(
    Output("temperature-chart", "figure"),
    Output("rainfall-chart", "figure"),
    Output("ndvi-chart", "figure"),
    Output("humidity-chart", "figure"),

    Input("climate-subcounty-dropdown", "value"),
    Input("climate-year-dropdown", "value")
)

def update_climate_charts(
    selected_subcounty,
    selected_year
):

    # FILTER DATA
    if selected_year == "ALL":

        dff = df[
            df["SubCounty"] == selected_subcounty
        ].copy()

        dff = dff.sort_values("Date")

        x_col = "Date"

        x_axis_title = "Year"


    else:

        dff = df[
            (df["SubCounty"] == selected_subcounty)
            &
            (df["Year"] == selected_year)
        ].copy()

        dff = dff.sort_values("Month")

        x_col = "Month"

        x_axis_title = "Month"

    # TEMPERATURE
    temp_fig = px.line(
        dff,
        x=x_col,
        y="Average_Temp",
        markers=(selected_year != "ALL")
    )

    # RAINFALL
    rain_fig = px.bar(
        dff,
        x=x_col,
        y="Precipitation"
    )

    # NDVI
    ndvi_fig = px.area(
        dff,
        x=x_col,
        y="Vegetation_NDVI"
    )

    # HUMIDITY
    humidity_fig = px.line(
        dff,
        x=x_col,
        y="Humidity",
        markers=(selected_year != "ALL")
    )

    # COMMON FIGURE STYLING
    for fig in [
        temp_fig,
        rain_fig,
        ndvi_fig,
        humidity_fig,
    ]:

        fig.update_layout(
            template="plotly_white",

            height=400,

            margin=dict(
                l=65,
                r=20,
                t=20,
                b=60
            ),

            font=dict(
                family="Segoe UI",
                size=13
            ),

            paper_bgcolor="white",
            plot_bgcolor="white",

            xaxis_title=x_axis_title,
        )

        fig.update_xaxes(
            showgrid=False,
            title_font=dict(size=14),
        )

        fig.update_yaxes(
            gridcolor="#e9ecef",
            title_font=dict(size=14),
        )

    # ADD Y-AXIS UNITS
    temp_fig.update_yaxes(
        title_text="Average temperature (°C)"
    )

    rain_fig.update_yaxes(
        title_text="Precipitation (mm)"
    )

    ndvi_fig.update_yaxes(
        title_text="NDVI (unitless)"
    )

    humidity_fig.update_yaxes(
        title_text="Relative humidity (%)"
    )

    # HOVER UNITS
    temp_fig.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Average temperature: %{y:.1f} °C"
            "<extra></extra>"
        )
    )

    rain_fig.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Precipitation: %{y:.1f} mm"
            "<extra></extra>"
        )
    )

    ndvi_fig.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br>"
            "NDVI: %{y:.3f}"
            "<extra></extra>"
        )
    )

    humidity_fig.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Relative humidity: %{y:.1f}%"
            "<extra></extra>"
        )
    )

    # MONTH LABELS
    if selected_year != "ALL":

        month_labels = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec"
        ]

        for fig in [
            temp_fig,
            rain_fig,
            ndvi_fig,
            humidity_fig,
        ]:

            fig.update_xaxes(
                tickmode="array",
                tickvals=list(range(1, 13)),
                ticktext=month_labels,
                title_text="Month",
            )

    # YEAR LABELS
    else:

        for fig in [
            temp_fig,
            rain_fig,
            ndvi_fig,
            humidity_fig,
        ]:

            fig.update_xaxes(
                tickformat="%Y",
                dtick="M12",
                title_text="Year",
            )


    return (
        temp_fig,
        rain_fig,
        ndvi_fig,
        humidity_fig
    )
