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
        dbc.Card(
            dbc.CardBody(
                [
                    # Title
                    html.H3(
                        "Project Contributors",
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

                    # Next paragraph
                    html.P("This work is conducted through a collaborative partnership involving: ",
                        style={
                            "fontSize": "20px",
                            "lineHeight": "1.8",
                            "color": TEXT,
                            "marginBottom": "20px",
                        },
                    ),
                    
                    html.Ul([
                        html.Li([
                            html.Strong("Principal Investigators: "),
                            "Felix Pabon-Rodriguez (IUSM) and George Ayodo (JOOUST)"]),
                        html.Li([
                            html.Strong("Co-Investigator: "),
                            "Yan Zhuang (IUI)"]),
                        html.Li([
                            html.Strong("Indiana University Research Assistants: "),
                            "Saad Pharis, Mridul Banik, Nathaniel Maxey, and Taliyah Griffin"]),
                        html.Li([
                            html.Strong("Siaya County Public Health Officer: "),
                            "Moses Ombuoro"]),
                        html.Li([
                            html.Strong("App Developer: "),
                            "Saad Pharis"]),
                        ], 
                            className="text-muted",
                            style={                                            
                                "fontSize": "20px",
                                "lineHeight": "1.8",
                                "color": TEXT,
                                "marginBottom": "20px",
                                "paddingLeft": "45px",
                            }
                    ),
                    
                    html.P("The project integrates data from:",className="text-muted",
                           style={                            
                               "fontSize": "20px",
                                "lineHeight": "1.8",
                                "color": TEXT,
                                "marginBottom": "20px",
                           }
                    ),
                    
                    html.Ul([
                        html.Li("Kenya Health Information System (KHIS)"),
                        html.Li("Google Earth spatial datasets"),
                        html.Li("Climate and environmental information supporting geospatial disease surveillance"),
                    ], className="text-muted", 
                            style={
                                "fontSize": "20px",
                                "lineHeight": "1.8",
                                "color": TEXT,
                                "marginBottom": "20px",
                                "paddingLeft": "45px",
                            }
                    ),
                    html.P("In case of questions and/or requests, please contact PI Felix Pabon-Rodriguez via email at fpabonr@iu.edu.",className="text-muted",
                           style={
                            "fontSize": "20px",
                            "lineHeight": "1.8",
                            "color": TEXT,
                            "marginBottom": "20px",
                           }
                    ),
                ]
            ),
            style=CARD_STYLE,
            className="mb-4",
        )
    ],
    fluid=True,
    style={
        "backgroundColor": PAGE_BG,
        "padding": "24px",
        "minHeight": "80vh",
    },
)
