from dash import html
import dash_bootstrap_components as dbc

layout = dbc.Container(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    html.H4("Climate Data"),
                    html.P(
                        "Temperature, precipitation, and humidity visualizations will appear here.",
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
