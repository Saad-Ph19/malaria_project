from dash import callback, Input, Output, html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import glob
import os

bednet_files = glob.glob("Bednet_Data/*.xlsx")

bednet_df = pd.concat(
    [pd.read_excel(f, header=1) for f in bednet_files],
    ignore_index=True
)
bednet_df.columns = bednet_df.columns.str.strip()
print(bednet_df.columns.tolist())
bednet_long = bednet_df.melt(
    id_vars=["Year"],
    var_name="Subcounty",
    value_name="Bed_Nets"
)

# Malaria data
files = glob.glob("Malaria_Data/*.xlsx")
df_list = []
for file in files:
    temp = pd.read_excel(file, header=1)
    year = os.path.basename(file)[:4]
    temp["Year"] = year
    df_list.append(temp)

df = pd.concat(df_list,ignore_index=True)
df.columns = df.columns.str.strip()

# Sankey Vis
under5_cases = df["Cases.Fever < 5"].sum()
over5_cases = df["Cases.Fever >= 5"].sum()
positive_under5 = (df["Cases.Fever.with.RDT.Positive < 5"].sum())
positive_over5 = (df["Cases.Fever.with.RDT.Positive >= 5"].sum())
negative_under5 = (df["Cases.Fever.with.RDT. negative < 5"].sum())
negative_over5 = (df["Cases.Fever.with.RDT. negative >= 5"].sum())

#Fever, age group, and rdt outcome
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

            label=["Fever Cases","Children <5","Individuals ≥5","RDT Positive <5","RDT Negative <5","RDT Positive ≥5","RDT Negative ≥5",],
            color=["#2563eb","#f97316","#16a34a","#dc2626","#fbbf24","#b91c1c","#fde68a",],
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

            value=[under5_cases,over5_cases,positive_under5,negative_under5,positive_over5,negative_over5],
            color=["rgba(249,115,22,0.35)","rgba(22,163,74,0.35)","rgba(220,38,38,0.35)","rgba(251,191,36,0.35)","rgba(185,28,28,0.35)","rgba(253,230,138,0.35)"]
        )
    )
)

fever_age_fig.update_layout(
    template="plotly_white",
    height=700,
    margin=dict(l=20, r=20, t=20, b=20)
)

# Stocks
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

# Chew weight bands
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

#bednets
bednet_fig = px.bar(
    bednet_long,
    x="Year",
    y="Bed_Nets",
    color="Subcounty",
    title="ANC Bed Net Distribution by Subcounty",
    barmode="stack"
)

bednet_fig.update_layout(
    template="plotly_white",
    height=450,
    legend_title=""
)

# Layout
layout = dbc.Container(
    [

dbc.Card(
    dbc.CardBody(
        [
                dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.Label("Subcounty",className="fw-bold text-muted mb-2"),     
                                    dcc.Dropdown(
                                        id="malaria-subcounty-dropdown",
                                        options=[
                                            {"label": "All Subcounties", "value": "ALL"}
                                        ] + [
                                            {"label": str(s), "value": str(s)}
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
                                    html.Label("Year",className="fw-bold text-muted mb-2"),
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
            style={"borderRadius": "16px",},
        ),
        
        dbc.Card(
            dbc.CardBody([
                html.H4("Fever Cases by Age Group and RDT Outcome",className="fw-bold mb-1"),
                html.P("Distribution of reported fever cases by age group and malaria diagnostic outcome.",className="text-muted mb-4"),
        
                dcc.Graph(
                    id="malaria-sankey",
                    figure=fever_age_fig,
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
                            html.H5("Commodity Stock Levels",className="fw-bold"),
                            html.P("Monthly mRDT and ACT stock availability.",className="text-muted"),
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
                            html.H5("CHEW Weight-Band Distribution",className="fw-bold"),
                            html.P("Monthly distribution across weight categories.",className="text-muted"),
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
        dbc.Card(
            dbc.CardBody([
                html.H5(
                    "ANC Bed Net Distribution",
                    className="fw-bold"
                ),
        
                html.P(
                    "Bed nets distributed to antenatal care clients across all subcounties and years.",
                    className="text-muted"
                ),
        
                dcc.Graph(
                    figure=bednet_fig,
                    config={"displayModeBar": False}
                )
            ]),
            className="border-0 shadow-sm mt-4"
        ),   
    ],
    fluid=True,
    style={"backgroundColor": "#f8fafc","padding": "20px","minHeight": "100vh",},
)

#Callback function
@callback(
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
    # Filter Subcounty
    if subcounty != "ALL":
        filtered_df = filtered_df[
            filtered_df["Subcounty"] == subcounty
        ]

    # Filter Year
    if year != "ALL":
        filtered_df = filtered_df[
            filtered_df["Year"].astype(str) == str(year)
        ]

    # Sankey values
    under5_cases = filtered_df["Cases.Fever < 5"].sum()
    over5_cases = filtered_df["Cases.Fever >= 5"].sum()
    positive_under5 = (filtered_df["Cases.Fever.with.RDT.Positive < 5"].sum())
    positive_over5 = (filtered_df["Cases.Fever.with.RDT.Positive >= 5"].sum())
    negative_under5 = (filtered_df["Cases.Fever.with.RDT. negative < 5"].sum())
    negative_over5 = (filtered_df["Cases.Fever.with.RDT. negative >= 5"].sum())
    not_tested_under5 = (under5_cases - positive_under5 - negative_under5)
    not_tested_over5 = (over5_cases - positive_over5 - negative_over5)

    sankey_fig = go.Figure(
        go.Sankey(
            arrangement="snap",

            node=dict(
                pad=25,
                thickness=25,

                label=[
                    "Fever Cases",
                    "Children <5",
                    "Individuals ≥5",
                    "RDT Positive <5",
                    "RDT Negative <5",
                    "Not Tested <5",
                    "RDT Positive ≥5",
                    "RDT Negative ≥5",
                    "Not Tested ≥5"
                ],
                color=[
                    "#2563eb",
                    "#f97316",
                    "#16a34a",
                    "#dc2626",
                    "#fbbf24",
                    "#6b7280",
                    "#b91c1c",
                    "#fde68a",
                    "#9ca3af"
                ]
            ),

            link=dict(
                source=[
                    0,0,
                    1,1,1,
                    2,2,2
                ],
                
                target=[
                    1,2,
                    3,4,5,
                    6,7,8
                ],
                
                value=[
                    under5_cases,
                    over5_cases,
                    positive_under5,
                    negative_under5,
                    not_tested_under5,
                    positive_over5,
                    negative_over5,
                    not_tested_over5
                ]
            )
        )
    )

    sankey_fig.update_layout(template="plotly_white",height=700)

    # Stock figures
    stock_fig = go.Figure()
    stock_fig.add_trace(
        go.Bar(
            x=filtered_df["Month"],
            y=filtered_df["Stock mRDTs"],
            name="mRDT Stock",
            marker_color="#2563eb"
        )
    )

    stock_fig.add_trace(
        go.Bar(
            x=filtered_df["Month"],
            y=filtered_df["Stock ACTs"],
            name="ACT Stock",
            marker_color="#16a34a"
        )
    )

    stock_fig.update_layout(
        barmode="group",
        template="plotly_white",
        height=450
    )

    # Weight figures
    weight_fig = go.Figure()
    weight_fig.add_trace(
        go.Bar(
            name="5-<15 kg",
            x=filtered_df["Month"],
            y=filtered_df["CHEW Weight band 5 to <15 kg  (<3 yrs)"]
        )
    )

    weight_fig.add_trace(
        go.Bar(
            name="15-<25 kg",
            x=filtered_df["Month"],
            y=filtered_df["CHEW Weight band 15 to <25 kg  (3 to <8 yrs)"]
        )
    )

    weight_fig.add_trace(
        go.Bar(
            name="25-<35 kg",
            x=filtered_df["Month"],
            y=filtered_df["CHEW Weight band 25 to <35 kg (8 to <12 yrs)"]
        )
    )

    weight_fig.add_trace(
        go.Bar(
            name="≥35 kg",
            x=filtered_df["Month"],
            y=filtered_df["CHEW Weight band ≥ 35 kg (≥ 12 yrs)"]
        )
    )

    weight_fig.update_layout(
        barmode="stack",
        template="plotly_white",
        height=450
    )

    return (
        sankey_fig,
        stock_fig,
        weight_fig
    )
