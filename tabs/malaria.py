from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import glob
import pandas as pd

# import data

files = glob.glob("Malaria_Data/*.xlsx")
print("Files found:")
print(files)

df = pd.concat(
    [pd.read_excel(f) for f in files],
    ignore_index=True
)

print("Columns:")
print(df.columns.tolist())



under5_cases = df["Cases.Fever <5"].sum()

over5_cases = df["Cases.Fever >=5"].sum()

positive_under5 = (
    df["Cases.Fever.with.RDT.Positive <5"].sum()
)

negative_under5 = (
    df["Cases.Fever.with.RDT.Negative <5"].sum()
)

positive_over5 = (
    df["Cases.Fever.with.RDT.Positive >=5"].sum()
)

negative_over5 = (
    df["Cases.Fever.with.RDT.Negative >=5"].sum()
)


# ==========================================================
# KPI VALUES
# ==========================================================

total_fever = int(
    df["Cases.Fever"].sum()
)

total_tests = int(
    df["Cases.Fever.with.RDT.Done"].sum()
)

positive_cases = int(
    df["Cases.Fever.with.RDT.Positive <5"].sum()
    +
    df["Cases.Fever.with.RDT.Positive >=5"].sum()
)

total_act = int(
    df["Cases.Fever.with.RDT.Positive.and.ACT"].sum()
)

# ==========================================================
# FEVER → AGE GROUP → RDT OUTCOME SANKEY
# ==========================================================

under5_cases = (
    df["Cases.Fever <5"].sum()
)

over5_cases = (
    df["Cases.Fever >=5"].sum()
)

positive_under5 = (
    df["Cases.Fever.with.RDT.Positive <5"].sum()
)

positive_over5 = (
    df["Cases.Fever.with.RDT.Positive >=5"].sum()
)

negative_under5 = (
    df["Cases.Fever.with.RDT.negative <5"].sum()
)

negative_over5 = (
    df["Cases.Fever.with.RDT.negative >=5"].sum()
)



fever_age_fig = go.Figure(

    go.Sankey(

        arrangement="snap",

        node=dict(

            pad=25,
            thickness=25,

            line=dict(
                color="rgba(0,0,0,0.2)",
                width=1
            ),

            label=[

                "Fever Cases",

                "Children <5",
                "Individuals ≥5",

                "RDT Positive <5",
                "RDT Negative <5",

                "RDT Positive ≥5",
                "RDT Negative ≥5",

            ],

            color=[

                "#2563eb",

                "#f97316",
                "#16a34a",

                "#dc2626",
                "#fbbf24",

                "#b91c1c",
                "#fde68a",

            ],

        ),

        link=dict(

            source=[

                # Fever → Age group
                0, 0,

                # <5
                1, 1,

                # ≥5
                2, 2

            ],

            target=[

                1, 2,

                3, 4,

                5, 6

            ],

            value=[

                under5_cases,
                over5_cases,

                positive_under5,
                negative_under5,

                positive_over5,
                negative_over5

            ],

            color=[

                "rgba(249,115,22,0.35)",
                "rgba(22,163,74,0.35)",

                "rgba(220,38,38,0.35)",
                "rgba(251,191,36,0.35)",

                "rgba(185,28,28,0.35)",
                "rgba(253,230,138,0.35)"

            ],

        ),

    )

)

fever_age_fig.update_layout(
    template="plotly_white",
    height=700,
    margin=dict(l=20, r=20, t=20, b=20)
)
# ==========================================================
# SANKEY 3 - RDT OUTCOMES
# ==========================================================

positive_under5 = 9000
positive_over5 = 16000

negative_under5 = 4000
negative_over5 = 9500

rdt_sankey_fig = go.Figure(

    go.Sankey(

        arrangement="snap",

        node=dict(

            pad=25,
            thickness=25,

            label=[
                "RDT Done",
                "RDT Positive",
                "RDT Negative",
                "Positive <5",
                "Positive ≥5",
                "Negative <5",
                "Negative ≥5"
            ],

            color=[
                "#2563eb",
                "#f97316",
                "#fbbf24",
                "#dc2626",
                "#ef4444",
                "#10b981",
                "#059669"
            ]
        ),

        link=dict(

            source=[
                0,0,
                1,1,
                2,2
            ],

            target=[
                1,2,
                3,4,
                5,6
            ],

            value=[
                positive_under5 + positive_over5,
                negative_under5 + negative_over5,

                positive_under5,
                positive_over5,

                negative_under5,
                negative_over5
            ],

            color="rgba(180,180,180,0.40)"
        )

    )

)

rdt_sankey_fig.update_layout(
    template="plotly_white",
    height=500,
    margin=dict(l=20,r=20,t=20,b=20)
)

# ==========================================================
# STOCKS (REAL DATA)
# ==========================================================

stock_fig = go.Figure()

stock_fig.add_trace(
    go.Bar(
        x=df["Month"],
        y=df["Stock mRDTs"],
        name="mRDT Stock",
        marker_color="#2563eb"
    )
)

stock_fig.add_trace(
    go.Bar(
        x=df["Month"],
        y=df["Stock ACTs"],
        name="ACT Stock",
        marker_color="#16a34a"
    )
)

stock_fig.update_layout(
    barmode="group",
    template="plotly_white",
    height=450,
    margin=dict(l=20, r=20, t=20, b=20),
    legend_title=""
)

# ==========================================================
# CHEW WEIGHT BAND DISTRIBUTION (REAL DATA)
# ==========================================================

weight_fig = go.Figure()

weight_fig.add_trace(
    go.Bar(
        name="5-<15 kg",
        x=df["Month"],
        y=df["CHEW Weight band 5 to <15 kg"],
        marker_color="#60a5fa"
    )
)

weight_fig.add_trace(
    go.Bar(
        name="15-<25 kg",
        x=df["Month"],
        y=df["CHEW Weight band 15 to <25 kg"],
        marker_color="#34d399"
    )
)

weight_fig.add_trace(
    go.Bar(
        name="25-<35 kg",
        x=df["Month"],
        y=df["CHEW Weight band 25 to <35 kg"],
        marker_color="#f59e0b"
    )
)

weight_fig.add_trace(
    go.Bar(
        name="≥35 kg",
        x=df["Month"],
        y=df["CHEW Weight band ≥35 kg"],
        marker_color="#ef4444"
    )
)

weight_fig.update_layout(
    barmode="stack",
    template="plotly_white",
    height=450,
    margin=dict(l=20, r=20, t=20, b=20),
    legend_title=""
)

# ==========================================================
# LAYOUT
# ==========================================================

layout = dbc.Container(

    [

        # =====================================================
# FILTER PANEL (PLACEHOLDER)
# =====================================================

dbc.Card(

    dbc.CardBody(

        [

                dbc.Row(
        
                        [
        
                            dbc.Col(
        
                                [
        
                                    html.Label(
                                        "Subcounty",
                                        className="fw-bold text-muted mb-2"
                                    ),
        
                                    dcc.Dropdown(
                                        id="malaria-subcounty-dropdown",
        
                                        options=[
                                            {"label": "Alego Usonga", "value": "alego"},
                                            {"label": "Bondo", "value": "bondo"},
                                            {"label": "Rarieda", "value": "rarieda"},
                                            {"label": "Ugunja", "value": "ugunja"},
                                            {"label": "Ugenya", "value": "ugenya"},
                                            {"label": "Gem", "value": "gem"},
                                        ],
        
                                        value="alego",
        
                                        clearable=False,
        
                                    ),
        
                                ],
        
                                lg=8,
        
                            ),
        
                            dbc.Col(
        
                                [
        
                                    html.Label(
                                        "Year",
                                        className="fw-bold text-muted mb-2"
                                    ),
        
                                    dcc.Dropdown(
        
                                        id="malaria-year-dropdown",
        
                                        options=[
                                            {"label": "All Years", "value": "ALL"},
                                            {"label": "2022", "value": 2022},
                                            {"label": "2023", "value": 2023},
                                            {"label": "2024", "value": 2024},
                                            {"label": "2025", "value": 2025},
                                            {"label": "2026", "value": 2026},
                                        ],
        
                                        value="ALL",
        
                                        clearable=False,
        
                                    ),
        
                                ],
        
                                lg=4,
        
                            ),
        
                        ],
        
                    ),
        
                ]
        
            ),
        
            className="border-0 shadow-sm mb-4",
        
            style={
                "borderRadius": "16px",
            },
        
        ),
        
        dbc.Card(
        
            dbc.CardBody([
        
                html.H4(
                    "Fever Cases by Age Group and RDT Outcome (Fake placerholder data)",
                    className="fw-bold mb-1"
                ),
        
                html.P(
                    "Distribution of reported fever cases by age group and malaria diagnostic outcome.",
                    className="text-muted mb-4"
                ),
        
                dcc.Graph(
                    figure=fever_age_fig,
                    config={
                        "displayModeBar": False
                    }
                )
        
            ]),
        
            className="border-0 shadow-sm mb-4"
        
        ),
        
        dbc.Row(

            [

                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.H5(
                                "Commodity Stock Levels",
                                className="fw-bold"
                            ),
                            html.P(
                                "Monthly mRDT and ACT stock availability.",
                                className="text-muted"
                            ),
                            dcc.Graph(
                                figure=stock_fig,
                                config={"displayModeBar": False}
                            )
                        ]),
                        className="border-0 shadow-sm"
                    ),
                    lg=6
                ),

                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.H5(
                                "CHEW Weight-Band Distribution",
                                className="fw-bold"
                            ),
                            html.P(
                                "Monthly distribution across weight categories.",
                                className="text-muted"
                            ),
                            dcc.Graph(
                                figure=weight_fig,
                                config={"displayModeBar": False}
                            )
                        ]),
                        className="border-0 shadow-sm"
                    ),
                    lg=6
                ),

            ]

        ),

    ],

    fluid=True,

    style={
        "backgroundColor": "#f8fafc",
        "padding": "20px",
        "minHeight": "100vh",
    },

)
