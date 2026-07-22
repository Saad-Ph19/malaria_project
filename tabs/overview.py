from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

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
)
                html.Hr(style={"borderTop": "2px solid #dee2e6","marginTop": "20px","marginBottom": "20px",}),
                ]
            ),
            className="mt-4 shadow-sm",
        )
    ],
    fluid=True,
    className="px-0",
)
