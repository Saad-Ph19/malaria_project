from dash import html
import dash_bootstrap_components as dbc


#Theme colors 
PRIMARY = "#274C77"
TEXT = "#1F2937"
TEXT_MUTED = "#6B7280"
BORDER = "#DCE3EA"
PAGE_BG = "#F5F7F9"
CARD_BG = "#FFFFFF"
PANEL_BG = "#F8FAFC"


CARD_STYLE = {
    "backgroundColor": CARD_BG,
    "border": f"1px solid {BORDER}",
    "borderRadius": "10px",
    "boxShadow": "0 2px 8px rgba(15, 23, 42, 0.05)",
}


# =========================================================
# LAYOUT
layout = dbc.Container(
    [
        # PROJECT DESCRIPTION
        dbc.Card(
            dbc.CardBody(
                [
                    # Title
                    html.H3(
                        "Project Description",
                        className="fw-bold mb-2",
                        style={
                            "color": PRIMARY,
                            "fontSize": "28px",
                        },
                    ),

                    # Small divider under title
                    html.Div(
                        style={
                            "width": "55px",
                            "height": "3px",
                            "backgroundColor": PRIMARY,
                            "borderRadius": "2px",
                            "marginBottom": "24px",
                        }
                    ),


                    # Main description
                    html.Div(
                        [
                            html.P("The Siaya County Disease and Climate Monitoring Dashboard is an interactive geospatial surveillance platform that integrates malaria epidemiology, climate, and health system data to support infectious disease research and public health decision-making in western Kenya. ",
                                style={
                                    "fontSize": "20px",
                                    "lineHeight": "1.8",
                                    "color": TEXT,
                                    "marginBottom": "20px",
                                },
                            ),

                            html.P("Beyond tracking malaria incidence, the dashboard visualizes the distribution and availability of key malaria control resources, including rapid diagnostic tests (RDTs), artemisinin-based combination therapies (ACTs), and insecticide-treated bed nets (ITNs), allowing users to evaluate disease burden alongside healthcare resource allocation and intervention coverage. ",
                                style={
                                    "fontSize": "20px",
                                    "lineHeight": "1.8",
                                    "color": TEXT,
                                    "marginBottom": "20px",
                                },
                            ),

                            html.P("This integrated approach supports investigations into malaria and other febrile illnesses by identifying transmission hotspots, assessing preparedness, and exploring the environmental and operational factors influencing disease dynamics. The inclusion of commodity stock monitoring aligns with WHO recommendations for integrated malaria surveillance systems that combine epidemiologic, environmental, and supply chain data. ",
                                style={
                                    "fontSize": "20px",
                                    "lineHeight": "1.8",
                                    "color": TEXT,
                                    "marginBottom": "20px",
                                },
                            ),

                            html.P("This project is in collaboration between researchers from Indiana University School of Medicine [IUSM] and Indiana University Indianapolis [IUI] (Indianapolis, Indiana, USA), Jaramogi Oginga Odinga University of Science and Technology [JOOUST] (Bondo, Kenya), and Siaya County Public Health Department. See the Project Contributors tab for more information. ",
                                style={
                                    "fontSize": "20px",
                                    "lineHeight": "1.8",
                                    "color": TEXT,
                                    "marginBottom": "20px",
                                },
                            ),

                            html.H4(
                                "Key Features: ",
                                className="fw-bold mb-3",
                                style={"color": TEXT, "fontSize": "25px",},
                            ),
        
                            html.Div(
                                [
                                    html.Ul(
                                        [
                                            html.Li("Malaria surveillance and disease burden monitoring"),
                                            html.Li("Climate and environmental data integration"),
                                            html.Li("Commodity stock monitoring (RDTs, ACTs, ITNs)"),
                                            html.Li("Interactive visualizations and forecasting tools"),
                                            html.Li("Decision-support for public health planning"),
                                        ],
        
                                        style={
                                            "fontSize": "18px",
                                            "lineHeight": "2",
                                            "color": TEXT,
                                            "marginBottom": "0",
                                            "paddingLeft": "22px",
                                        },
                                    ),
                                ],
                            ),
                        ],
                        #style={"maxWidth": "1150px",},
                    ),
                ],
                style={"padding": "30px",},
            ),
            style=CARD_STYLE,
            className="mb-4",
        ),
    ],
    fluid=True,
    style={
        "backgroundColor": PAGE_BG,
        "padding": "24px",
        "minHeight": "100vh",
    },
)
