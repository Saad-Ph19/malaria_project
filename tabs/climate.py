from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import glob

#Load the data
files = glob.glob("climate_data/*.xlsx")
df_list = [pd.read_excel(f) for f in files]
climate_df = pd.concat(df_list, ignore_index=True)

# Create Date column
climate_df["Date"] = pd.to_datetime(
    climate_df["Year"].astype(int).astype(str)
    + "-"
    + climate_df["Month"].astype(int).astype(str)
    + "-01"
)

# figures
temp_fig = px.line(
    climate_df.groupby("Date")["Average_Temp"]
    .mean()
    .reset_index(),
    x="Date",
    y="Average_Temp",
    title="Average Temperature"
)

temp_fig.update_layout(
    template="plotly_white",
    height=350
)

rain_fig = px.bar(
    climate_df.groupby("Date")["Precipitation"]
    .mean()
    .reset_index(),
    x="Date",
    y="Precipitation",
    title="Precipitation"
)

rain_fig.update_layout(
    template="plotly_white",
    height=350
)

humidity_fig = px.line(
    climate_df.groupby("Date")["Humidity"]
    .mean()
    .reset_index(),
    x="Date",
    y="Humidity",
    title="Humidity"
)

humidity_fig.update_layout(
    template="plotly_white",
    height=350
)

ndvi_fig = px.line(
    climate_df.groupby("Date")["Vegetation_NDVI"]
    .mean()
    .reset_index(),
    x="Date",
    y="Vegetation_NDVI",
    title="Vegetation NDVI"
)

ndvi_fig.update_layout(
    template="plotly_white",
    height=350
)

# summary
avg_temp = round(climate_df["Average_Temp"].mean(), 1)
avg_rain = round(climate_df["Precipitation"].mean(), 1)
avg_humidity = round(climate_df["Humidity"].mean(), 1)
avg_ndvi = round(climate_df["Vegetation_NDVI"].mean(), 2)

layout = dbc.Container(
    [
        html.H2(
            "Siaya County Climate Dashboard",
            className="fw-bold mb-4 mt-3"
        ),
        
        dbc.Row(

            [
                dbc.Col(
                    [
                        html.Label(
                            "SubCounty",
                            className="fw-bold"
                        ),
                        dcc.Dropdown(
                            id="subcounty-dropdown",
                            options=[
                                {
                                    "label": i,
                                    "value": i
                                }
                                for i in sorted(
                                    climate_df["SubCounty"].unique()
                                )
                            ],
                            value=None,
                            placeholder="All SubCounties"
                        ),

                    ],

                    md=6

                ),

                dbc.Col(
                    [
                        html.Label(
                            "Year",
                            className="fw-bold"
                        ),
                        dcc.Dropdown(
                            id="year-dropdown",
                            options=[
                                {
                                    "label": str(i),
                                    "value": i
                                }
                                for i in sorted(
                                    climate_df["Year"].unique()
                                )
                            ],
                            value=None,
                            placeholder="All Years"
                        ),

                    ],

                    md=6

                ),

            ],

            className="mb-4"

        ),

        dbc.Row(

            [

                dbc.Col(

                    dbc.Card(

                        dbc.CardBody(
                            [
                                html.H6("Avg Temperature"),
                                html.H3(
                                    f"{avg_temp} °C",
                                    className="text-danger"
                                )
                            ]
                        )

                    ),

                    md=3

                ),

                dbc.Col(

                    dbc.Card(

                        dbc.CardBody(
                            [
                                html.H6("Avg Rainfall"),
                                html.H3(
                                    f"{avg_rain} mm",
                                    className="text-primary"
                                )
                            ]
                        )

                    ),

                    md=3

                ),

                dbc.Col(

                    dbc.Card(

                        dbc.CardBody(
                            [
                                html.H6("Avg Humidity"),
                                html.H3(
                                    f"{avg_humidity} %",
                                    className="text-info"
                                )
                            ]
                        )

                    ),
                    md=3
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H6("Avg NDVI"),
                                html.H3(
                                    f"{avg_ndvi}",
                                    className="text-success"
                                )
                            ]
                        )
                    ),
                    md=3
                ),
            ],
            className="mb-4"
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id="temp-graph",
                        figure=temp_fig
                    ),
                    lg=6
                ),
                dbc.Col(
                    dcc.Graph(
                        id="rain-graph",
                        figure=rain_fig
                    ),
                    lg=6
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(
                        id="humidity-graph",
                        figure=humidity_fig
                    ),
                    lg=6
                ),
                dbc.Col(
                    dcc.Graph(
                        id="ndvi-graph",
                        figure=ndvi_fig
                    ),
                    lg=6
                ),
            ]
        ),
    ],
    fluid=True
)
