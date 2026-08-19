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
                        "Malaria Prediction Model",
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
                    html.P("Prediction results and model evaluation metrics will appear here. ",
                        style={
                            "fontSize": "20px",
                            "lineHeight": "1.8",
                            "color": TEXT,
                            "marginBottom": "20px",
                        },
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
        "minHeight": "75vh",
    },
)

