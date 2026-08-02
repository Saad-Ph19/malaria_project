from dash import html
import dash_bootstrap_components as dbc

layout = dbc.Container(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H3("Project Description", className="mb-3"),

                    html.P(
                        "This dashboard provides an overview of malaria surveillance "
                        "data, climate indicators, and predictive analytics for "
                        "Rarieda Sub-County, Kenya. It integrates disease trends, "
                        "environmental variables, and forecasting models to support "
                        "public health decision-making and improve malaria monitoring.",
                        className="text-muted",
                    ),
                ]
            ),
            className="mt-4 shadow-sm",
        )
    ],
    fluid=True,
    className="px-0",
)
