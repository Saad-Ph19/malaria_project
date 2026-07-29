from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
            "Projected population: %{x:,}<extra></extra>"
        ),
    )
)

population_figure.update_layout(
    xaxis_title="Projected population",
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

# Under 5 treemap
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
    textinfo="label+value+percent root"
)

treemap_fig.update_layout(
    template="plotly_white",
    height=500,
    margin=dict(l=10, r=10, t=10, b=10)
)

# Bar chart for the causes of death
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

values = [12, 12, 11, 10, 10, 10, 8, 7, 6, 5]

# Highlight malaria
colors = ["#4e79a7",  "#4e79a7",  "#4e79a7",  "#4e79a7",  "#4e79a7",  "#4e79a7",  "#d62728", "#4e79a7",  "#4e79a7",  "#4e79a7"   ]
mortality_fig = go.Figure(
    go.Bar(
        x=values,
        y=conditions,
        orientation="h",
        text=values,
        textposition="outside",
        marker_color=colors,
    )
)

mortality_fig.update_layout(
    template="plotly_white",
    height=500,
    margin=dict(l=20, r=40, t=20, b=20),
    xaxis_title="Occurrence",
    yaxis_title="",
    showlegend=False,
)

mortality_fig.update_yaxes(
    autorange="reversed"
)

#Over 5 year data
#over 5 treemap
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
    textinfo="label+value+percent root"
)

over5_treemap_fig.update_layout(
    template="plotly_white",
    height=500,
    margin=dict(l=10, r=10, t=10, b=10)
)

#Bar chart
over5_conditions = ["Pneumonia","HIV","Hypertension","Anemia","Viral Infection","Bacteremia","Diseases of Respiratory System","Head Injury","Malaria","Congestive Heart Failure"]
over5_values = [60, 57, 46, 32, 27, 27, 24, 21, 21, 21]
over5_colors = ["#4e79a7","#4e79a7","#4e79a7","#4e79a7","#4e79a7","#4e79a7","#4e79a7","#4e79a7","#d62728","#4e79a7",]

over5_mortality_fig = go.Figure(
    go.Bar(
        x=over5_values,
        y=over5_conditions,
        orientation="h",
        text=over5_values,
        textposition="outside",
        marker_color=over5_colors,
    )
)

over5_mortality_fig.update_layout(
    template="plotly_white",
    height=500,
    margin=dict(l=20, r=40, t=20, b=20),
    xaxis_title="Occurrence",
    yaxis_title="",
    showlegend=False,
)

over5_mortality_fig.update_yaxes(
    autorange="reversed"
)
# =========================================================
# THEME
# =========================================================

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

# =========================================================
# IMPROVE FIGURE STYLING
# =========================================================

population_figure.update_traces(
    marker=dict(
        color="#2563eb",
        line=dict(color="#1d4ed8", width=1)
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
# =========================================================

layout = dbc.Container(

    [

        # =====================================================
        # HEADER
        # =====================================================

        html.Div(
            [
                html.H2(
                    "Siaya County Health Profile Dashboard",
                    className="fw-bold mb-1",
                    style={"color": "white"},
                ),

                html.P(
                    "Population structure, disease burden, outpatient conditions and mortality indicators (2024/2025)",
                    className="mb-0",
                    style={"color": "#e2e8f0"},
                ),
            ],
            className="p-4 rounded-4 mb-4",
            style={
                "background": "linear-gradient(135deg,#0f172a,#2563eb)"
            },
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
                                    "Total Population",
                                    className="text-muted",
                                ),
                                html.H3(
                                    "1.15M",
                                    className="fw-bold text-primary mb-0",
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
                                    "475,536",
                                    className="fw-bold text-primary mb-0",
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

        # =====================================================
        # POPULATION SECTION
        # =====================================================

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
                                    style={"height": "550px"},
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
                                                        "Children under 15 years represent the largest population group."
                                                    ),

                                                    html.Li(
                                                        "Population demographics highlight the importance of child health and malaria prevention."
                                                    ),

                                                    html.Li(
                                                        "Age structure influences disease burden, healthcare utilization, and resource planning."
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

        # =====================================================
        # UNDER 5 CONDITIONS
        # =====================================================

        dbc.Card(

            dbc.CardBody(

                [

                    html.H4(
                        "Most Common Outpatient Health Conditions (Under 5 Years)",
                        className="fw-bold mb-1",
                    ),

                    html.P(
                        "Distribution of reported outpatient conditions among children under five years.",
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
                                    style={"height": "550px"},
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
                                                        "Confirmed malaria was the leading outpatient condition."
                                                    ),

                                                    html.Li(
                                                        "Upper respiratory tract infections ranked second."
                                                    ),

                                                    html.Li(
                                                        "Malaria and respiratory illnesses accounted for nearly 40% of disease burden."
                                                    ),

                                                    html.Li(
                                                        "Top 10 conditions represented almost half of all visits."
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

        # =====================================================
        # UNDER 5 MORTALITY
        # =====================================================

        dbc.Card(

            dbc.CardBody(

                [

                    html.H4(
                        "Leading Causes of Mortality (Under 5 Years)",
                        className="fw-bold mb-1",
                    ),

                    html.P(
                        "Most frequently reported causes of mortality among children under five years.",
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

        # =====================================================
        # OVER 5 CONDITIONS
        # =====================================================

        dbc.Card(

            dbc.CardBody(

                [

                    html.H4(
                        "Most Common Outpatient Health Conditions (Over 5 Years)",
                        className="fw-bold mb-1",
                    ),

                    html.P(
                        "Distribution of reported outpatient conditions among individuals over five years.",
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
                                    style={"height": "550px"},
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
                                                        "Confirmed malaria was the leading outpatient condition."
                                                    ),

                                                    html.Li(
                                                        "Malaria and respiratory infections contributed substantially to disease burden."
                                                    ),

                                                    html.Li(
                                                        "The top twenty conditions represented approximately 80% of visits."
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

        # =====================================================
        # OVER 5 MORTALITY
        # =====================================================

        dbc.Card(

            dbc.CardBody(

                [

                    html.H4(
                        "Leading Causes of Mortality (Over 5 Years)",
                        className="fw-bold mb-1",
                    ),

                    html.P(
                        "Most frequently reported causes of mortality among individuals over five years.",
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

    ],

    fluid=True,

    style={
        "backgroundColor": "#f8fafc",
        "padding": "25px",
    },

)
