# app.py

from dash import Dash, html
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    title="Siaya County Disease and Climate Monitoring Dashboard",
    suppress_callback_exceptions=True,
)

# Render and Gunicorn need access to the Flask server
server = app.server


# Place holder
def placeholder_card(title, description):

    return dbc.Card(
        dbc.CardBody(
            [
                html.H4(title, className="card-title"),
                html.P(description, className="text-muted"),
                html.Hr(),
                html.Div(
                    "Visualization or dashboard content will be added here.",
                    className="text-center text-secondary py-5",
                ),
            ]
        ),
        className="mt-4 shadow-sm",
    )


# Tab content
overview_tab = dbc.Tab(
    label="Overview",
    tab_id="overview-tab",
    children=[
        placeholder_card(
            "Project Overview",
            "This section will provide a summary of the malaria project.",
        )
    ],
)

climate_tab = dbc.Tab(
    label="Climate",
    tab_id="climate-tab",
    children=[
        placeholder_card(
            "Climate Data",
            "Temperature, precipitation, and humidity visualizations will appear here.",
        )
    ],
)

malaria_tab = dbc.Tab(
    label="Malaria",
    tab_id="malaria-tab",
    children=[
        placeholder_card(
            "Malaria Data",
            "Malaria cases, rates, and trends will appear here.",
        )
    ],
)

model_tab = dbc.Tab(
    label="Prediction Model",
    tab_id="model-tab",
    children=[
        placeholder_card(
            "Malaria Prediction Model",
            "Prediction results and model evaluation metrics will appear here.",
        )
    ],
)

about_tab = dbc.Tab(
    label="About",
    tab_id="about-tab",
    children=[
        placeholder_card(
            "About the Project",
            "Project description, collaborators, data sources, and limitations will appear here.",
        )
    ],
)


# App layout
app.layout = dbc.Container(
    [
        # Header
        dbc.Navbar(
            dbc.Container(
                [
                    html.Div(
                        [
                            html.H3(
                                "Malaria Analytics Dashboard",
                                className="mb-0 text-white fw-bold",
                            ),
                            html.Small(
                                "Climate, environmental, and malaria surveillance data",
                                className="text-white-50",
                            ),
                        ]
                    )
                ],
                fluid=True,
            ),
            color="primary",
            dark=True,
            className="mb-4 px-3 py-3",
        ),

        # Dashboard introduction
        dbc.Row(
            dbc.Col(
                [
                    html.H4("Dashboard"),
                    html.P(
                        "Use the tabs below to navigate between dashboard sections.",
                        className="text-muted",
                    ),
                ],
                width=12,
            )
        ),

        # Tabs only
        dbc.Tabs(
            [
                overview_tab,
                climate_tab,
                malaria_tab,
                model_tab,
                about_tab,
            ],
            id="main-tabs",
            active_tab="overview-tab",
            className="mt-3",
        ),

        # Footer
        html.Hr(className="mt-5"),
        html.P(
            "Malaria Analytics Dashboard",
            className="text-muted small text-center mb-3",
        ),
    ],
    fluid=True,
)


# Main
if __name__ == "__main__":
    app.run(debug=True, port=8050)
