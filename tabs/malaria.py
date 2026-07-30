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
# FUNNEL
# ==========================================================

funnel_fig = go.Figure(
    go.Funnel(
        y=[
            "Fever Cases",
            "RDT Done",
            "RDT Positive",
            "ACT Treatment"
        ],
        x=[
            total_fever,
            total_tests,
            positive_cases,
            total_act
        ],
        marker=dict(
            color=[
                "#2563eb",
                "#3b82f6",
                "#f97316",
                "#16a34a"
            ]
        )
    )
)

funnel_fig.update_layout(
    template="plotly_white",
    height=500,
    margin=dict(l=20,r=20,t=20,b=20)
)

# ==========================================================
# CASE TREND
# ==========================================================

trend_fig = go.Figure()

trend_fig.add_trace(
    go.Scatter(
        x=df["Month"],
        y=df["Fever_Cases"],
        mode="lines+markers",
        name="Fever Cases",
        line=dict(color="#2563eb")
    )
)

trend_fig.add_trace(
    go.Scatter(
        x=df["Month"],
        y=df["RDT_Positive"],
        mode="lines+markers",
        name="RDT Positive",
        line=dict(color="#ef4444")
    )
)

trend_fig.update_layout(
    template="plotly_white",
    height=450
)

# ==========================================================
# COVERAGE
# ==========================================================

coverage_fig = go.Figure()

coverage_fig.add_trace(
    go.Scatter(
        x=df["Month"],
        y=df["Testing_Coverage"],
        mode="lines+markers",
        name="Testing Coverage (%)"
    )
)

coverage_fig.add_trace(
    go.Scatter(
        x=df["Month"],
        y=df["Treatment_Coverage"],
        mode="lines+markers",
        name="Treatment Coverage (%)"
    )
)

coverage_fig.update_layout(
    template="plotly_white",
    height=450,
    yaxis_title="%"
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

        dbc.Row(

            [

                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.Div("Fever Cases", className="text-muted"),
                            html.H3(f"{total_fever:,}",
                                    className="fw-bold text-primary")
                        ]),
                        className="border-0 shadow-sm"
                    ),
                    lg=3
                ),

                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.Div("RDT Done", className="text-muted"),
                            html.H3(f"{total_tests:,}",
                                    className="fw-bold text-success")
                        ]),
                        className="border-0 shadow-sm"
                    ),
                    lg=3
                ),

                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.Div("RDT Positive", className="text-muted"),
                            html.H3(f"{positive_cases:,}",
                                    className="fw-bold text-danger")
                        ]),
                        className="border-0 shadow-sm"
                    ),
                    lg=3
                ),

                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.Div("ACT Treatment", className="text-muted"),
                            html.H3(f"{total_act:,}",
                                    className="fw-bold text-success")
                        ]),
                        className="border-0 shadow-sm"
                    ),
                    lg=3
                ),

            ],

            className="mb-4"

        ),

        dbc.Card(
            dbc.CardBody([
                html.H4(
                    "Community Malaria Surveillance Cascade",
                    className="fw-bold mb-1"
                ),
                html.P(
                    "Progression from fever presentation through testing, diagnosis and treatment.",
                    className="text-muted mb-4"
                ),
                dcc.Graph(
                    figure=funnel_fig,
                    config={"displayModeBar": False}
                )
            ]),
            className="border-0 shadow-sm mb-4"
        ),

        dbc.Row(

            [

                dbc.Col(
                    dbc.Card(
                        dbc.CardBody([
                            html.H5("Case Trends",
                                    className="fw-bold"),
                            html.P(
                                "Monthly fever and malaria-positive cases.",
                                className="text-muted"
                            ),
                            dcc.Graph(
                                figure=trend_fig,
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
                                "Testing & Treatment Coverage",
                                className="fw-bold"
                            ),
                            html.P(
                                "Monthly surveillance performance indicators.",
                                className="text-muted"
                            ),
                            dcc.Graph(
                                figure=coverage_fig,
                                config={"displayModeBar": False}
                            )
                        ]),
                        className="border-0 shadow-sm"
                    ),
                    lg=6
                ),

            ],

            className="mb-4"

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
