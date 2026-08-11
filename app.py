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

#Colors
HEADER_COLOR = "#24557A"       # Muted professional blue
ACTIVE_COLOR = "#2C7DA0"       # Selected tab color
TEXT_COLOR = "#495057"         # Unselected tab text
PAGE_COLOR = "#F8F9FA"         # Light page background


# Shared Tab Styles
tab_style = {
    "flex": "1",
    "textAlign": "center",
    "fontWeight": "500",
    "fontSize": "18px",
    "padding": "18px 8px",
    "backgroundColor": "white",
    "color": TEXT_COLOR,
    # Remove all Bootstrap tab borders
    "borderTop": "none",
    "borderLeft": "none",
    "borderRight": "none",
    "borderBottom": "4px solid transparent",
    # Remove rounded corners
    "borderRadius": "0",
}

active_tab_style = {
    "fontWeight": "700",
    "fontSize": "18px",
    "backgroundColor": "white",
    "color": ACTIVE_COLOR,
    # Remove top, left, and right borders
    "borderTop": "none",
    "borderLeft": "none",
    "borderRight": "none",
    # only show the bottom blue line
    "borderBottom": f"4px solid {ACTIVE_COLOR}",
    # Remove rounded corners
    "borderRadius": "0",
}

# Tabs
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

# Main Layout
app.layout = html.Div(
    [
        # HEADER
        dbc.Navbar(
            dbc.Container(
                [
                    html.Div(
                        [
                            # Dashboard title
                            html.H2(
                                "Siaya County Disease and Climate Monitoring Dashboard",
                                className="mb-1 fw-bold",
                                style={
                                    "color": "white",
                                    "fontSize": "30px",
                                },
                            ),

                            # Dashboard subtitle
                            html.P(
                                "Monitoring malaria, climate, and disease trends across Siaya County",
                                className="mb-0",
                                style={
                                    "color": "rgba(255,255,255,0.80)",
                                    "fontSize": "16px",
                                },
                            ),

                        ]
                    )
                ],
                fluid=True,
            ),
            style={"backgroundColor": HEADER_COLOR,},
            dark=True,
            className="py-4 px-4",
        ),
        
        # NAVIGATION BAR
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
                style={"display": "flex","width": "100%","backgroundColor": "white","margin": "0",},
            ),

            style={
                "width": "100%",
                "backgroundColor": "white",
                "borderBottom": "1px solid #DEE2E6",
                # Very subtle separation from page content
                "boxShadow": "0 2px 5px rgba(0,0,0,0.06)",
            },
        ),

        # FOOTER
        dbc.Container(
            [
                html.Hr(
                    className="mt-5",
                    style={
                        "borderColor": "#DEE2E6",
                    },
                ),

                html.P(
                    "Siaya County Disease and Climate Monitoring Dashboard",
                    className="text-muted small text-center mb-4",
                ),
            ],
            fluid=True,
            className="px-4",
        ),
    ],
    style={"backgroundColor": PAGE_COLOR,"minHeight": "100vh",},
)


if __name__ == "__main__":
    app.run(
        debug=True,
        port=8050,
    )
