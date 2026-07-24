from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# Placeholder figure
empty_fig = go.Figure()

empty_fig.update_layout(
    template="plotly_white",
    height=350,
    margin=dict(l=20, r=20, t=20, b=20),
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
    annotations=[
        dict(
            text="Select a Subcounty",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=18)
        )
    ]
)

layout = dbc.Container(

    [

        # =====================================================
        # PAGE TITLE
        # =====================================================

        html.H3(
            "Climate and Environmental Conditions",
            className="fw-bold mb-4"
        ),

        # =====================================================
        # SUBCOUNTY DROPDOWN
        # =====================================================

        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label(
                            "Select Subcounty",
                            className="fw-bold mb-2"
                        ),

                        dcc.Dropdown(
                            id="climate-subcounty-dropdown",
                            options=[
                                {"label": "Alego Usonga", "value": "Alego Usonga Sub County"},
                                {"label": "Bondo", "value": "Bondo Sub County"},
                                {"label": "Gem", "value": "Gem Sub County"},
                                {"label": "Rarieda", "value": "Rarieda Sub County"},
                                {"label": "Ugenya", "value": "Ugenya Sub County"},
                                {"label": "Ugunja", "value": "Ugunja Sub County"},
                            ],
                            value="Alego Usonga Sub County",
                            clearable=False,
                        ),
                    ],
                    lg=4,
                ),
            ],
            className="mb-4",
        ),

        html.Hr(),

        # =====================================================
        # TEMPERATURE + RAINFALL
        # =====================================================

        dbc.Row(
            [

                dbc.Col(
                    [
                        html.H5(
                            "Average Temperature",
                            className="fw-bold mb-3"
                        ),

                        dcc.Graph(
                            id="temperature-chart",
                            figure=empty_fig,
                            config={"displayModeBar": False},
                        ),
                    ],
                    lg=6,
                ),

                dbc.Col(
                    [
                        html.H5(
                            "Monthly Rainfall",
                            className="fw-bold mb-3"
                        ),

                        dcc.Graph(
                            id="rainfall-chart",
                            figure=empty_fig,
                            config={"displayModeBar": False},
                        ),
                    ],
                    lg=6,
                ),

            ]
        ),

        html.Hr(),

        # =====================================================
        # NDVI + HUMIDITY
        # =====================================================

        dbc.Row(
            [

                dbc.Col(
                    [
                        html.H5(
                            "NDVI",
                            className="fw-bold mb-3"
                        ),

                        dcc.Graph(
                            id="ndvi-chart",
                            figure=empty_fig,
                            config={"displayModeBar": False},
                        ),
                    ],
                    lg=6,
                ),

                dbc.Col(
                    [
                        html.H5(
                            "Relative Humidity",
                            className="fw-bold mb-3"
                        ),

                        dcc.Graph(
                            id="humidity-chart",
                            figure=empty_fig,
                            config={"displayModeBar": False},
                        ),
                    ],
                    lg=6,
                ),

            ]
        ),

    ],

    fluid=True,
)
