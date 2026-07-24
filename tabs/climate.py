from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# Empty figures for now
empty_fig = go.Figure()

empty_fig.update_layout(
    template="plotly_white",
    height=350,
    margin=dict(l=20, r=20, t=40, b=20),
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
    annotations=[
        dict(
            text="Data will be added here",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=16)
        )
    ]
)

layout = dbc.Container(

    [

        # map
        html.H4(
            "Interactive Map of Siaya Subcounties",
            className="fw-bold mt-3 mb-3"
        ),

        dbc.Card(
            dbc.CardBody(
                html.Div(
                    "Map Placeholder",
                    style={
                        "height": "500px",
                        "display": "flex",
                        "justifyContent": "center",
                        "alignItems": "center",
                        "fontSize": "24px",
                        "backgroundColor": "#f8f9fa"
                    }
                )
            ),
            className="shadow-sm mb-4"
        ),

        html.Hr(),

        #Temp and rainfall 
        dbc.Row(
            [

                dbc.Col(
                    [
                        html.H5(
                            "Temperature Trend",
                            className="fw-bold mb-3"
                        ),

                        dcc.Graph(
                            figure=empty_fig,
                            config={"displayModeBar": False}
                        ),
                    ],
                    lg=6,
                ),

                dbc.Col(
                    [
                        html.H5(
                            "Rainfall Trend",
                            className="fw-bold mb-3"
                        ),

                        dcc.Graph(
                            figure=empty_fig,
                            config={"displayModeBar": False}
                        ),
                    ],
                    lg=6,
                ),

            ]
        ),

        html.Hr(),

        # NDVI and humidity
        dbc.Row(
            [

                dbc.Col(
                    [
                        html.H5(
                            "NDVI Trend",
                            className="fw-bold mb-3"
                        ),

                        dcc.Graph(
                            figure=empty_fig,
                            config={"displayModeBar": False}
                        ),
                    ],
                    lg=6,
                ),

                dbc.Col(
                    [
                        html.H5(
                            "Humidity Trend",
                            className="fw-bold mb-3"
                        ),

                        dcc.Graph(
                            figure=empty_fig,
                            config={"displayModeBar": False}
                        ),
                    ],
                    lg=6,
                ),

            ]
        ),

    ],

    fluid=True,
)
