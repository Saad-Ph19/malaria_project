from dash import html
import dash_bootstrap_components as dbc


layout = dbc.Container(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H4("Malaria Prediction Model"),
                    html.P(
                        "Prediction results and model evaluation metrics will appear here.",
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
