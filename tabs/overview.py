from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

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

# SIAYA SUB-COUNTY MAP
# Approximate geographic centers used only to position
# sub-county information on the overview map.
subcounty_data = pd.DataFrame(
    {
        "Subcounty": [
            "Alego Usonga",
            "Bondo",
            "Gem",
            "Rarieda",
            "Ugenya",
            "Ugunja",
        ],

        "Latitude": [
            0.060,
            -0.090,
            0.110,
            -0.170,
            0.180,
            0.200,
        ],

        "Longitude": [
            34.285,
            34.270,
            34.430,
            34.390,
            34.210,
            34.300,
        ],

        "Agriculture": [
            "Mixed crop and livestock farming",
            "Crop production, livestock, and fisheries",
            "Mixed farming and crop production",
            "Crop production, livestock, and fisheries",
            "Mixed farming and crop production",
            "Mixed farming and crop production",
        ],

        "Economy": [
            "Agriculture, trade, and services centered around Siaya town",
            "Agriculture, fishing, trade, and the Lake Victoria blue economy",
            "Agriculture, small-scale trade, and local services",
            "Agriculture, fishing, livestock, and lake-related economic activity",
            "Agriculture, cross-regional trade, and small businesses",
            "Agriculture, commerce, transport, and small businesses",
        ],

        "Geography": [
            "Central Siaya County and home to Siaya town",
            "Southwestern Siaya with extensive Lake Victoria influence",
            "Eastern part of Siaya County",
            "Southern Siaya along Lake Victoria",
            "Northwestern Siaya near the Kenya–Uganda transport corridor",
            "Northern-central Siaya County",
        ],

        "Topography": [
            "Predominantly gently undulating inland terrain",
            "Low-lying and gently rolling terrain toward Lake Victoria",
            "Undulating inland landscape with agricultural areas",
            "Rolling terrain descending toward the Lake Victoria shoreline",
            "Gently rolling inland terrain",
            "Gently undulating inland terrain",
        ],
    }
)


# Create detailed hover text
subcounty_data["hover_text"] = (
    "<b>"
    + subcounty_data["Subcounty"]
    + "</b>"
    + "<br><br><b>Agriculture:</b> "
    + subcounty_data["Agriculture"]
    + "<br><b>Economy:</b> "
    + subcounty_data["Economy"]
    + "<br><b>Geography:</b> "
    + subcounty_data["Geography"]
    + "<br><b>Topography:</b> "
    + subcounty_data["Topography"]
)


siaya_map = go.Figure(
    go.Scattermapbox(
        lat=subcounty_data["Latitude"],
        lon=subcounty_data["Longitude"],

        mode="markers+text",

        marker=dict(
            size=16,
            color="#2563eb",
        ),

        text=subcounty_data["Subcounty"],

        textposition="top center",

        textfont=dict(
            size=13,
            color="#1f2937",
        ),

        customdata=subcounty_data["hover_text"],

        hovertemplate="%{customdata}<extra></extra>",
    )
)


siaya_map.update_layout(
    mapbox=dict(
        style="open-street-map",
        center=dict(
            lat=0.03,
            lon=34.30,
        ),
        zoom=8.5,
    ),

    height=560,

    margin=dict(
        l=0,
        r=0,
        t=0,
        b=0,
    ),

    paper_bgcolor="white",

    showlegend=False,
)

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
    margin=dict(
        l=10,
        r=10,
        t=10,
        b=10
    )
)

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

    margin=dict(
        l=20,
        r=40,
        t=20,
        b=20
    ),

    xaxis_title="Reported occurrences (count)",
    yaxis_title="",

    showlegend=False,
)


mortality_fig.update_yaxes(
    autorange="reversed"
)

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

    margin=dict(
        l=10,
        r=10,
        t=10,
        b=10
    )
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

    margin=dict(
        l=20,
        r=40,
        t=20,
        b=20
    ),

    xaxis_title="Reported occurrences (count)",
    yaxis_title="",

    showlegend=False,
)


over5_mortality_fig.update_yaxes(
    autorange="reversed"
)

# THEME
CARD_STYLE = {
    "border": "none",
    "borderRadius": "18px",
    "boxShadow": "0 4px 15px rgba(0,0,0,0.08)",
}


INSIGHT_STYLE = {
    "backgroundColor": "#f8fafc",
    "border": "1px solid #e2e8f0",
    "borderRadius": "12px",
}

# IMPROVE FIGURE STYLING
population_figure.update_traces(
    marker=dict(
        color="#2563eb",
        line=dict(
            color="#1d4ed8",
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


# LAYOUT
layout = dbc.Container(
    [
        # =================================================
        # SIAYA COUNTY MAP
        # =================================================
        dbc.Card(
            dbc.CardBody(
                [

                    html.H4(
                        "Siaya County Geographic Overview",
                        className="fw-bold mb-1",
                    ),

                    html.P(
                        "Explore the six sub-counties of Siaya County. "
                        "Hover over each location for a brief summary of "
                        "agriculture, economic activity, geography, and topography.",
                        className="text-muted mb-4",
                    ),


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

                                    style={
                                        "height": "560px",
                                    },
                                ),

                                lg=8,
                            ),


                            # Map information panel
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [

                                            html.H6(
                                                "County Context",
                                                className="fw-bold text-primary mb-3",
                                            ),

                                            html.P(
                                                "Siaya County consists of six "
                                                "sub-counties: Alego Usonga, Bondo, "
                                                "Gem, Rarieda, Ugenya, and Ugunja.",
                                                className="mb-3",
                                            ),

                                            html.P(
                                                "Agriculture is an important part "
                                                "of the county economy, while "
                                                "communities near Lake Victoria, "
                                                "particularly Bondo and Rarieda, "
                                                "also have strong links to fisheries "
                                                "and the blue economy.",
                                                className="mb-3",
                                            ),

                                            html.P(
                                                "Hover over a sub-county marker on "
                                                "the map to view additional geographic "
                                                "and economic information.",
                                                className="text-muted mb-0",
                                            ),

                                        ]
                                    ),

                                    style=INSIGHT_STYLE,
                                ),

                                lg=4,
                            ),

                        ],

                        className="align-items-center",
                    ),

                ],

                className="p-4",
            ),

            className="mb-4 border-0 shadow-sm",
        ),

        
        # =================================================
        # KPI CARDS
        # =================================================
        dbc.Row(
            [

                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.Div(
                                    "Total Population",
                                    className="text-muted",
                                ),

                                html.H3(
                                    "1.15M",
                                    className="fw-bold text-primary mb-0",
                                ),

                                html.Small(
                                    "people",
                                    className="text-muted",
                                ),
                            ]
                        ),

                        style=CARD_STYLE,
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
                                    className="text-muted",
                                ),

                                html.H3(
                                    "475K+",
                                    className="fw-bold text-primary mb-0",
                                ),

                                html.Small(
                                    "people",
                                    className="text-muted",
                                ),
                            ]
                        ),

                        style=CARD_STYLE,
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
                                    className="text-muted",
                                ),

                                html.H3(
                                    "550K+",
                                    className="fw-bold text-primary mb-0",
                                ),

                                html.Small(
                                    "reported outpatient conditions",
                                    className="text-muted",
                                ),
                            ]
                        ),

                        style=CARD_STYLE,
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
                                    className="text-muted",
                                ),

                                html.H3(
                                    "1.26M+",
                                    className="fw-bold text-primary mb-0",
                                ),

                                html.Small(
                                    "reported outpatient conditions",
                                    className="text-muted",
                                ),
                            ]
                        ),

                        style=CARD_STYLE,
                    ),

                    lg=3,
                    md=6,
                    className="mb-3",
                ),

            ],

            className="mb-4",
        ),


        # =================================================
        # POPULATION INFORMATION
        # =================================================

        dbc.Card(
            dbc.CardBody(
                [

                    html.H4(
                        "Population Distribution",
                        className="fw-bold mb-1",
                    ),

                    html.P(
                        "Projected population distribution across major age groups.",
                        className="text-muted mb-4",
                    ),


                    dbc.Row(
                        [

                            dbc.Col(
                                dcc.Graph(
                                    id="population-profile-chart",
                                    figure=population_figure,
                                    config=svg_download_config,

                                    style={
                                        "height": "550px"
                                    },
                                ),

                                lg=8,
                            ),


                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [

                                            html.H6(
                                                "Key Insights",
                                                className="fw-bold text-primary",
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
                                                    "fontSize": "15px",
                                                    "lineHeight": "1.8",
                                                },
                                            ),

                                        ]
                                    ),

                                    style=INSIGHT_STYLE,
                                ),

                                lg=4,
                            ),

                        ]
                    ),

                ],

                className="p-4",
            ),

            className="mb-4 border-0 shadow-sm",
        ),


        # =================================================
        # UNDER 5 TOTAL CONDITIONS
        # =================================================
        dbc.Card(
            dbc.CardBody(
                [

                    html.H4(
                        "Most Common Outpatient Health Conditions (Under 5 Years)",
                        className="fw-bold mb-1",
                    ),

                    html.P(
                        "Distribution of reported outpatient conditions "
                        "among children under five years. Values represent counts "
                        "of reported conditions.",
                        className="text-muted mb-4",
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
                                        "height": "550px"
                                    },
                                ),

                                lg=8,
                            ),


                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [

                                            html.H6(
                                                "Key Insights",
                                                className="fw-bold text-primary",
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
                                                    "fontSize": "15px",
                                                    "lineHeight": "1.8",
                                                },
                                            ),

                                        ]
                                    ),

                                    style=INSIGHT_STYLE,
                                ),

                                lg=4,
                            ),

                        ]
                    ),

                ],

                className="p-4",
            ),

            className="mb-4 border-0 shadow-sm",
        ),


        # =================================================
        # UNDER 5 MORTALITY
        # =================================================
        dbc.Card(
            dbc.CardBody(
                [

                    html.H4(
                        "Leading Causes of Mortality (Under 5 Years)",
                        className="fw-bold mb-1",
                    ),

                    html.P(
                        "Most frequently reported causes of mortality among "
                        "children under five years. Values are reported occurrences.",
                        className="text-muted mb-4",
                    ),

                    dcc.Graph(
                        id="under5-mortality-chart",
                        figure=mortality_fig,
                        config=svg_download_config,
                    ),

                ],

                className="p-4",
            ),

            className="mb-4 border-0 shadow-sm",
        ),


        # =================================================
        # OVER 5 TOTAL CONDITIONS
        # =================================================
        dbc.Card(
            dbc.CardBody(
                [

                    html.H4(
                        "Most Common Outpatient Health Conditions (Over 5 Years)",
                        className="fw-bold mb-1",
                    ),

                    html.P(
                        "Distribution of reported outpatient conditions among "
                        "individuals over five years. Values represent counts "
                        "of reported conditions.",
                        className="text-muted mb-4",
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
                                        "height": "550px"
                                    },
                                ),

                                lg=8,
                            ),


                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        [

                                            html.H6(
                                                "Key Insights",
                                                className="fw-bold text-primary",
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
                                                    "fontSize": "15px",
                                                    "lineHeight": "1.8",
                                                },
                                            ),

                                        ]
                                    ),

                                    style=INSIGHT_STYLE,
                                ),

                                lg=4,
                            ),

                        ]
                    ),

                ],

                className="p-4",
            ),

            className="mb-4 border-0 shadow-sm",
        ),


        # =================================================
        # OVER 5 MORTALITY
        # =================================================
        dbc.Card(
            dbc.CardBody(
                [

                    html.H4(
                        "Leading Causes of Mortality (Over 5 Years)",
                        className="fw-bold mb-1",
                    ),

                    html.P(
                        "Most frequently reported causes of mortality among "
                        "individuals over five years. Values are reported occurrences.",
                        className="text-muted mb-4",
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

                className="p-4",
            ),

            className="mb-4 border-0 shadow-sm",
        ),


        # =================================================
        # DATA SOURCE
        # =================================================
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
                        "Rarieda Sub-County Health Promotion Officer and Community Health Services within Siaya County",
                    ],

                    className="text-muted mb-1",

                    style={
                        "fontSize": "30px",
                    },
                ),

            ],

            className="mt-4 mb-3 px-2",
        ),

    ],

    fluid=True,

    style={
        "backgroundColor": "#f8fafc",
        "padding": "25px",
    },
)
