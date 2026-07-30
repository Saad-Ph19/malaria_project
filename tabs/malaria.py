from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ==========================================================
# FAKE DATA
# ==========================================================

months = [
    "Jan","Feb","Mar","Apr","May","Jun",
    "Jul","Aug","Sep","Oct","Nov","Dec"
]

np.random.seed(42)

df = pd.DataFrame({
    "Month": months,
    "Fever_Cases": np.random.randint(2500, 5000, 12),
    "RDT_Done": np.random.randint(2200, 4500, 12),
    "RDT_Positive": np.random.randint(1000, 3000, 12),
    "ACT_Given": np.random.randint(900, 2800, 12),
    "Stock_RDT": np.random.randint(2000, 10000, 12),
    "Stock_ACT": np.random.randint(2000, 10000, 12),
    "Loss_RDT": np.random.randint(0, 100, 12),
    "Loss_ACT": np.random.randint(0, 80, 12),
})

df["Testing_Coverage"] = (
    df["RDT_Done"] / df["Fever_Cases"] * 100
)

df["Treatment_Coverage"] = (
    df["ACT_Given"] / df["RDT_Positive"] * 100
)

# ==========================================================
# KPI VALUES
# ==========================================================

total_fever = int(df["Fever_Cases"].sum())
total_tests = int(df["RDT_Done"].sum())
positive_cases = int(df["RDT_Positive"].sum())
total_act = int(df["ACT_Given"].sum())

# ==========================================================
# FEVER → AGE GROUP → RDT OUTCOME SANKEY
# ==========================================================

under5_cases = 18000
over5_cases = 26000

positive_under5 = 9000
negative_under5 = 9000

positive_over5 = 16000
negative_over5 = 10000

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
# STOCKS
# ==========================================================

stock_fig = go.Figure()

stock_fig.add_trace(
    go.Bar(
        x=df["Month"],
        y=df["Stock_RDT"],
        name="mRDT Stock"
    )
)

stock_fig.add_trace(
    go.Bar(
        x=df["Month"],
        y=df["Stock_ACT"],
        name="ACT Stock"
    )
)

stock_fig.update_layout(
    barmode="group",
    template="plotly_white",
    height=450
)

# ==========================================================
# CHEW WEIGHT BAND
# ==========================================================

weight_fig = go.Figure()

weight_fig.add_trace(
    go.Bar(
        name="<15 kg",
        x=months,
        y=np.random.randint(100, 300, 12)
    )
)

weight_fig.add_trace(
    go.Bar(
        name="15-25 kg",
        x=months,
        y=np.random.randint(150, 400, 12)
    )
)

weight_fig.add_trace(
    go.Bar(
        name="25-35 kg",
        x=months,
        y=np.random.randint(100, 350, 12)
    )
)

weight_fig.add_trace(
    go.Bar(
        name="35+ kg",
        x=months,
        y=np.random.randint(100, 300, 12)
    )
)

weight_fig.update_layout(
    barmode="stack",
    template="plotly_white",
    height=450
)

# ==========================================================
# LAYOUT
# ==========================================================

layout = dbc.Container(

    [
        dbc.Card(
        
            dbc.CardBody([
        
                html.H4(
                    "Fever Cases by Age Group and RDT Outcome",
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
