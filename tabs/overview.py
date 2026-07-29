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


layout = dbc.Container(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3("Siaya County Population Profile (2024/2025)", className="fw-bold mb-4",),
                    dbc.Row(
        [
        # Left: Chart
        dbc.Col(
            [
                html.H5(
                    "Population Distribution",
                    className="fw-bold mb-3"
                ),

                dcc.Graph(
                    id="population-profile-chart",
                    figure=population_figure,
                    config={
                        **svg_download_config,
                        "toImageButtonOptions": {
                            "format": "svg",
                            "filename": "siaya_population_distribution",
                            "height": 700,
                            "width": 1200,
                            "scale": 1,
                        },
                    },
                    style={"height": "540px"},
                ),
            ],
            width=12,
            lg=8,
        ),
        # Right: Context Box
        dbc.Col(
            [
                html.H5(
                    "Context",
                    className="fw-bold mb-3",
                    style={"marginLeft": "35px"}
                ),

                html.Ul(
                    [
                        html.Li("Children under 15 years represent the largest population group in Siaya County."),
                        html.Li("The county's age structure highlights the importance of child health, malaria prevention, and surveillance programs."),
                        html.Li("Population demographics can affect disease burden, healthcare utilization, and public health planning."),
                    ],
                    style={"paddingLeft": "35px","fontSize": "20px","lineHeight": "1.8",},
                ),
            ],
            width=12,
            lg=3,
            style={"marginLeft": "-30px"},
        ),
    ],
    className="align-items-start",
            ),
                    #line breaker
                    html.Hr(style={"height": "3px","backgroundColor": "#adb5bd","border": "none","opacity": "0.5","margin": "25px 0",}),
                    html.H3("Health Conditions Among Children Under 5 Years (2024/2025)", className="fw-bold mb-4",),
                    html.H5("Most Common Outpatient Health Conditions (Under 5 Years)",className="fw-bold mb-3"),
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
                                width=12,
                                lg=8,
                            ),
                    
                            dbc.Col(
                                [
                                    #html.H5("Context",className="fw-bold mb-3",style={"marginLeft": "35px"}),
                                    html.Ul(
                                        [
                                            html.Li("Confirmed malaria was the leading outpatient condition among children under 5, accounting for 114,002 cases (20.7% of all reported conditions)."),
                                            html.Li("Upper respiratory tract infections were the second most common condition, representing 17.8% of all cases."),
                                            html.Li("Malaria and respiratory infections together accounted for nearly 40% of the total disease burden."),
                                            html.Li("The top 10 conditions represented 49.3% of all outpatient visits among children under 5 years."),
                                        ],
                                        style={"paddingLeft": "35px","lineHeight": "1.5","fontSize": "20px",},
                                    ),
                                ],
                                width=12,
                                lg=3,
                                style={"marginLeft": "-30px"},
                            ),
                        ]
                    ),
                    
                    #line breaker
                    html.Hr(style={"height": "3px","backgroundColor": "#adb5bd","border": "none","opacity": "0.5","margin": "25px 0",}),
                        html.H5("Leading Causes of Mortality (Under 5 Years)",className="fw-bold mb-3"), 
                        dcc.Graph(
                            id="under5-mortality-chart",
                            figure=mortality_fig,
                            config={
                                **svg_download_config,
                                "toImageButtonOptions": {
                                    "format": "svg",
                                    "filename": "under5_leading_causes_of_mortality",
                                    "height": 700,
                                    "width": 1200,
                                    "scale": 1,
                                },
                            },
                        ),

                    #line breaker
                    html.Hr(style={"height": "3px","backgroundColor": "#adb5bd","border": "none","opacity": "0.5","margin": "25px 0",}),
                    html.H5("Most Common Outpatient Health Conditions (Over 5 Years)",className="fw-bold mb-3"),
                    
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
                                width=12,
                                lg=8,
                            ),
                    
                            dbc.Col(
                                [
                                    html.H5("Context",className="fw-bold mb-3",style={"marginLeft": "35px"}),
                                    html.Ul(
                                        [
                                            html.Li("Confirmed malaria was the leading outpatient condition among individuals over 5 years, accounting for 444,240 cases (35.2%)."),
                                            html.Li("Malaria and respiratory infections together accounted for more than half of the reported disease burden."),
                                            html.Li("The top 20 conditions represented 80% of all outpatient visits."),
                                        ],
                                        style={"paddingLeft": "35px","lineHeight": "1.8","fontSize": "20px",},
                                    ),
                                ],
                                width=12,
                                lg=3,
                                style={"marginLeft": "-30px"},
                            ),
                        ]
                    ),

                        #line breaker
                        html.Hr(style={"height": "3px","backgroundColor": "#adb5bd","border": "none","opacity": "0.5","margin": "25px 0",}),
                        html.H5(
                            "Leading Causes of Mortality (Over 5 Years)",
                            className="fw-bold mb-3"
                        ),
                        
                        dcc.Graph(
                            id="over5-mortality-chart",
                            figure=over5_mortality_fig,
                            config={
                                "displayModeBar": False,
                                "responsive": True,
                            },
                        ),
                    
                ]#box border
            ),
            className="mt-4 shadow-sm",
        )
    ],
    fluid=True,
    className="px-0",
)
