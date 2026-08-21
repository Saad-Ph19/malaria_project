from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import geopandas as gpd
import glob
import plotly.graph_objects as go
import plotly.express as px
import os
import gdown


#=========================================================
# THEME
PRIMARY = "#274C77"
PRIMARY_DARK = "#1F3B5B"
TEXT = "#1F2937"
TEXT_MUTED = "#6B7280"
BORDER = "#DCE3EA"
PAGE_BG = "#F5F7F9"
CARD_BG = "#FFFFFF"
CARD_STYLE = {
    "backgroundColor": CARD_BG,
    "border": f"1px solid {BORDER}",
    "borderRadius": "10px",
    "boxShadow": "0 2px 8px rgba(15, 23, 42, 0.05)",
}

# =========================================================
# DATA IMPORT 
DRIVE_FOLDER_URL = (
    "https://drive.google.com/drive/folders/"
    "1DeKaLUtbfvK8CHx3ZU5-tNtCuSD9PI5h?usp=sharing"
)

DOWNLOAD_FOLDER = "/tmp/Climate_Data"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
gdown.download_folder(
    url=DRIVE_FOLDER_URL,
    output=DOWNLOAD_FOLDER,
    quiet=False,
    use_cookies=False
)

# Read csv files
files = glob.glob(
    os.path.join(DOWNLOAD_FOLDER, "*.csv")
)

if not files:
    raise ValueError("No CSV files were found in the Google Drive folder.")

df_list = []

for file in files:
    print(f"Reading: {file}")

    df_list.append(
        pd.read_csv(file)
    )

df = pd.concat(
    df_list,
    ignore_index=True
)

# DATA Cleaning
df["Year"] = pd.to_numeric(df["Year"],errors="coerce")
df["Month"] = pd.to_numeric(df["Month"],errors="coerce")

df["Date"] = pd.to_datetime(
    dict(
        year=df["Year"],
        month=df["Month"],
        day=1
    )
)


# Available subcounties
subcounties = sorted(df["SubCounty"].dropna().unique())
years = sorted(df["Year"].dropna().astype(int).unique())

# =========================================================
# Load the siaya subcounty boundaries
subcounty_gdf = gpd.read_file(
    "Boundary_Data/ke_subcounty.shp"
)

# THE subcounties we want
siaya_subcounties = [
    "Alego Usonga Sub County",
    "Bondo Sub County",
    "Gem Sub County",
    "Rarieda Sub County",
    "Ugenya Sub County",
    "Ugunja Sub County",
]

subcounty_gdf = subcounty_gdf[subcounty_gdf["subcounty"].isin(siaya_subcounties)].copy()

# Make sure map coordinates use longitude / latitude
subcounty_gdf = subcounty_gdf.to_crs(epsg=4326)

# Short name
subcounty_gdf["Display_Name"] = (subcounty_gdf["subcounty"].str.replace(" Sub County","",regex=False).str.strip())


# =========================================================
# EMPTY FIGURE FOR NOW
def empty_figure():
    fig = go.Figure()
    fig.update_layout(
        template="plotly_white",
        height=350,
        margin=dict(l=20,r=20,t=20,b=20),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        annotations=[
            dict(
                text="Loading...",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=18,color=TEXT_MUTED)
            )
        ]
    )
    return fig

# =========================================================
# CLIMATE MAP
def create_climate_map(
    selected_variable="Average_Temp",
    selected_year="ALL"
):

    map_df = df.copy()

    # YEAR FILTER
    if selected_year != "ALL":
        map_df = map_df[map_df["Year"] == int(selected_year)]

    map_summary = (map_df.groupby("SubCounty",as_index=False).agg({selected_variable: "mean"}))

    # Short display name
    map_summary["Display_Name"] = (map_summary["SubCounty"].str.replace(" Sub County","",regex=False).str.strip())

    # VARIABLE SETTINGS
    variable_settings = {
        "Average_Temp": {
            "title": "Average Temperature",
            "unit": "°C",
            "color_scale": "RdYlBu_r",
        },

        "Precipitation": {
            "title": "Average Precipitation",
            "unit": "mm",
            "color_scale": "Blues",
        },

        "Humidity": {
            "title": "Relative Humidity",
            "unit": "%",
            "color_scale": "Teal",
        },

        "Vegetation_NDVI": {
            "title": "Vegetation Index (NDVI)",
            "unit": "",
            "color_scale": "Greens",
        },
    }

    settings = variable_settings[selected_variable]

    # BOUNDARIES + DATA
    map_gdf = subcounty_gdf.merge(
        map_summary[
            [
                "Display_Name",
                selected_variable
            ]
        ],
        on="Display_Name",
        how="left"
    )

    # CREATE MAP
    climate_map = px.choropleth_map(
        map_gdf,
        geojson=map_gdf.geometry.__geo_interface__,
        locations=map_gdf.index,
        color=selected_variable,
        hover_name="Display_Name",
        color_continuous_scale=settings["color_scale"],
        map_style="open-street-map",
        center={
            "lat": 0.03,
            "lon": 34.30,
        },

        zoom=8.5,
        opacity=0.68,
        labels={
            selected_variable:
                f"{settings['title']} ({settings['unit']})"
                if settings["unit"]
                else settings["title"]
        }
    )

    climate_map.update_traces(
        marker_line_width=1.5,
        marker_line_color="white",
    )

    # ADD SUBCOUNTY LABELS
    label_points = (map_gdf.geometry.representative_point())

    climate_map.add_trace(
        go.Scattermap(
            lat=label_points.y,
            lon=label_points.x,
            mode="text",

            text=map_gdf["Display_Name"],

            textfont=dict(size=13,color="#25313C"),

            hoverinfo="skip",
            showlegend=False,
        )
    )


    climate_map.update_layout(
        height=520,
        margin=dict(l=0,r=0,t=0,b=0),
        paper_bgcolor="white",

        coloraxis_colorbar=dict(
            title=(
                settings["unit"]
                if settings["unit"]
                else "Value"
            ),

            thickness=14,
            len=0.65,
            x=0.98,
        ),
        showlegend=False,
    )

    return climate_map

initial_climate_map = create_climate_map()


# =========================================================
# TAB LAYOUT
layout = dbc.Container(
    [
        # =================================================
        # CLIMATE SPATIAL OVERVIEW
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3(
                        "Climate Spatial Overview",
                        className="fw-bold mb-1",
                        style={"color": "#274C77","fontSize": "28px",},
                    ),
                    # Small divider under title
                    html.Div(
                        style={
                            "width": "55px",
                            "height": "3px",
                            "backgroundColor": "#274C77",
                            "borderRadius": "2px",
                            "marginBottom": "24px",
                        }
                    ),

                    html.P(
                        "The six subcounties of Siaya County exhibit distinct climate and environmental characteristics. "
                        "Subcounties bordering Lake Victoria generally experience different humidity, rainfall, "
                        "and vegetation patterns than those located farther inland due to the moderating influence of the lake. "
                        "Variations in land cover, geography, and seasonal weather conditions also contribute to differences in "
                        "temperature, precipitation, and environmental conditions across the county. Use the filters below to "
                        "compare these patterns across subcounties and examine how they change over time.",
                        className="mb-4",
                        style={
                            "color": "#1F2937",
                            "fontSize": "20px",
                            "lineHeight": "1.8",
                            #"maxWidth": "1050px",
                        },
                    ),

                    # MAP FILTERS
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Label(
                                        "Climate Variable",
                                        className="fw-semibold mb-2",
                                        style={
                                            "color": TEXT,
                                            "fontSize": "18px",
                                        },
                                    ),

                                    dcc.Dropdown(
                                        id="climate-map-variable",
                                        options=[
                                            {
                                                "label":
                                                    "Average Temperature",
                                                "value":
                                                    "Average_Temp",
                                            },

                                            {
                                                "label":
                                                    "Precipitation",
                                                "value":
                                                    "Precipitation",
                                            },

                                            {
                                                "label":
                                                    "Relative Humidity",
                                                "value":
                                                    "Humidity",
                                            },

                                            {
                                                "label":
                                                    "Vegetation Index (NDVI)",
                                                "value":
                                                    "Vegetation_NDVI",
                                            },
                                        ],

                                        value="Average_Temp",
                                        clearable=False,
                                    ),
                                ],
                                lg=8,
                            ),

                            dbc.Col(
                                [
                                    html.Label(
                                        "Year",
                                        className="fw-semibold mb-2",
                                        style={
                                            "color": TEXT,
                                            "fontSize": "18px",
                                        },
                                    ),

                                    dcc.Dropdown(
                                        id="climate-map-year",
                                        options=[
                                            {
                                                "label":
                                                    "All Years",
                                                "value":
                                                    "ALL",
                                            }
                                        ]
                                        +
                                        [
                                            {
                                                "label":
                                                    str(year),

                                                "value":
                                                    year,
                                            }
                                            for year in sorted(years, reverse=True)
                                        ],

                                        value="ALL",
                                        clearable=False,
                                    ),
                                ],
                                lg=4,
                            ),
                        ],
                        className="mb-4",
                    ),


                    #=======================================
                    # MAP
                    dcc.Graph(
                        id="climate-spatial-map",
                        figure=initial_climate_map,
                        config={
                            "displayModeBar": False,
                            "responsive": True,
                        },
                        style={"height": "520px",},
                    ),
                ],
                style={"padding": "24px",},
            ),

            style=CARD_STYLE,
            className="mb-4",
        ),

        # =========================================================
        # CLIMATE TRENDS + FILTERS
        dbc.Card(
            dbc.CardBody(
                [
                    # Section title
                    html.H4(
                        "Climate Trends",
                        className="fw-bold mb-1",
                        style={"color": "#274C77","fontSize": "28px",},
                    ),
                    # Small divider under title
                    html.Div(
                        style={
                            "width": "55px",
                            "height": "3px",
                            "backgroundColor": "#274C77",
                            "borderRadius": "2px",
                            "marginBottom": "24px",
                        }
                    ),
        
                    html.P(
                        "Explore monthly climate and environmental conditions for each subcounty in "
                        "Siaya County. Select a subcounty and year using the filters below to view "
                        "location-specific climate patterns and trends. ",
                        className="mb-4",
                        style={
                            "color": "#1F2937",
                            "fontSize": "20px",
                            "lineHeight": "1.8",
                        },
                    ),
        
                    # Filters
                    dbc.Row(
                        [
                            # Subcounty
                            dbc.Col(
                                [
                                    html.Label(
                                        "Subcounty",
                                        className="fw-semibold mb-2",
                                        style={
                                            "color": TEXT,
                                            "fontSize": "18px",
                                        },
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
        
                            # Year
                            dbc.Col(
                                [
                                    html.Label(
                                        "Year",
                                        className="fw-semibold mb-2",
                                        style={
                                            "color": TEXT,
                                            "fontSize": "18px",
                                        },
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
                                            for year in sorted(years, reverse=True)
                                        ],
        
                                        value="ALL",
        
                                        clearable=False,
                                    ),
                                ],
                                lg=4,
                            ),
                        ]
                    ),
                ],
                style={
                    "padding": "22px 24px",
                },
            ),
        
            style=CARD_STYLE,
            className="mb-4",
        ),

        #=================================================
        # TEMPERATURE + RAINFALL
        dbc.Row(
            [
                # TEMPERATURE
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5(
                                    "Average Temperature",
                                    className="fw-bold mb-1",
                                    style={"color": TEXT,},
                                ),

                                html.P(
                                    "Monthly average air temperature for the selected subcounty and year.",
                                    className="mb-3",
                                    style={
                                        "fontSize": "14px",
                                        "color": TEXT_MUTED,
                                    },
                                ),

                                dcc.Graph(
                                    id="temperature-chart",
                                    figure=empty_figure(),
                                    config={"displayModeBar": False},
                                    style={"height": "430px"},
                                ),
                            ],
                            style={"padding": "22px",},
                        ),

                        style={
                            **CARD_STYLE,
                            "height": "100%",
                        },
                    ),
                    lg=6,
                    className="mb-4",
                ),

                # RAINFALL
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5(
                                    "Monthly Rainfall",
                                    className="fw-bold mb-1",
                                    style={"color": TEXT,},
                                ),

                                html.P(
                                    "Monthly accumulated precipitation for the selected subcounty and year.",
                                    className="mb-3",
                                    style={
                                        "fontSize": "14px",
                                        "color": TEXT_MUTED,
                                    },
                                ),

                                dcc.Graph(
                                    id="rainfall-chart",
                                    figure=empty_figure(),
                                    config={
                                        "displayModeBar":
                                            False
                                    },

                                    style={"height": "430px"},
                                ),
                            ],
                            style={"padding": "22px",},
                        ),

                        style={
                            **CARD_STYLE,
                            "height": "100%",
                        },
                    ),
                    lg=6,
                    className="mb-4",
                ),
            ],
            className="align-items-stretch",
        ),


        # =================================================
        # NDVI + HUMIDITY
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
                                    style={"color": TEXT,},
                                ),

                                html.P(
                                    "Monthly vegetation greenness conditions derived from satellite observations.",
                                    className="mb-3",
                                    style={
                                        "fontSize": "14px",
                                        "color": TEXT_MUTED,
                                    },
                                ),

                                dcc.Graph(
                                    id="ndvi-chart",
                                    figure=empty_figure(),
                                    config={
                                        "displayModeBar":
                                            False
                                    },
                                    style={"height": "430px"},
                                ),
                            ],
                            style={"padding": "22px",},
                        ),

                        style={
                            **CARD_STYLE,
                            "height": "100%",
                        },
                    ),
                    lg=6,
                    className="mb-4",
                ),

                # HUMIDITY
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5(
                                    "Relative Humidity",
                                    className="fw-bold mb-1",
                                    style={"color": TEXT,},
                                ),

                                html.P(
                                    "Monthly average atmospheric humidity for the selected subcounty and year.",
                                    className="mb-3",
                                    style={
                                        "fontSize": "14px",
                                        "color": TEXT_MUTED,
                                    },
                                ),

                                dcc.Graph(
                                    id="humidity-chart",
                                    figure=empty_figure(),
                                    config={
                                        "displayModeBar":
                                            False
                                    },
                                    style={"height": "430px"},
                                ),
                            ],
                            style={"padding": "22px",},
                        ),

                        style={
                            **CARD_STYLE,
                            "height": "100%",
                        },
                    ),

                    lg=6,
                    className="mb-4",
                ),
            ],
            className="align-items-stretch",
        ),

        # =================================================
        # DATA SOURCE
        html.Div(
            [
                html.Hr(
                    style={
                        "borderColor": BORDER,
                        "opacity": "1",
                    }
                ),

                html.P(
                    [
                        html.Strong(
                            "Data source: ",
                            style={"color": TEXT,},
                        ),

                        "Google Earth",
                    ],

                    className="mb-1",
                    style={
                        "fontSize": "15px",
                        "color": TEXT_MUTED,
                    },
                ),
            ],
            className="mt-3 mb-3 px-2",
        ),
    ],

    fluid=True,
    style={
        "backgroundColor": PAGE_BG,
        "padding": "24px",
        "minHeight": "100vh",
    },
)


# =========================================================
# CLIMATE MAP CALLBACK
@callback(
    Output(
        "climate-spatial-map",
        "figure"
    ),

    Input(
        "climate-map-variable",
        "value"
    ),

    Input(
        "climate-map-year",
        "value"
    ),
)
def update_climate_map(
    selected_variable,
    selected_year
):

    return create_climate_map(
        selected_variable,
        selected_year
    )


# =========================================================
# CLIMATE TREND CALLBACK
@callback(
    Output(
        "temperature-chart",
        "figure"
    ),

    Output(
        "rainfall-chart",
        "figure"
    ),

    Output(
        "ndvi-chart",
        "figure"
    ),

    Output(
        "humidity-chart",
        "figure"
    ),

    Input(
        "climate-subcounty-dropdown",
        "value"
    ),

    Input(
        "climate-year-dropdown",
        "value"
    )
)
def update_climate_charts(
    selected_subcounty,
    selected_year
):

    # =====================================================
    # FILTER DATA
    if selected_year == "ALL":
        dff = df[df["SubCounty"]== selected_subcounty].copy()
        dff = dff.sort_values("Date")
        x_col = "Date"
        x_axis_title = "Year"


    else:
        dff = df[(df["SubCounty"]== selected_subcounty)&(df["Year"]== int(selected_year))].copy()
        dff = dff.sort_values("Month")
        x_col = "Month"
        x_axis_title = "Month"


    # =====================================================
    # TEMPERATURE
    temp_fig = px.line(
        dff,
        x=x_col,
        y="Average_Temp",
        markers=(selected_year != "ALL"),
    )

    # =====================================================
    # RAINFALL
    rain_fig = px.bar(
        dff,
        x=x_col,
        y="Precipitation",
    )


    # =====================================================
    # NDVI
    ndvi_fig = px.area(
        dff,
        x=x_col,
        y="Vegetation_NDVI",
    )

    # =====================================================
    # HUMIDITY
    humidity_fig = px.line(
        dff,
        x=x_col,
        y="Humidity",
        markers=(selected_year != "ALL"),
    )


    # =====================================================
    # RESTRAINED COLORS
    temp_fig.update_traces(
        line=dict(
            color="#A35D45",
            width=2.5,
        ),
        marker=dict(color="#A35D45",),
    )

    rain_fig.update_traces(marker_color="#527A9B",)

    ndvi_fig.update_traces(
        line=dict(
            color="#66856A",
            width=2.2,
        ),

        fillcolor="rgba(102,133,106,0.20)",
    )


    humidity_fig.update_traces(
        line=dict(
            color="#5E7F8D",
            width=2.5,
        ),

        marker=dict(color="#5E7F8D",),
    )


    # =====================================================
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
            margin=dict(l=65,r=20,t=20,b=60),
            font=dict(
                family="Segoe UI",
                size=13,
                color=TEXT,
            ),

            paper_bgcolor="white",
            plot_bgcolor="white",
            xaxis_title=x_axis_title,
            hoverlabel=dict(
                bgcolor="white",
                font_size=13,
                font_family="Segoe UI",
            ),
        )


        fig.update_xaxes(
            showgrid=False,
            title_font=dict(size=14),
            linecolor=BORDER,
            tickcolor=BORDER,
        )


        fig.update_yaxes(
            gridcolor="#EDF1F4",
            title_font=dict(size=14),
            zeroline=False,
        )

    # =====================================================
    # Y AXIS UNITS
    temp_fig.update_yaxes(
        title_text=
            "Average temperature (°C)"
    )

    rain_fig.update_yaxes(
        title_text=
            "Precipitation (mm)"
    )

    ndvi_fig.update_yaxes(
        title_text=
            "NDVI (unitless)"
    )

    humidity_fig.update_yaxes(
        title_text=
            "Relative humidity (%)"
    )

    # =====================================================
    # HOVER UNITS
    temp_fig.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Average temperature: "
            "%{y:.1f} °C"
            "<extra></extra>"
        )
    )

    rain_fig.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Precipitation: "
            "%{y:.1f} mm"
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
            "Relative humidity: "
            "%{y:.1f}%"
            "<extra></extra>"
        )
    )

    # =====================================================
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
            "Dec",
        ]


        for fig in [
            temp_fig,
            rain_fig,
            ndvi_fig,
            humidity_fig,
        ]:

            fig.update_xaxes(
                tickmode="array",
                tickvals=list(
                    range(
                        1,
                        13
                    )
                ),
                ticktext=month_labels,
                title_text="Month",
            )


    # =====================================================
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
