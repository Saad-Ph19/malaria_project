from dash import Dash, html
import dash_bootstrap_components as dbc

from tabs import overview
from tabs import climate
from tabs import malaria
from tabs import prediction
from tabs import about


app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    title="Siaya County Disease and Climate Monitoring Dashboard",
    suppress_callback_exceptions=True,
)

server = app.server


overview_tab = dbc.Tab(
    overview.layout,
    label="Overview",
    tab_id="overview-tab",
)

climate_tab = dbc.Tab(
    climate.layout,
    label="Climate",
    tab_id="climate-tab",
)

malaria_tab = dbc.Tab(
    malaria.layout,
    label="Malaria",
    tab_id="malaria-tab",
)

prediction_tab = dbc.Tab(
    prediction.layout,
    label="Prediction Model",
    tab_id="prediction-tab",
)

about_tab = dbc.Tab(
    about.layout,
    label="About",
    tab_id="about-tab",
)


app.layout = dbc.Container(
    [
        dbc.Navbar(
            dbc.Container(
                html.H3(
                    "Siaya County Disease and Climate Monitoring Dashboard",
                    className="mb-0 text-white fw-bold",
                ),
                fluid=True,
            ),
            color="primary",
            dark=True,
            className="mb-4 px-3 py-3",
        ),

        dbc.Tabs(
            [
                overview_tab,
                climate_tab,
                malaria_tab,
                prediction_tab,
                about_tab,
            ],
            id="main-tabs",
            active_tab="overview-tab",
            className="mt-3",
        ),

        html.Hr(className="mt-5"),

        html.P(
            "Siaya County Disease and Climate Monitoring Dashboard",
            className="text-muted small text-center mb-3",
        ),
    ],
    fluid=True,
)


if __name__ == "__main__":
    app.run(debug=True, port=8050)
