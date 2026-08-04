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

# ==========================================================
# TABS
# ==========================================================

overview_tab = dbc.Tab(
    overview.layout,
    label="Overview",
    tab_id="overview-tab",
    label_style={"fontSize": "1.15rem", "fontWeight": "600"},
)

climate_tab = dbc.Tab(
    climate.layout,
    label="Climate",
    tab_id="climate-tab",
    label_style={"fontSize": "1.15rem", "fontWeight": "600"},
)

malaria_tab = dbc.Tab(
    malaria.layout,
    label="Malaria",
    tab_id="malaria-tab",
    label_style={"fontSize": "1.15rem", "fontWeight": "600"},
)

prediction_tab = dbc.Tab(
    prediction.layout,
    label="Prediction Model",
    tab_id="prediction-tab",
    label_style={"fontSize": "1.15rem", "fontWeight": "600"},
)

description_tab = dbc.Tab(
    description.layout,
    label="Project Description",
    tab_id="description-tab",
    label_style={"fontSize": "1.15rem", "fontWeight": "600"},
)

about_tab = dbc.Tab(
    about.layout,
    label="Project Contributors",
    tab_id="about-tab",
    label_style={"fontSize": "1.15rem", "fontWeight": "600"},
)

# ==========================================================
# APP LAYOUT
# ==========================================================

app.layout = dbc.Container(

    [

        # --------------------------------------------------
        # NAVBAR
        # --------------------------------------------------

        dbc.Navbar(

            dbc.Container(

                [

                    html.H2(
                        "Siaya County Disease & Climate Monitoring Dashboard",
                        className="mb-0 text-white fw-bold"
                    ),

                ],

                fluid=True,

            ),

            color="primary",
            dark=True,
            className="shadow-sm mb-3 py-3",

        ),

        # --------------------------------------------------
        # TABS CONTAINER
        # --------------------------------------------------

        dbc.Card(

            dbc.CardBody(

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

                    class_name="w-100",

                    style={
                        "fontSize": "1.15rem",
                        "fontWeight": "600",
                    },

                )

            ),

            className="border-0 shadow-sm mb-4"

        ),

        # --------------------------------------------------
        # FOOTER
        # --------------------------------------------------

        html.Hr(className="mt-4"),

        html.P(
            "Department of Biomedical Engineering & Informatics | Indiana University",
            className="text-muted text-center small py-2"
        ),

    ],

    fluid=True,

    style={
        "backgroundColor": "#f8fafc",
        "minHeight": "100vh",
        "padding": "0",
    },

)

if __name__ == "__main__":
    app.run(debug=True, port=8050)
