from dash import dcc, html, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import geopandas as gpd

#Download 
svg_download_config = {
    "displayModeBar": True,
    "displaylogo": False,
    "responsive": True,
    "modeBarButtonsToRemove": [
        "zoom2d",
        "pan2d",
        "select2d",
        "lasso2d",
        "zoomIn2d",
        "zoomOut2d",
        "autoScale2d",
        "resetScale2d",
    ],
    "toImageButtonOptions": {
        "format": "svg",
        "filename": "visualization",
        "height": 700,
        "width": 1200,
        "scale": 1,
    },
}


#====================================================
# DASHBOARD THEME
PRIMARY = "#274C77"          # Muted navy
PRIMARY_DARK = "#1F3B5B"     # Dark navy
PRIMARY_LIGHT = "#EAF0F6"    # Very light blue
TEXT = "#1F2937"             # Main text
TEXT_MUTED = "#6B7280"       # Secondary text
BORDER = "#DCE3EA"           # Soft border
PAGE_BG = "#F5F7F9"          # Page background
CARD_BG = "#FFFFFF"          # Card background
INSIGHT_BG = "#F8FAFC"       # Insight panel background
MAP_COLORS = ["#6C8EBF","#87A9C7","#7EA6A1","#9B9BC4","#B5A07A","#7F9F8D",]

#population data
population_categories = [
    "Children under 1",
    "Children under 5",
    "Population under 15",
    "Adolescents and youth (15–24)",
    "Adults (25–59)",
    "Older adults (60+)",
]

population_values = [
    33_239,
    148_044,
    475_536,
    215_311,
    364_179,
    95_106,
]


population_figure = go.Figure(
    go.Bar(
        x=population_values,
        y=population_categories,
        orientation="h",
        text=[f"{value:,}" for value in population_values],
        textposition="outside",
        cliponaxis=False,
        hovertemplate=(
            "<b>%{y}</b><br>"
            "Projected population: %{x:,} people"
            "<extra></extra>"
        ),
    )
)


population_figure.update_layout(
    xaxis_title="Projected population (people)",
    yaxis_title="",
    template="plotly_white",
    height=520,
    margin={
        "l": 30,
        "r": 130,
        "t": 20,
        "b": 60,
    },
    showlegend=False,
    bargap=0.22,
)


population_figure.update_yaxes(
    autorange="reversed",
    automargin=True,
)


population_figure.update_xaxes(
    tickformat=",",
    range=[0, 560_000],
    gridcolor="#e9ecef",
)

# =========================================================
# SIAYA SUBCOUNTY BOUNDARY MAP
# Load the same shapefile that was already working
subcounty_gdf = gpd.read_file(
    "Boundary_Data/ke_subcounty.shp"
)

# Keep only the six Siaya subcounties
siaya_subcounties = [
    "Alego Usonga Sub County",
    "Bondo Sub County",
    "Gem Sub County",
    "Rarieda Sub County",
    "Ugenya Sub County",
    "Ugunja Sub County",
]

subcounty_gdf = subcounty_gdf[subcounty_gdf["subcounty"].isin(siaya_subcounties)].copy()

# Make sure map coordinates are longitude / latitude
subcounty_gdf = subcounty_gdf.to_crs(epsg=4326)

# Shorter names for display
subcounty_gdf["Display_Name"] = (subcounty_gdf["subcounty"].str.replace(" Sub County","",regex=False).str.strip())


# =========================================================
# SUBCOUNTY INFORMATION
subcounty_information = {
    "Alego Usonga": {
        "Agriculture": "Mixed crop and livestock farming",
        "Economy": "Agriculture, trade, and services centered around Siaya town",
        "Geography": "Central Siaya County and home to Siaya town",
        "Topography": "Predominantly gently undulating inland terrain",
    },

    "Bondo": {
        "Agriculture": "Crop production, livestock, and fisheries",
        "Economy": "Agriculture, fishing, trade, and Lake Victoria-related economic activity",
        "Geography": "Southwestern Siaya County along Lake Victoria",
        "Topography": "Low-lying and gently rolling terrain toward Lake Victoria",
    },

    "Gem": {
        "Agriculture": "Mixed farming and crop production",
        "Economy": "Agriculture, small-scale trade, and local services",
        "Geography": "Eastern part of Siaya County",
        "Topography": "Undulating inland landscape with agricultural areas",
    },

    "Rarieda": {
        "Agriculture": "Crop production, livestock, and fisheries",
        "Economy": "Agriculture, fishing, livestock, and lake-related economic activity",
        "Geography": "Southern Siaya County along Lake Victoria",
        "Topography": "Rolling terrain descending toward the Lake Victoria shoreline",
    },

    "Ugenya": {
        "Agriculture": "Mixed farming and crop production",
        "Economy": "Agriculture, trade, and small businesses",
        "Geography": "Northwestern Siaya County",
        "Topography": "Gently rolling inland terrain",
    },

    "Ugunja": {
        "Agriculture": "Mixed farming and crop production",
        "Economy": "Agriculture, commerce, transport, and small businesses",
        "Geography": "Northern-central Siaya County",
        "Topography": "Gently undulating inland terrain",
    },
}


# Add information to GeoDataFrame
subcounty_gdf["Agriculture"] = (subcounty_gdf["Display_Name"].map(lambda x: subcounty_information[x]["Agriculture"]))
subcounty_gdf["Economy"] = (subcounty_gdf["Display_Name"].map(lambda x: subcounty_information[x]["Economy"]))
subcounty_gdf["Geography"] = (subcounty_gdf["Display_Name"].map(lambda x: subcounty_information[x]["Geography"]))
subcounty_gdf["Topography"] = (subcounty_gdf["Display_Name"].map(lambda x: subcounty_information[x]["Topography"]))


# =========================================================
# CREATE POLYGON MAP
siaya_map = px.choropleth_map(
    subcounty_gdf,
    geojson=subcounty_gdf.geometry.__geo_interface__,
    locations=subcounty_gdf.index,
    color="Display_Name",
    color_discrete_sequence=MAP_COLORS,
    hover_name="Display_Name",

    # Only show the name on hover
    hover_data={
        "Display_Name": False,
        "Agriculture": False,
        "Economy": False,
        "Geography": False,
        "Topography": False,
    },

    #Map style
    map_style="open-street-map",

    center={
        "lat": 0.03,
        "lon": 34.30,
    },

    zoom=8.3,
    opacity=0.55,
)


# Boundary styling
siaya_map.update_traces(
    marker_line_width=2,
    marker_line_color="white",
)


# =========================================================
# CREATE LABEL LOCATIONS INSIDE EACH SUBCOUNTY
# representative_point() places the point inside the polygon,
label_points = subcounty_gdf.geometry.representative_point()

label_df = pd.DataFrame(
    {
        "Subcounty": subcounty_gdf["Display_Name"].values,
        "Longitude": label_points.x.values,
        "Latitude": label_points.y.values,
    }
)


# =========================================================
# ADD SUBCOUNTY NAMES DIRECTLY ON THE MAP
siaya_map.add_trace(
    go.Scattermap(
        lat=label_df["Latitude"],
        lon=label_df["Longitude"],
        mode="text",
        text=label_df["Subcounty"],

        textfont=dict(
            size=14,
            color="#1f2937",
        ),

        hoverinfo="skip",
        showlegend=False,
    )
)

# MAP LAYOUT
siaya_map.update_layout(
    height=560,
    margin=dict(l=0,r=0,t=0,b=0,),
    paper_bgcolor="white",

    # No external legend because names are inside map
    showlegend=False,
)

#===============================================
# UNDER 5 TREEMAP
disease_labels = [
    "Confirmed malaria",
    "Upper Respiratory Tract Infections",
    "Diseases of the skin",
    "Diarrhoea (no dehydration)",
    "Pneumonia",
    "Lower Respiratory Tract Infections",
    "Gastroenteritis",
    "Eye Infections",
    "Tonsillitis",
    "Ear infection",
    "All Other Conditions/Diseases"
]

disease_values = [
    114002,
    98302,
    17771,
    12534,
    7432,
    6333,
    5337,
    4643,
    2840,
    2741,
    279615
]

treemap_fig = px.treemap(
    names=disease_labels,
    parents=[""] * len(disease_labels),
    values=disease_values,
)

treemap_fig.update_traces(
    textinfo="label+value+percent root",

    hovertemplate=(
        "<b>%{label}</b><br>"
        "Reported outpatient conditions: %{value:,}<br>"
        "Share: %{percentRoot:.1%}"
        "<extra></extra>"
    ),
)

treemap_fig.update_layout(
    template="plotly_white",
    height=500,
    margin=dict(l=10,r=10,t=10,b=10)
)

#==============================================
# UNDER 5 MORTALITY
conditions = [
    "Pneumonia",
    "LBW",
    "Anaemia",
    "Acute Malnutrition",
    "Birth Asphyxia",
    "Respiratory Distress Syndrome",
    "Malaria",
    "Sickle Cell Disease",
    "Hypoglycemia",
    "Dehydration"
]


values = [
    12,
    12,
    11,
    10,
    10,
    10,
    8,
    7,
    6,
    5
]

# Highlight malaria
colors = [
    "#4e79a7",
    "#4e79a7",
    "#4e79a7",
    "#4e79a7",
    "#4e79a7",
    "#4e79a7",
    "#d62728",
    "#4e79a7",
    "#4e79a7",
    "#4e79a7"
]

mortality_fig = go.Figure(
    go.Bar(
        x=values,
        y=conditions,
        orientation="h",
        text=values,
        textposition="outside",
        marker_color=colors,

        hovertemplate=(
            "<b>%{y}</b><br>"
            "Reported occurrences: %{x}"
            "<extra></extra>"
        ),
    )
)

mortality_fig.update_layout(
    template="plotly_white",
    height=500,
    margin=dict(l=20,r=40,t=20,b=20),
    xaxis_title="Reported occurrences (count)",
    yaxis_title="",
    showlegend=False,
)

mortality_fig.update_yaxes(autorange="reversed")

#==================================================
# OVER 5 TREEMAP
over5_labels = [
    "Confirmed Malaria",
    "Upper Respiratory Tract Infections",
    "Diseases of the Skin",
    "Urinary Tract Infections",
    "Arthritis / Joint Pains",
    "Hypertension",
    "Pneumonia",
    "Diarrhoea",
    "Lower Respiratory Tract Infections",
    "Other Injuries",
    "Eye Infections / Conditions",
    "Musculoskeletal Conditions",
    "Dental Disorders",
    "Diabetes",
    "Overweight (BMI >25)",
    "Anaemia",
    "Ear Infections / Conditions",
    "Typhoid Fever",
    "Asthma",
    "Malaria in Pregnancy",
    "All Other Diseases"
]

over5_values = [
    444240,
    219918,
    47149,
    40178,
    32264,
    30589,
    28203,
    23719,
    21033,
    20862,
    18861,
    13558,
    13149,
    10775,
    8908,
    8407,
    8327,
    7283,
    6831,
    6731,
    252559
]

over5_treemap_fig = px.treemap(
    names=over5_labels,
    parents=[""] * len(over5_labels),
    values=over5_values,
)

over5_treemap_fig.update_traces(
    textinfo="label+value+percent root",

    hovertemplate=(
        "<b>%{label}</b><br>"
        "Reported outpatient conditions: %{value:,}<br>"
        "Share: %{percentRoot:.1%}"
        "<extra></extra>"
    ),
)


over5_treemap_fig.update_layout(
    template="plotly_white",
    height=500,
    margin=dict(l=10,r=10,t=10,b=10)
)

# OVER 5 MORTALITY
over5_conditions = [
    "Pneumonia",
    "HIV",
    "Hypertension",
    "Anemia",
    "Viral Infection",
    "Bacteremia",
    "Diseases of Respiratory System",
    "Head Injury",
    "Malaria",
    "Congestive Heart Failure"
]

over5_values = [
    60,
    57,
    46,
    32,
    27,
    27,
    24,
    21,
    21,
    21
]

over5_colors = [
    "#4e79a7",
    "#4e79a7",
    "#4e79a7",
    "#4e79a7",
    "#4e79a7",
    "#4e79a7",
    "#4e79a7",
    "#4e79a7",
    "#d62728",
    "#4e79a7",
]

over5_mortality_fig = go.Figure(
    go.Bar(
        x=over5_values,
        y=over5_conditions,
        orientation="h",
        text=over5_values,
        textposition="outside",
        marker_color=over5_colors,

        hovertemplate=(
            "<b>%{y}</b><br>"
            "Reported occurrences: %{x}"
            "<extra></extra>"
        ),
    )
)


over5_mortality_fig.update_layout(
    template="plotly_white",
    height=500,
    margin=dict(l=20,r=40,t=20,b=20),
    xaxis_title="Reported occurrences (count)",
    yaxis_title="",
    showlegend=False,
)

over5_mortality_fig.update_yaxes(autorange="reversed")


# =========================================================
# SUBCOUNTY INFORMATION PANEL
def build_subcounty_information_panel(selected_subcounty):
    info = subcounty_information[selected_subcounty]

    return [
        html.H4(
            selected_subcounty,
            className="fw-bold mb-4",
            style={"color": PRIMARY,"fontSize": "25px",},
        ),

        html.Div(
            [
                html.H6(
                    "Agriculture",
                    className="fw-bold mb-1",
                    style={"color": TEXT},
                ),
                html.P(
                    info["Agriculture"],
                    className="mb-3",
                    style={"color": TEXT_MUTED, "lineHeight": "1.6"},
                ),
            ]
        ),

        html.Div(
            [
                html.H6(
                    "Economy",
                    className="fw-bold mb-1",
                    style={"color": TEXT},
                ),
                html.P(
                    info["Economy"],
                    className="mb-3",
                    style={"color": TEXT_MUTED, "lineHeight": "1.6"},
                ),
            ]
        ),

        html.Div(
            [
                html.H6(
                    "Geography",
                    className="fw-bold mb-1",
                    style={"color": TEXT},
                ),
                html.P(
                    info["Geography"],
                    className="mb-3",
                    style={"color": TEXT_MUTED, "lineHeight": "1.6"},
                ),
            ]
        ),

        html.Div(
            [
                html.H6(
                    "Topography",
                    className="fw-bold mb-1",
                    style={"color": TEXT},
                ),
                html.P(
                    info["Topography"],
                    className="mb-0",
                    style={"color": TEXT_MUTED, "lineHeight": "1.6"},
                ),
            ]
        ),
    ]


# =========================================================
# CARD STYLING
CARD_STYLE = {
    "backgroundColor": CARD_BG,
    "border": f"1px solid {BORDER}",
    "borderRadius": "10px",
    "boxShadow": "0 2px 8px rgba(15, 23, 42, 0.05)",
}

INSIGHT_STYLE = {
    "backgroundColor": INSIGHT_BG,
    "border": f"1px solid {BORDER}",
    "borderRadius": "10px",
    "height": "100%",
}

# Population figure traces
population_figure.update_traces(
    marker=dict(
        color=PRIMARY,
        line=dict(
            color=PRIMARY_DARK,
            width=1
        )
    )
)

for fig in [
    population_figure,
    treemap_fig,
    mortality_fig,
    over5_treemap_fig,
    over5_mortality_fig,
]:
    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",

        font=dict(
            family="Segoe UI",
            size=14
        )
    )


# =========================================================
# LAYOUT
layout = dbc.Container(
    [
        # =================================================
        # SUBCOUNTY FILTER
        dbc.Card(
            dbc.CardBody(
                [
                    html.Label(
                        "Subcounty",
                        className="fw-semibold mb-2",
                        style={"color": TEXT,"fontSize": "14px",},
                    ),

                    dcc.Dropdown(
                        id="overview-subcounty-dropdown",
                        options=[
                            {
                                "label": name,
                                "value": name
                            }
                            for name in [
                                "Alego Usonga",
                                "Bondo",
                                "Gem",
                                "Rarieda",
                                "Ugenya",
                                "Ugunja",
                            ]
                        ],

                        value="Alego Usonga",
                        clearable=False,
                    ),
                ],
                style={"padding": "18px 20px",},
            ),
            style=CARD_STYLE,
            className="mb-4",
        ),


        # =================================================
        # MAP + SUBCOUNTY INFORMATION
        dbc.Card(
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            # Map
                            dbc.Col(
                                dcc.Graph(
                                    id="siaya-overview-map",
                                    figure=siaya_map,
                                    config={
                                        "displayModeBar": False,
                                        "responsive": True,
                                    },
                                    style={"height": "560px","width": "100%",},
                                ),
                                lg=8,
                                style={"height": "560px",},
                            ),

                            # Subcounty information
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        id="subcounty-information-panel",
                                        children=build_subcounty_information_panel("Alego Usonga"),

                                        style={
                                            "padding": "26px",
                                            "display": "flex",
                                            "flexDirection": "column",
                                            "justifyContent": "flex-start",
                                        },
                                    ),

                                    style={
                                        **INSIGHT_STYLE,
                                        "height": "560px",
                                    },
                                ),

                                lg=4,

                                style={
                                    "height": "560px",
                                },
                            ),
                        ],
                        className="g-4 align-items-stretch",
                    ),
                ],
                style={"padding": "20px",},
            ),
            style=CARD_STYLE,
            className="mb-4",
        ),

        # =================================================
        # POPULATION DISTRIBUTION
        dbc.Card(
            dbc.CardBody(
                [
                    html.H4(
                        "Population Distribution",
                        className="fw-bold mb-1",
                        style={"color": TEXT,},
                    ),

                    html.P(
                        "Projected population distribution across major age groups.",
                        className="mb-4",
                        style={"color": TEXT_MUTED,},
                    ),

                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(
                                    id="population-profile-chart",
                                    figure=population_figure,
                                    config=svg_download_config,
                                    style={ "height": "550px",},
                                ),

                                lg=8,
                                style={"height": "550px",},
                            ),

                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.H6(
                                                "Key Insights",
                                                className="fw-bold mb-3",
                                                style={"color": PRIMARY,},
                                            ),

                                            html.Ul(
                                                [
                                                    html.Li(
                                                        "Children under 15 years represent "
                                                        "the largest population group."
                                                    ),

                                                    html.Li(
                                                        "Population demographics highlight "
                                                        "the importance of child health and "
                                                        "malaria prevention."
                                                    ),

                                                    html.Li(
                                                        "Age structure influences disease "
                                                        "burden, healthcare utilization, "
                                                        "and resource planning."
                                                    ),

                                                ],

                                                style={
                                                    "fontSize": "30px",
                                                    "lineHeight": "1.8",
                                                    "color": TEXT,
                                                    "paddingLeft": "20px",
                                                },
                                            ),

                                        ],
                                        style={"padding": "24px",},
                                    ),

                                    style={
                                        **INSIGHT_STYLE,
                                        "height": "550px",
                                    },
                                ),
                                lg=4,
                                style={"height": "550px",},
                            ),

                        ],
                        className="g-4 align-items-stretch",
                    ),
                ],
                style={"padding": "24px",},
            ),
            style=CARD_STYLE,
            className="mb-4",
        ),


        # =================================================
        # KPI CARDS
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Div(
                                    "Total Population",
                                    style={
                                        "color": TEXT_MUTED,
                                        "fontSize": "14px",
                                        "fontWeight": "500",
                                    },
                                ),

                                html.H3(
                                    "1.15M",
                                    className="fw-bold mb-0",
                                    style={
                                        "color": PRIMARY,
                                        "marginTop": "5px",
                                    },
                                ),

                                html.Small(
                                    "people",
                                    style={
                                        "color": TEXT_MUTED,
                                    },
                                ),
                            ],

                            style={
                                "padding": "20px",
                            },
                        ),

                        style={
                            **CARD_STYLE,
                            "height": "100%",
                        },
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
                                    "Population Under 15",
                                    style={
                                        "color": TEXT_MUTED,
                                        "fontSize": "14px",
                                        "fontWeight": "500",
                                    },
                                ),
                                
                                html.H3(
                                    "475K+",
                                    className="fw-bold mb-0",
                                    style={
                                        "color": PRIMARY,
                                        "marginTop": "5px",
                                    },
                                ),

                                html.Small(
                                    "people",
                                    style={
                                        "color": TEXT_MUTED,
                                    },
                                ),
                            ],
                            style={"padding": "20px",},
                        ),

                        style={
                            **CARD_STYLE,
                            "height": "100%",
                        },
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
                                    "Under-5 Conditions",
                                    style={
                                        "color": TEXT_MUTED,
                                        "fontSize": "14px",
                                        "fontWeight": "500",
                                    },
                                ),

                                html.H3(
                                    "550K+",
                                    className="fw-bold mb-0",
                                    style={
                                        "color": PRIMARY,
                                        "marginTop": "5px",
                                    },
                                ),

                                html.Small(
                                    "reported outpatient conditions",
                                    style={"color": TEXT_MUTED,},
                                ),
                            ],
                            style={"padding": "20px",},
                        ),

                        style={
                            **CARD_STYLE,
                            "height": "100%",
                        },
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
                                    "Over-5 Conditions",
                                    style={
                                        "color": TEXT_MUTED,
                                        "fontSize": "14px",
                                        "fontWeight": "500",
                                    },
                                ),

                                html.H3(
                                    "1.26M+",
                                    className="fw-bold mb-0",
                                    style={
                                        "color": PRIMARY,
                                        "marginTop": "5px",
                                    },
                                ),

                                html.Small(
                                    "reported outpatient conditions",
                                    style={
                                        "color": TEXT_MUTED,
                                    },
                                ),
                            ],
                            style={"padding": "20px",},
                        ),

                        style={
                            **CARD_STYLE,
                            "height": "100%",
                        },
                    ),

                    lg=3,
                    md=6,

                    className="mb-3",
                ),

            ],

            className="mb-3 align-items-stretch",
        ),


        # =================================================
        # UNDER 5 CONDITIONS
        dbc.Card(
            dbc.CardBody(
                [

                    html.H4(
                        "Most Common Outpatient Health Conditions (Under 5 Years)",

                        className="fw-bold mb-1",

                        style={
                            "color": TEXT,
                        },
                    ),

                    html.P(
                        "Distribution of reported outpatient conditions "
                        "among children under five years. Values represent counts "
                        "of reported conditions.",

                        className="mb-4",
                        style={"color": TEXT_MUTED,},
                    ),


                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(
                                    id="under5-disease-chart",
                                    figure=treemap_fig,
                                    config={
                                        "displayModeBar": False,
                                        "responsive": True,
                                    },

                                    style={
                                        "height": "550px",
                                    },
                                ),

                                lg=8,

                                style={
                                    "height": "550px",
                                },
                            ),


                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [

                                            html.H6(
                                                "Key Insights",

                                                className="fw-bold mb-3",

                                                style={
                                                    "color": PRIMARY,
                                                },
                                            ),

                                            html.Ul(
                                                [

                                                    html.Li(
                                                        "Confirmed malaria was the "
                                                        "leading outpatient condition."
                                                    ),

                                                    html.Li(
                                                        "Upper respiratory tract infections "
                                                        "ranked second."
                                                    ),

                                                    html.Li(
                                                        "Malaria and respiratory illnesses "
                                                        "accounted for nearly 40% of "
                                                        "disease burden."
                                                    ),

                                                    html.Li(
                                                        "Top 10 conditions represented "
                                                        "almost half of all visits."
                                                    ),

                                                ],

                                                style={
                                                    "fontSize": "30px",
                                                    "lineHeight": "1.8",
                                                    "color": TEXT,
                                                    "paddingLeft": "20px",
                                                },
                                            ),

                                        ],

                                        style={
                                            "padding": "24px",
                                        },
                                    ),

                                    style={
                                        **INSIGHT_STYLE,
                                        "height": "550px",
                                    },
                                ),

                                lg=4,

                                style={
                                    "height": "550px",
                                },
                            ),

                        ],

                        className="g-4 align-items-stretch",
                    ),

                ],

                style={
                    "padding": "24px",
                },
            ),

            style=CARD_STYLE,

            className="mb-4",
        ),


        # =================================================
        # UNDER 5 MORTALITY
        dbc.Card(
            dbc.CardBody(
                [

                    html.H4(
                        "Leading Causes of Mortality (Under 5 Years)",

                        className="fw-bold mb-1",

                        style={
                            "color": TEXT,
                        },
                    ),

                    html.P(
                        "Most frequently reported causes of mortality among "
                        "children under five years. Values are reported occurrences.",

                        className="mb-4",

                        style={
                            "color": TEXT_MUTED,
                        },
                    ),

                    dcc.Graph(
                        id="under5-mortality-chart",
                        figure=mortality_fig,
                        config=svg_download_config,
                    ),

                ],

                style={
                    "padding": "24px",
                },
            ),

            style=CARD_STYLE,

            className="mb-4",
        ),


        # =================================================
        # OVER 5 CONDITIONS
        dbc.Card(
            dbc.CardBody(
                [

                    html.H4(
                        "Most Common Outpatient Health Conditions (Over 5 Years)",

                        className="fw-bold mb-1",

                        style={
                            "color": TEXT,
                        },
                    ),

                    html.P(
                        "Distribution of reported outpatient conditions among "
                        "individuals over five years. Values represent counts "
                        "of reported conditions.",

                        className="mb-4",

                        style={
                            "color": TEXT_MUTED,
                        },
                    ),


                    dbc.Row(
                        [

                            dbc.Col(
                                dcc.Graph(
                                    id="over5-disease-chart",

                                    figure=over5_treemap_fig,

                                    config={
                                        "displayModeBar": False,
                                        "responsive": True,
                                    },

                                    style={
                                        "height": "550px",
                                    },
                                ),

                                lg=8,

                                style={
                                    "height": "550px",
                                },
                            ),


                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [

                                            html.H6(
                                                "Key Insights",

                                                className="fw-bold mb-3",

                                                style={
                                                    "color": PRIMARY,
                                                },
                                            ),

                                            html.Ul(
                                                [

                                                    html.Li(
                                                        "Confirmed malaria was the "
                                                        "leading outpatient condition."
                                                    ),

                                                    html.Li(
                                                        "Malaria and respiratory infections "
                                                        "contributed substantially to "
                                                        "disease burden."
                                                    ),

                                                    html.Li(
                                                        "The top twenty conditions represented "
                                                        "approximately 80% of visits."
                                                    ),

                                                ],

                                                style={
                                                    "fontSize": "30px",
                                                    "lineHeight": "1.8",
                                                    "color": TEXT,
                                                    "paddingLeft": "20px",
                                                },
                                            ),

                                        ],
                                        style={"padding": "24px",},
                                    ),

                                    style={
                                        **INSIGHT_STYLE,
                                        "height": "550px",
                                    },
                                ),

                                lg=4,
                                style={
                                    "height": "550px",
                                },
                            ),

                        ],

                        className="g-4 align-items-stretch",
                    ),

                ],

                style={
                    "padding": "24px",
                },
            ),

            style=CARD_STYLE,

            className="mb-4",
        ),


        # =================================================
        # OVER 5 MORTALITY
        dbc.Card(
            dbc.CardBody(
                [

                    html.H4(
                        "Leading Causes of Mortality (Over 5 Years)",

                        className="fw-bold mb-1",

                        style={
                            "color": TEXT,
                        },
                    ),

                    html.P(
                        "Most frequently reported causes of mortality among "
                        "individuals over five years. Values are reported occurrences.",

                        className="mb-4",

                        style={
                            "color": TEXT_MUTED,
                        },
                    ),

                    dcc.Graph(
                        id="over5-mortality-chart",

                        figure=over5_mortality_fig,

                        config={
                            "displayModeBar": False,
                            "responsive": True,
                        },
                    ),

                ],

                style={
                    "padding": "24px",
                },
            ),

            style=CARD_STYLE,

            className="mb-4",
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
                            style={
                                "color": TEXT,
                            },
                        ),

                        "Rarieda Sub-County Health Promotion Officer and "
                        "Community Health Services within Siaya County",
                    ],

                    className="mb-1",

                    style={
                        "fontSize": "15px",
                        "color": TEXT_MUTED,
                    },
                ),

            ],

            className="mt-4 mb-3 px-2",
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
# SUBCOUNTY INFORMATION CALLBACK
@callback(
    Output("subcounty-information-panel", "children"),
    Input("overview-subcounty-dropdown", "value")
)
def update_subcounty_information(selected_subcounty):
    return build_subcounty_information_panel(selected_subcounty)
