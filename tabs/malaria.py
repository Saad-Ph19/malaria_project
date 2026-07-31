from dash import html, dcc
from dash import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import glob
import pandas as pd
import os

# ==========================================================
# LOAD MALARIA DATA
# ==========================================================
files = glob.glob("Malaria_Data/*.xlsx")

df_list = []

for file in files:

    temp = pd.read_excel(file, header=1)

    year = os.path.basename(file)[:4]

    temp["Year"] = year

    df_list.append(temp)

df = pd.concat(
    df_list,
    ignore_index=True
)

df.columns = df.columns.str.strip()

# ==========================================================
# KPI VALUES
# ==========================================================

total_fever = int(df["Cases.Fever"].sum())

total_tests = int(df["Cases.Fever.with.RDT.Done"].sum())

positive_cases = int(
    df["Cases.Fever.with.RDT.Positive < 5"].sum()
    + df["Cases.Fever.with.RDT.Positive >= 5"].sum()
)

total_act = int(
    df["Cases.Fever.with.RDT.Positive.and.ACT"].sum()
)

# ==========================================================
# SANKEY DATA
# ==========================================================

under5_cases = df["Cases.Fever < 5"].sum()

over5_cases = df["Cases.Fever >= 5"].sum()

positive_under5 = (
    df["Cases.Fever.with.RDT.Positive < 5"].sum()
)

positive_over5 = (
    df["Cases.Fever.with.RDT.Positive >= 5"].sum()
)

negative_under5 = (
    df["Cases.Fever.with.RDT. negative < 5"].sum()
)

negative_over5 = (
    df["Cases.Fever.with.RDT. negative >= 5"].sum()
)

# ==========================================================
# FEVER → AGE GROUP → RDT OUTCOME SANKEY
# ==========================================================

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
                0, 0,
                1, 1,
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
            ]

        )

    )

)

fever_age_fig.update_layout(
    template="plotly_white",
    height=700,
    margin=dict(l=20, r=20, t=20, b=20)
)

# ==========================================================
# STOCKS
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
    margin=dict(l=20, r=20, t=20, b=20)
)

# ==========================================================
# CHEW WEIGHT BANDS
# ==========================================================

weight_fig = go.Figure()

weight_fig.add_trace(
    go.Bar(
        name="5-<15 kg",
        x=df["Month"],
        y=df["CHEW Weight band 5 to <15 kg  (<3 yrs)"],
        marker_color="#60a5fa"
    )
)

weight_fig.add_trace(
    go.Bar(
        name="15-<25 kg",
        x=df["Month"],
        y=df["CHEW Weight band 15 to <25 kg  (3 to <8 yrs)"],
        marker_color="#34d399"
    )
)

weight_fig.add_trace(
    go.Bar(
        name="25-<35 kg",
        x=df["Month"],
        y=df["CHEW Weight band 25 to <35 kg (8 to <12 yrs)"],
        marker_color="#f59e0b"
    )
)

weight_fig.add_trace(
    go.Bar(
        name="≥35 kg",
        x=df["Month"],
        y=df["CHEW Weight band ≥ 35 kg (≥ 12 yrs)"],
        marker_color="#ef4444"
    )
)

weight_fig.update_layout(
    barmode="stack",
    template="plotly_white",
    height=450,
    margin=dict(l=20, r=20, t=20, b=20)
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
                                            {"label": "All Subcounties", "value": "ALL"}
                                        ] + [
                                            {"label": s, "value": s}
                                            for s in sorted(df["Subcounty"].dropna().unique())
                                        ],
                                        value="ALL",
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
                                            {"label": "All Years", "value": "ALL"}
                                        ] + [
                                            {"label": str(y), "value": str(y)}
                                            for y in sorted(df["Year"].unique())
                                        ],
                                        value="ALL",
                                        clearable=False,
                                    )
                                            
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
                    id="malaria-sankey",
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
                                id="malaria-stock",
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
                                id="malaria-weight",
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

#Callback function
@app.callback(
    [
        Output("malaria-sankey", "figure"),
        Output("malaria-stock", "figure"),
        Output("malaria-weight", "figure"),
    ],
    [
        Input("malaria-subcounty-dropdown", "value"),
        Input("malaria-year-dropdown", "value"),
    ]
)
def update_malaria(subcounty, year):

    filtered_df = df.copy()

    if subcounty != "ALL":
        filtered_df = filtered_df[
            filtered_df["Subcounty"] == subcounty
        ]

    if year != "ALL":
        filtered_df = filtered_df[
            filtered_df["Year"] == year
        ]

    # recalculate Sankey values here
    # rebuild stock_fig here
    # rebuild weight_fig here

    return fever_age_fig, stock_fig, weight_fig
