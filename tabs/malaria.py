from dash import callback, Input, Output, html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import glob
import os

# Bednet data
bednet_files = glob.glob("Bednet_Data/*.xlsx")

bednet_df = pd.read_excel(
    bednet_files[0],
    header=1
)

bednet_df.columns = bednet_df.columns.str.strip()

anc_cols = [
    col
    for col in bednet_df.columns
    if "LLINs distributed to ANC clients" in col
]

bednet_long = bednet_df.melt(
    id_vars=["organisationunitname"],
    value_vars=anc_cols,
    var_name="Year",
    value_name="Bed_Nets"
)

bednet_long["Year"] = (
    bednet_long["Year"]
    .str.extract(r"(\d{4})")
    .astype(int)
)

bednet_long.rename(
    columns={
        "organisationunitname": "Subcounty"
    },
    inplace=True
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


# Prepare Non-Malarial Fever data
###
df["Month"] = pd.to_numeric(df["Month"], errors="coerce")
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

# Create Month-Year date
df["Date"] = pd.to_datetime(
    dict(
        year=df["Year"],
        month=df["Month"],
        day=1
    ),
    errors="coerce"
)

# Total fever cases
df["Total_Fever_Cases"] = (
    df["Cases.Fever < 5"].fillna(0)
    + df["Cases.Fever >= 5"].fillna(0)
)

# Fever cases that tested negative for malaria
df["Non_Malarial_Fever"] = (
    df["Cases.Fever.with.RDT. negative < 5"].fillna(0)
    + df["Cases.Fever.with.RDT. negative >= 5"].fillna(0)
)

# Percentage
df["Non_Malarial_Fever_Percent"] = np.where(
    df["Total_Fever_Cases"] > 0,
    (
        df["Non_Malarial_Fever"]
        / df["Total_Fever_Cases"]
    ) * 100,
    np.nan
)


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
bednet_fig = px.line(
    bednet_long,
    x="Year",
    y="Bed_Nets",
    color="Subcounty",
    markers=True,
    title="ANC Bed Net Distribution (2020-2026)"
)

bednet_fig.update_layout(
    template="plotly_white",
    height=450,
    legend_title="",
    margin=dict(
        l=20,
        r=20,
        t=50,
        b=20
    )
)

# Proportion of Non-Malarial Fever Cases
# Always displays ALL subcounties and ALL years

non_malaria_data = df.copy()

# Shorten the Subcounty names ONLY for this visualization
non_malaria_data["Subcounty"] = (
    non_malaria_data["Subcounty"]
    .astype(str)
    .str.replace(" Sub County", "", regex=False)
    .str.strip()
)

# Sort data by Subcounty and date
non_malaria_data = non_malaria_data.sort_values(
    ["Subcounty", "Date"]
)

# Create small-multiple line chart
non_malaria_fig = px.line(
    non_malaria_data,
    x="Date",
    y="Non_Malarial_Fever_Percent",
    color="Subcounty",
    facet_col="Subcounty",
    facet_col_wrap=3,
    category_orders={
        "Subcounty": [
            "Alego Usonga",
            "Bondo",
            "Gem",
            "Rarieda",
            "Ugenya",
            "Ugunja"
        ]
    }
)

# Remove "Subcounty=" from titles
#non_malaria_fig.for_each_annotation(
    #lambda a: a.update(
        #text=a.text.replace("Subcounty=", "")
   #)
#)

non_malaria_fig.update_traces(
    line=dict(width=3),
    hovertemplate=(
        "<b>%{x|%B %Y}</b><br>"
        "Non-Malarial Fever: %{y:.1f}%"
        "<extra></extra>"
    )
)

non_malaria_fig.update_yaxes(
    ticksuffix="%",
    rangemode="tozero",
    showgrid=True,
    gridcolor="rgba(0,0,0,0.08)",
    title=None
)

non_malaria_fig.update_xaxes(
    title=None,
    showgrid=True,
    gridcolor="rgba(0,0,0,0.08)",
    tickformat="%Y",
    dtick="M12"
)

non_malaria_fig.update_layout(
    template="plotly_white",
    height=650,

    margin=dict(
        l=70,
        r=130,
        t=40,
        b=70
    ),

    legend_title_text="SubCounty",

    legend=dict(
        orientation="v",
        x=1.01,
        y=0.5,
        yanchor="middle"
    ),

    hovermode="closest"
)

# Shared X-axis title
non_malaria_fig.add_annotation(
    text="Month–Year",
    x=0.5,
    y=-0.10,
    xref="paper",
    yref="paper",
    showarrow=False,
    font=dict(size=14)
)

# Shared Y-axis title
non_malaria_fig.add_annotation(
    text="% Non-Malarial Fever",
    x=-0.06,
    y=0.5,
    xref="paper",
    yref="paper",
    textangle=-90,
    showarrow=False,
    font=dict(size=14)
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

        dbc.Card(
            dbc.CardBody([
                html.H4(
                    "Proportion of Non-Malarial Fever Cases",
                    className="fw-bold mb-1"
                ),
        
                html.P(
                    "Monthly proportion of reported fever cases that tested negative for malaria across all subcounties.",
                    className="text-muted mb-4"
                ),
        
                dcc.Graph(
                    id="non-malaria-fever",
                    figure=non_malaria_fig,
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
                    "Long-lasting insecticidal nets distributed to antenatal care clients.",
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
