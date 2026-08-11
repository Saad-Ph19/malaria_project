from dash import Dash, html
import dash_bootstrap_components as dbc

from tabs import overview
from tabs import climate
from tabs import malaria
from tabs import prediction
from tabs import about
from tabs import description


app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.FLATLY],
    title="Siaya County Disease and Climate Monitoring Dashboard",
    suppress_callback_exceptions=True,
)

server = app.server


# -------------------------------------------------
# Tabs
# -------------------------------------------------

overview_tab = dbc.Tab(
    overview.layout,
    label="Overview",
    tab_id="overview-tab",
    tab_class_name="dashboard-tab",
    active_tab_class_name="dashboard-tab-active",
)

climate_tab = dbc.Tab(
    climate.layout,
    label="Climate",
    tab_id="climate-tab",
    tab_class_name="dashboard-tab",
    active_tab_class_name="dashboard-tab-active",
)

malaria_tab = dbc.Tab(
    malaria.layout,
    label="Malaria",
    tab_id="malaria-tab",
    tab_class_name="dashboard-tab",
    active_tab_class_name="dashboard-tab-active",
)

prediction_tab = dbc.Tab(
    prediction.layout,
    label="Prediction Model",
    tab_id="prediction-tab",
    tab_class_name="dashboard-tab",
    active_tab_class_name="dashboard-tab-active",
)

description_tab = dbc.Tab(
    description.layout,
    label="Project Description",
    tab_id="description-tab",
    tab_class_name="dashboard-tab",
    active_tab_class_name="dashboard-tab-active",
)

about_tab = dbc.Tab(
    about.layout,
    label="Project Contributors",
    tab_id="about-tab",
    tab_class_name="dashboard-tab",
    active_tab_class_name="dashboard-tab-active",
)


# -------------------------------------------------
# App Layout
# -------------------------------------------------

app.layout = html.Div(
    [

        # Header
        html.Div(
            [
                dbc.Container(
                    [
                        html.H2(
                            "Siaya County Disease and Climate Monitoring Dashboard",
                            className="dashboard-title",
                        ),
                        html.P(
                            "Monitoring malaria, climate conditions, and disease trends across Siaya County",
                            className="dashboard-subtitle",
                        ),
                    ],
                    fluid=True,
                )
            ],
            className="dashboard-header",
        ),

        # Full-width tab navigation
        html.Div(
            dbc.Container(
                dbc.Tabs(
                    [
                        overview_tab,
                        climate_tab,
                        malaria_tab,
                        prediction_tab,
                        description_tab,
                        about_tab,
                    ],
                    id="main-tabs",
                    active_tab="overview-tab",
                    className="dashboard-tabs",
                ),
                fluid=True,
                className="px-0",
            ),
            className="tabs-wrapper",
        ),

        # Footer
        html.Div(
            [
                html.Hr(className="mb-3"),
                html.P(
                    "Siaya County Disease and Climate Monitoring Dashboard",
                    className="text-muted small text-center mb-3",
                ),
            ],
            className="footer-container",
        ),

    ],
    className="dashboard-page",
)


if __name__ == "__main__":
    app.run(debug=True, port=8050)
