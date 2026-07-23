from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

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

# UNDER-5 DISEASE PIE CHART
grand_total = 551550
disease_df = pd.DataFrame({
    "Disease": [
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
        "Other injuries",
        "Anaemia",
        "Intestinal worms",
        "Burns",
        "Severe pneumonia",
        "Urinary Tract Infections",
        "Diarrhoea (some dehydration)",
        "Presumed Tuberculosis",
        "Dental Disorders",
        "Malnutrition"
    ],
    "Cases": [
        114002,98302,17771,12534,7432,
        6333,5337,4643,2840,2741,
        2136,2024,1507,1438,1407,
        1399,1106,887,877,788
    ]
})

# Largest to smallest
disease_df = disease_df.sort_values(
    "Cases",
    ascending=False
)

disease_df["Percent"] = (
    disease_df["Cases"] / grand_total * 100
).round(1)

disease_pie_figure = go.Figure(
    go.Pie(
        labels=disease_df["Disease"],
        values=disease_df["Cases"],
        hole=0.4,
        sort=False,
        textinfo="none",
        customdata=disease_df["Percent"],
        hovertemplate=
            "<b>%{label}</b><br>" +
            "Cases: %{value:,}<br>" +
            "Percent of total: %{customdata}%<extra></extra>"
    )
)

disease_pie_figure.update_layout(
    template="plotly_white",
    height=500,
    margin=dict(l=20, r=20, t=20, b=20),
    legend=dict(
        orientation="v",
        y=1,
        x=1.02
    )
)

layout = dbc.Container(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3(
                        "Siaya County Population Profile, 2024/2025",
                        className="fw-bold mb-4",
                    ),

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
                        "displayModeBar": False,
                        "responsive": True,
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
                    className="fw-bold mb-3"
                ),

                html.Ul(
                    [
                        html.Li(
                            "Children under 15 years represent the largest population group in Siaya County."
                        ),
                        html.Li(
                            "The county's age structure highlights the importance of child health, malaria prevention, and surveillance programs."
                        ),
                        html.Li(
                            "Population demographics can affect disease burden, healthcare utilization, and public health planning."
                        ),
                    ],
                    style={
                        "paddingLeft": "20px",
                        "fontSize": "15px",
                        "lineHeight": "1.8",
                    },
                ),
            ],
            width=12,
            lg=3,
            style={"marginLeft": "-30px"},
        ),
    ],
    className="align-items-start",
            ),
                            html.Hr(
                style={
                    "height": "3px",
                    "backgroundColor": "#adb5bd",
                    "border": "none",
                    "opacity": "0.5",
                    "margin": "25px 0",
                }
            ),

html.H5(
    "Top Twenty Commonest Outpatient Health Conditions (Under 5 Years)",
    className="fw-bold mb-3"
),

dbc.Row(
    [
        dbc.Col(
            dcc.Graph(
                id="under5-disease-chart",
                figure=disease_pie_figure,
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
                html.H5(
                    "Context",
                    className="fw-bold mb-3",
                ),

                html.Ul(
                    [
                        html.Li(
                            "Confirmed malaria was the leading outpatient condition among children under 5, accounting for 114,002 cases (20.7% of all reported conditions)."
                        ),
                        html.Li(
                            "Upper respiratory tract infections were the second most common condition, representing 17.8% of all cases."
                        ),
                        html.Li(
                            "Malaria and respiratory infections together accounted for nearly 40% of the total disease burden."
                        ),
                        html.Li(
                            "The top twenty conditions represented 51.8% of all outpatient visits among children under 5 years."
                        ),
                    ],
                    style={
                        "paddingLeft": "20px",
                        "lineHeight": "1.8",
                        "fontSize": "15px",
                    },
                ),
            ],
            width=12,
            lg=3,
            style={"marginLeft": "-30px"},
        ),
    ]
),
                ]
            ),
            className="mt-4 shadow-sm",
        )
    ],
    fluid=True,
    className="px-0",
)
