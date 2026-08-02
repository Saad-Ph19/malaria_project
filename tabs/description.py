from dash import html
import dash_bootstrap_components as dbc

layout = dbc.Container(
    [

        dbc.Card(
            dbc.CardBody(

                [

                    html.H2(
                        "Malaria Surveillance & Forecasting Dashboard",
                        className="fw-bold mb-2 text-primary"
                    ),

                    html.P(
                        "Siaya County, Kenya",
                        className="text-muted mb-4"
                    ),

                    html.Hr(),

                    html.P(
                        "This dashboard integrates malaria surveillance, climate, "
                        "environmental, and health system data to support evidence-based "
                        "decision making. Interactive visualizations provide insights into "
                        "disease burden, diagnostic testing, treatment coverage, commodity "
                        "availability, and forecasting indicators across subcounties.",
                        className="lead"
                    ),

                    dbc.Row(

                        [

                            dbc.Col(

                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.H5("Surveillance"),
                                            html.P(
                                                "Monitor fever cases, malaria testing, and confirmed infections.",
                                                className="text-muted mb-0"
                                            )
                                        ]
                                    ),
                                    className="border-0 bg-light h-100"
                                ),

                                md=4
                            ),

                            dbc.Col(

                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.H5("Climate & Environment"),
                                            html.P(
                                                "Explore rainfall, temperature, humidity, and environmental risk factors.",
                                                className="text-muted mb-0"
                                            )
                                        ]
                                    ),
                                    className="border-0 bg-light h-100"
                                ),

                                md=4
                            ),

                            dbc.Col(

                                dbc.Card(
                                    dbc.CardBody(
                                        [
                                            html.H5("Forecasting"),
                                            html.P(
                                                "Support planning through predictive analytics and early warning indicators.",
                                                className="text-muted mb-0"
                                            )
                                        ]
                                    ),
                                    className="border-0 bg-light h-100"
                                ),

                                md=4
                            ),

                        ],

                        className="mt-3"

                    )

                ]

            ),

            className="shadow-sm border-0 mt-4",
            style={
                "borderRadius": "18px"
            }

        )

    ],

    fluid=True,

    style={
        "backgroundColor": "#f8fafc",
        "padding": "20px",
        "minHeight": "100vh"
    }

)
