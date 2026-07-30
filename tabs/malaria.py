from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go


# ------------------------------------------------------------------
# TEMPORARY VALUES
# Replace these with your real calculations later
# ------------------------------------------------------------------

fever_cases = 10000
tested = 8500
not_tested = 1500

rdt_positive = 5200
rdt_negative = 3300

treated = 5000
not_treated = 200


# ------------------------------------------------------------------
# SANKEY DIAGRAM
# ------------------------------------------------------------------

sankey_fig = go.Figure(
    go.Sankey(
        arrangement="snap",
        node=dict(
            pad=25,
            thickness=25,
            line=dict(color="rgba(0,0,0,0.2)", width=1),
            label=[
                "Fever Cases",
                "Tested",
                "Not Tested",
                "RDT Positive",
                "RDT Negative",
                "Treated (ACT)",
                "Not Treated"
            ],
            color=[
                "#1f77b4",  # blue
                "#aec7e8",  # light blue
                "#ffbb78",  # light orange
                "#ff7f0e",  # orange
                "#f4a261",  # orange-light
                "#2ca02c",  # green
                "#d62728",  # red
            ],
        ),
        link=dict(
            source=[
                0, 0,      # Fever -> Tested, Not Tested
                1, 1,      # Tested -> Positive, Negative
                3, 3       # Positive -> Treated, Not Treated
            ],
            target=[
                1, 2,
                3, 4,
                5, 6
            ],
            value=[
                tested,
                not_tested,
                rdt_positive,
                rdt_negative,
                treated,
                not_treated
            ],
            color="rgba(180,180,180,0.45)",
        ),
    )
)

sankey_fig.update_layout(
    title="Community Malaria Surveillance Cascade",
    template="plotly_white",
    height=650,
    font_size=15,
    margin=dict(l=20, r=20, t=60, b=20),
)


# ------------------------------------------------------------------
# PAGE LAYOUT
# ------------------------------------------------------------------

layout = dbc.Container(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3(
                        "Community Malaria Surveillance",
                        className="fw-bold mb-4",
                    ),

                    dbc.Row(
                        [
                            dbc.Col(
                                dcc.Graph(
                                    figure=sankey_fig,
                                    config={
                                        "displayModeBar": False,
                                        "responsive": True,
                                    },
                                ),
                                lg=9,
                            ),

                            dbc.Col(
                                [
                                    html.H5(
                                        "Key Insights",
                                        className="fw-bold mb-3",
                                    ),

                                    html.Ul(
                                        [
                                            html.Li(
                                                "Most reported fever cases underwent diagnostic testing."
                                            ),
                                            html.Li(
                                                "A substantial proportion of tested individuals were RDT positive."
                                            ),
                                            html.Li(
                                                "Most RDT-positive cases received ACT treatment."
                                            ),
                                            html.Li(
                                                "The visualization summarizes the community malaria testing and treatment pathway."
                                            ),
                                        ],
                                        style={
                                            "lineHeight": "1.8",
                                            "fontSize": "18px",
                                        },
                                    ),
                                ],
                                lg=3,
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

