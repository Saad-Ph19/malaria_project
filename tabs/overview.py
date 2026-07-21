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
    height=480,
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
                            # Visualization
                            dbc.Col(
                                dcc.Graph(
                                    id="population-profile-chart",
                                    figure=population_figure,
                                    config={
                                        "displayModeBar": False,
                                        "responsive": True,
                                    },
                                    style={"height": "500px"},
                                ),
                                width=12,
                                lg=8,
                            ),

                            # Explanation
                            dbc.Col(
                                html.Div(
                                    [
                                        html.H4(
                                            "Population Context",
                                            className="ps-lg-2 pt-0"
                                        ),

                                        html.P(
                                            [
                                                "Siaya County has a projected population of ",
                                                html.Strong("1,150,131 people"),
                                                " for 2024/2025, living in approximately ",
                                                html.Strong("287,533 households"),
                                                ".",
                                            ]
                                        ),

                                        html.P(
                                            [
                                                "Approximately ",
                                                html.Strong("475,536 residents"),
                                                " are under 15 years of age.",
                                            ]
                                        ),

                                        html.P(
                                            (
                                                "Children under five are an important group "
                                                "for malaria monitoring because they are "
                                                "especially vulnerable to severe malaria."
                                            )
                                        ),

                                        html.P(
                                            (
                                                "These population estimates provide context "
                                                "for interpreting malaria case counts, "
                                                "incidence rates, health-service demand, "
                                                "and prevention needs."
                                            )
                                        ),

                                        html.Hr(),

                                        html.Small(
                                            (
                                                "The age categories overlap and should not "
                                                "be added together. For example, children "
                                                "under five are included in the population "
                                                "under 15."
                                            ),
                                            className="text-muted",
                                        ),
                                    ],
                                    className="ps-lg-4 pt-3 pt-lg-0",
                                ),
                                width=12,
                                lg=4,
                            ),
                        ],
                        className="align-items-center",
                    ),
                ]
            ),
            className="mt-4 shadow-sm",
        )
    ],
    fluid=True,
    className="px-0",
)
