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


overview_tab = dbc.Tab(
    overview.layout,
    label="Overview",
    tab_id="overview-tab",
    style={
    "width": "100%"
    }
)

climate_tab = dbc.Tab(
    climate.layout,
    label="Climate",
    tab_id="climate-tab",
    style={
    "width": "100%"}
)

malaria_tab = dbc.Tab(
    malaria.layout,
    label="Malaria",
    tab_id="malaria-tab",
    style={
    "width": "100%"
}
)

prediction_tab = dbc.Tab(
    prediction.layout,
    label="Prediction Model",
    tab_id="prediction-tab",
    style={
    "width": "100%"
}
)

about_tab = dbc.Tab(
    about.layout,
    label="Project Contributors",
    tab_id="about-tab",
    style={
    "width": "100%"
}
)

description_tab = dbc.Tab(
    description.layout,
    label="Project Description",
    tab_id="description-tab",
    style={
    "width": "100%"
}
)

app.layout = dbc.Container(
    [
        dbc.Navbar(
            dbc.Container(
                [
                    html.H2(
                        "Siaya County Disease & Climate Monitoring Dashboard",
                        className="mb-0 text-white fw-bold"
                    )
                ],
                fluid=True,
            ),
            color="primary",
            dark=True,
            className="shadow-sm mb-3 py-3",
        ),

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
                "fontSize": "1.05rem",
                "fontWeight": "600",
            },
        
            active_tab_style={
                "backgroundColor": "#0d6efd",
                "color": "white",
                "fontWeight": "700",
                "borderColor": "#0d6efd",
            },
        
            tab_style={
                "padding": "14px",
                "fontSize": "1.05rem",
            },
        ),

        html.Hr(className="mt-5"),

        html.P(
            "Siaya County Disease and Climate Monitoring Dashboard",
            className="text-muted small text-center mb-3",
        ),
    ],
    fluid=True,
style={
    "backgroundColor": "#f8fafc",
    "minHeight": "100vh",
},
)


if __name__ == "__main__":
    app.run(debug=True, port=8050)
