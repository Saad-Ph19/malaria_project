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
                                    "Fever Cases",
                                    className="text-muted"
                                ),
                                html.H3(
                                    f"{fever_cases:,}",
                                    className="fw-bold text-primary mb-0"
                                ),
                            ]
                        ),
                        className="border-0 shadow-sm",
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
                                    "Tested",
                                    className="text-muted"
                                ),
                                html.H3(
                                    f"{tested:,}",
                                    className="fw-bold text-success mb-0"
                                ),
                            ]
                        ),
                        className="border-0 shadow-sm",
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
                                    "RDT Positive",
                                    className="text-muted"
                                ),
                                html.H3(
                                    f"{rdt_positive:,}",
                                    className="fw-bold text-danger mb-0"
                                ),
                            ]
                        ),
                        className="border-0 shadow-sm",
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
                                    "ACT Treated",
                                    className="text-muted"
                                ),
                                html.H3(
                                    f"{treated:,}",
                                    className="fw-bold text-success mb-0"
                                ),
                            ]
                        ),
                        className="border-0 shadow-sm",
                    ),

                    lg=3,
                    md=6,
                    className="mb-3",

                ),

            ],

            className="mb-4",

        ),

        # =====================================================
        # SANKEY SECTION
        # =====================================================

        dbc.Card(

            dbc.CardBody(

                [

                    html.H4(
                        "Community Malaria Surveillance Cascade",
                        className="fw-bold mb-1",
                    ),

                    html.P(
                        "Patient flow from reported fever cases through malaria testing and treatment.",
                        className="text-muted mb-4",
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

                                lg=8,

                            ),

                            dbc.Col(

                                dbc.Card(

                                    dbc.CardBody(

                                        [

                                            html.H6(
                                                "Key Findings",
                                                className="fw-bold text-primary"
                                            ),

                                            html.Ul(

                                                [

                                                    html.Li(
                                                        "Most fever cases proceeded to diagnostic testing."
                                                    ),

                                                    html.Li(
                                                        "A large proportion of tested individuals were RDT positive."
                                                    ),

                                                    html.Li(
                                                        "Treatment coverage among confirmed cases was high."
                                                    ),

                                                    html.Li(
                                                        "Only a small number of confirmed cases did not receive ACT treatment."
                                                    ),

                                                ],

                                                style={
                                                    "lineHeight": "1.8",
                                                    "fontSize": "15px",
                                                },

                                            ),

                                        ]

                                    ),

                                    style={
                                        "backgroundColor": "#f8fafc",
                                        "border": "1px solid #e2e8f0",
                                        "borderRadius": "12px",
                                    },

                                ),

                                lg=4,

                            ),

                        ]

                    ),

                ]

            ),

            className="border-0 shadow-sm mb-4",

        ),

        # =====================================================
        # INTERPRETATION
        # =====================================================

        dbc.Card(

            dbc.CardBody(

                [

                    html.H5(
                        "Interpretation",
                        className="fw-bold mb-3"
                    ),

                    html.P(
                        "This visualization summarizes the community malaria surveillance pathway. "
                        "It highlights progression from fever presentation through testing, diagnosis, "
                        "and treatment, allowing identification of potential gaps in testing coverage "
                        "or case management.",
                        className="text-muted mb-0",
                    ),

                ]

            ),

            className="border-0 shadow-sm",

        ),

    ],

    fluid=True,

    style={
        "backgroundColor": "#f8fafc",
        "padding": "20px",
        "minHeight": "100vh",
    },

)

