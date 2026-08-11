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


# --------------------------------------------------
# Shared tab style
# --------------------------------------------------

tab_style = {
    "flex": "1",
    "textAlign": "center",
    "fontWeight": "500",
    "padding": "14px 8px",
}

active_tab_style = {
    "fontWeight": "700",
}


# --------------------------------------------------
# Tabs
# --------------------------------------------------

overview_tab = dbc.Tab(
    overview.layout,
    label="Overview",
    tab_id="overview-tab",
    tab_style=tab_style,
    active_tab_style=active_tab_style,
)

climate_tab = dbc.Tab(
    climate.layout,
    label="Climate",
    tab_id="climate-tab",
    tab_style=tab_style,
    active_tab_style=active_tab_style,
)

malaria_tab = dbc.Tab(
    malaria.layout,
    label="Malaria",
    tab_id="malaria-tab",
    tab_style=tab_style,
    active_tab_style=active_tab_style,
)

prediction_tab = dbc.Tab(
    prediction.layout,
    label="Prediction Model",
    tab_id="prediction-tab",
    tab_style=tab_style,
    active_tab_style=active_tab_style,
)

description_tab = dbc.Tab(
    description.layout,
    label="Project Description",
    tab_id="description-tab",
    tab_style=tab_style,
    active_tab_style=active_tab_style,
)

about_tab = dbc.Tab(
    about.layout,
    label="Project Contributors",
    tab_id="about-tab",
    tab_style=tab_style,
    active_tab_style=active_tab_style,
)


# --------------------------------------------------
# App Layout
# --------------------------------------------------

app.layout = html.Div(
    [

        # Header
        dbc.Navbar(
            dbc.Container(
                [
                    html.Div(
                        [
                            html.H2(
                                "Siaya County Disease and Climate Monitoring Dashboard",
                                className="mb-1 text-white fw-bold",
                            ),

                            html.P(
                                "Monitoring malaria, climate, and disease trends across Siaya County",
                                className="mb-0 text-white-50",
                            ),
                        ]
                    )
                ],
                fluid=True,
            ),
            color="primary",
            dark=True,
            className="py-4 px-4 shadow-sm",
        ),


        # Full-width navigation tabs
        html.Div(
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
                className="w-100",
                style={
                    "display": "flex",
                    "width": "100%",
                    "backgroundColor": "white",
                },
            ),
            className="bg-white shadow-sm",
        ),


        # Footer
        dbc.Container(
            [
                html.Hr(className="mt-5"),

                html.P(
                    "Siaya County Disease and Climate Monitoring Dashboard",
                    className="text-muted small text-center mb-4",
                ),
            ],
            fluid=True,
            className="px-4",
        ),
    ],
    className="bg-light min-vh-100",
)


if __name__ == "__main__":
    app.run(debug=True, port=8050)
