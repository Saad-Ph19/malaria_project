from dash import callback, Input, Output, html, dcc
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
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


# Fever / RDT / ACT Summary by Age Group and Year
# Always displays ALL subcounties and ALL years

age_summary = df.copy()

# Make sure Year is numeric
age_summary["Year"] = pd.to_numeric(
    age_summary["Year"],
    errors="coerce"
)


# Create required measures
# Fever cases
age_summary["Fever_U5"] = (
    pd.to_numeric(
        age_summary["Cases.Fever < 5"],
        errors="coerce"
    ).fillna(0)
)

age_summary["Fever_5plus"] = (
    pd.to_numeric(
        age_summary["Cases.Fever >= 5"],
        errors="coerce"
    ).fillna(0)
)

# RDT Positive
age_summary["RDT_Pos_U5"] = (
    pd.to_numeric(
        age_summary["Cases.Fever.with.RDT.Positive < 5"],
        errors="coerce"
    ).fillna(0)
)

age_summary["RDT_Pos_5plus"] = (
    pd.to_numeric(
        age_summary["Cases.Fever.with.RDT.Positive >= 5"],
        errors="coerce"
    ).fillna(0)
)


# RDT Negative
age_summary["RDT_Neg_U5"] = (
    pd.to_numeric(
        age_summary["Cases.Fever.with.RDT. negative < 5"],
        errors="coerce"
    ).fillna(0)
)

age_summary["RDT_Neg_5plus"] = (
    pd.to_numeric(
        age_summary["Cases.Fever.with.RDT. negative >= 5"],
        errors="coerce"
    ).fillna(0)
)


# Total RDT tested = positive + negative
age_summary["RDT_Tested_U5"] = (
    age_summary["RDT_Pos_U5"]
    + age_summary["RDT_Neg_U5"]
)

age_summary["RDT_Tested_5plus"] = (
    age_summary["RDT_Pos_5plus"]
    + age_summary["RDT_Neg_5plus"]
)


# Aggregate across all subcounties by year
year_age_summary = (
    age_summary
    .groupby("Year", as_index=False)
    .agg(
        Fever_U5=("Fever_U5", "sum"),
        Fever_5plus=("Fever_5plus", "sum"),

        RDT_Tested_U5=("RDT_Tested_U5", "sum"),
        RDT_Tested_5plus=("RDT_Tested_5plus", "sum"),

        RDT_Pos_U5=("RDT_Pos_U5", "sum"),
        RDT_Pos_5plus=("RDT_Pos_5plus", "sum"),
    )
    .sort_values("Year")
)


####
# Malaria Estimated Prevalence by Age Group and Year
prevalence_data = df.copy()

# Make sure numeric columns are actually numeric
numeric_columns = [
    "Cases.Fever.with.RDT.Positive < 5",
    "Cases.Fever.with.RDT.Positive >= 5",
    "Cases.Fever.with.RDT. negative < 5",
    "Cases.Fever.with.RDT. negative >= 5",
]

for col in numeric_columns:
    prevalence_data[col] = pd.to_numeric(
        prevalence_data[col],
        errors="coerce"
    ).fillna(0)

prevalence_data["Year"] = pd.to_numeric(
    prevalence_data["Year"],
    errors="coerce"
)

prevalence_data["Month"] = pd.to_numeric(
    prevalence_data["Month"],
    errors="coerce"
)

# Aggregate ALL subcounties by Year and Month
monthly_prevalence = (
    prevalence_data
    .groupby(["Year", "Month"], as_index=False)
    .agg(
        Positive_U5=(
            "Cases.Fever.with.RDT.Positive < 5",
            "sum"
        ),
        Negative_U5=(
            "Cases.Fever.with.RDT. negative < 5",
            "sum"
        ),
        Positive_5plus=(
            "Cases.Fever.with.RDT.Positive >= 5",
            "sum"
        ),
        Negative_5plus=(
            "Cases.Fever.with.RDT. negative >= 5",
            "sum"
        )
    )
)

prevalence_rows = []

for _, row in monthly_prevalence.iterrows():

    # -----------------------------
    # Under 5
    # -----------------------------
    tested_u5 = (
        row["Positive_U5"]
        + row["Negative_U5"]
    )

    if tested_u5 > 0:

        prevalence_u5 = (
            row["Positive_U5"]
            / tested_u5
        )

        # 95% CI
        se_u5 = np.sqrt(
            prevalence_u5
            * (1 - prevalence_u5)
            / tested_u5
        )

        ci_u5 = 1.96 * se_u5

        prevalence_rows.append(
            {
                "Year": int(row["Year"]),
                "Month": int(row["Month"]),
                "Age_Group": "<5",
                "Prevalence": prevalence_u5,
                "CI": ci_u5
            }
        )

    tested_5plus = (
        row["Positive_5plus"]
        + row["Negative_5plus"]
    )

    if tested_5plus > 0:

        prevalence_5plus = (
            row["Positive_5plus"]
            / tested_5plus
        )

        # 95% CI
        se_5plus = np.sqrt(
            prevalence_5plus
            * (1 - prevalence_5plus)
            / tested_5plus
        )

        ci_5plus = 1.96 * se_5plus

        prevalence_rows.append(
            {
                "Year": int(row["Year"]),
                "Month": int(row["Month"]),
                "Age_Group": "5+",
                "Prevalence": prevalence_5plus,
                "CI": ci_5plus
            }
        )


prevalence_long = pd.DataFrame(
    prevalence_rows
)

prevalence_long = prevalence_long.sort_values(
    ["Age_Group", "Year", "Month"]
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
non_malaria_fig.for_each_annotation(
    lambda a: a.update(
        text=a.text.replace("Subcounty=", "")
   )
)

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

###
# Create 2 x 2 visualization
age_group_fig = make_subplots(
    rows=2,
    cols=2,

    subplot_titles=[
        "# Subjects with Fever",
        "# Subjects RDT Tested",
        "# Subjects with RDT+",
        "# Subjects with RDT+ and ACT"
    ],

    vertical_spacing=0.18,
    horizontal_spacing=0.10
)

years = year_age_summary["Year"].astype(int).astype(str)

# Colors similar to the example
under5_color = "#F8766D"
over5_color = "#00BFC4"


# 1. Subjects with Fever
age_group_fig.add_trace(
    go.Bar(
        x=years,
        y=year_age_summary["Fever_U5"],
        name="<5",
        legendgroup="<5",
        marker_color=under5_color,
        offsetgroup="u5",

        hovertemplate=(
            "Year: %{x}<br>"
            "Age Group: <5<br>"
            "Fever Cases: %{y:,.0f}"
            "<extra></extra>"
        )
    ),
    row=1,
    col=1
)

age_group_fig.add_trace(
    go.Bar(
        x=years,
        y=year_age_summary["Fever_5plus"],
        name="5+",
        legendgroup="5+",
        marker_color=over5_color,
        offsetgroup="5plus",

        hovertemplate=(
            "Year: %{x}<br>"
            "Age Group: 5+<br>"
            "Fever Cases: %{y:,.0f}"
            "<extra></extra>"
        )
    ),
    row=1,
    col=1
)

# 2. Subjects RDT Tested
age_group_fig.add_trace(
    go.Bar(
        x=years,
        y=year_age_summary["RDT_Tested_U5"],
        name="<5",
        legendgroup="<5",
        marker_color=under5_color,
        offsetgroup="u5",
        showlegend=False,

        hovertemplate=(
            "Year: %{x}<br>"
            "Age Group: <5<br>"
            "RDT Tested: %{y:,.0f}"
            "<extra></extra>"
        )
    ),
    row=1,
    col=2
)

age_group_fig.add_trace(
    go.Bar(
        x=years,
        y=year_age_summary["RDT_Tested_5plus"],
        name="5+",
        legendgroup="5+",
        marker_color=over5_color,
        offsetgroup="5plus",
        showlegend=False,

        hovertemplate=(
            "Year: %{x}<br>"
            "Age Group: 5+<br>"
            "RDT Tested: %{y:,.0f}"
            "<extra></extra>"
        )
    ),
    row=1,
    col=2
)

# 3. Subjects with RDT+
age_group_fig.add_trace(
    go.Bar(
        x=years,
        y=year_age_summary["RDT_Pos_U5"],
        name="<5",
        legendgroup="<5",
        marker_color=under5_color,
        offsetgroup="u5",
        showlegend=False,

        hovertemplate=(
            "Year: %{x}<br>"
            "Age Group: <5<br>"
            "RDT Positive: %{y:,.0f}"
            "<extra></extra>"
        )
    ),
    row=2,
    col=1
)

age_group_fig.add_trace(
    go.Bar(
        x=years,
        y=year_age_summary["RDT_Pos_5plus"],
        name="5+",
        legendgroup="5+",
        marker_color=over5_color,
        offsetgroup="5plus",
        showlegend=False,

        hovertemplate=(
            "Year: %{x}<br>"
            "Age Group: 5+<br>"
            "RDT Positive: %{y:,.0f}"
            "<extra></extra>"
        )
    ),
    row=2,
    col=1
)

# Figure formatting
age_group_fig.update_layout(
    template="plotly_white",

    barmode="group",

    height=750,

    margin=dict(
        l=60,
        r=30,
        t=100,
        b=60
    ),

    legend=dict(
        title="Age Group",
        orientation="h",
        x=0.5,
        xanchor="center",
        y=1.12,
        yanchor="bottom"
    ),

    bargap=0.25,
    bargroupgap=0.05
)


# X axis titles
age_group_fig.update_xaxes(
    title_text="Year",
    row=1,
    col=1
)

age_group_fig.update_xaxes(
    title_text="Year",
    row=1,
    col=2
)

age_group_fig.update_xaxes(
    title_text="Year",
    row=2,
    col=1
)

age_group_fig.update_xaxes(
    title_text="Year",
    row=2,
    col=2
)


# Y axis titles
age_group_fig.update_yaxes(
    title_text="Count",
    rangemode="tozero",
    row=1,
    col=1
)

age_group_fig.update_yaxes(
    title_text="Count",
    rangemode="tozero",
    row=1,
    col=2
)

age_group_fig.update_yaxes(
    title_text="Count",
    rangemode="tozero",
    row=2,
    col=1
)

age_group_fig.update_yaxes(
    title_text="Count",
    rangemode="tozero",
    row=2,
    col=2
)

# --------------------------------------------------------- #
# Prevalence Visualization
prevalence_fig = px.line(
    prevalence_long,

    x="Month",
    y="Prevalence",

    color="Age_Group",

    facet_col="Year",
    facet_row="Age_Group",

    error_y="CI",

    markers=True,

    category_orders={
        "Age_Group": ["<5", "5+"],
        "Year": sorted(
            prevalence_long["Year"]
            .dropna()
            .unique()
        )
    },

    color_discrete_map={
        "<5": "#F8766D",
        "5+": "#00BFC4"
    }
)


# Formatting
prevalence_fig.update_traces(
    line=dict(
        width=2.5
    ),

    marker=dict(
        size=6
    ),

    error_y=dict(
        thickness=1.5,
        width=4
    ),

    hovertemplate=(
        "Month: %{x}<br>"
        "Prevalence: %{y:.3f}"
        "<extra></extra>"
    )
)


# X axis
prevalence_fig.update_xaxes(
    title=None,

    tickmode="linear",
    tick0=1,
    dtick=1,

    range=[0.5, 12.5],

    showgrid=True,
    gridcolor="rgba(0,0,0,0.08)"
)


# Y axis
prevalence_fig.update_yaxes(
    title=None,

    range=[0, 1],

    tickformat=".1f",

    showgrid=True,
    gridcolor="rgba(0,0,0,0.08)"
)


# Clean facet labels
prevalence_fig.for_each_annotation(
    lambda a: a.update(
        text=(
            a.text
            .replace("Year=", "")
            .replace("Age_Group=", "")
        )
    )
)


prevalence_fig.update_layout(
    template="plotly_white",

    height=700,

    margin=dict(
        l=80,
        r=100,
        t=60,
        b=80
    ),

    legend=dict(
        title="Age Group",
        orientation="v",
        x=1.01,
        y=0.5,
        yanchor="middle"
    ),

    hovermode="closest"
)

# Shared X-axis label
prevalence_fig.add_annotation(
    text="Month",
    x=0.5,
    y=-0.10,
    xref="paper",
    yref="paper",
    showarrow=False,
    font=dict(size=15)
)


# Shared Y-axis label
prevalence_fig.add_annotation(
    text="Prevalence",
    x=-0.06,
    y=0.5,
    xref="paper",
    yref="paper",
    textangle=-90,
    showarrow=False,
    font=dict(size=15)
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

        dbc.Card(
            dbc.CardBody([
                html.H4(
                    "Fever Testing and Treatment by Age Group",
                    className="fw-bold mb-1"
                ),
        
                html.P(
                    "Annual fever cases, malaria testing, positive RDT results, and treatment by age group across all subcounties.",
                    className="text-muted mb-4"
                ),
        
                dcc.Graph(
                    id="malaria-age-summary",
                    figure=age_group_fig,
                    config={"displayModeBar": False}
                )
            ]),
            className="border-0 shadow-sm mb-4"
        ),

        dbc.Card(
            dbc.CardBody([
                html.H4(
                    "Malaria Estimated Prevalence by Age Group and Year",
                    className="fw-bold mb-1"
                ),
        
                html.P(
                    "Monthly estimated malaria prevalence among RDT-tested fever cases by age group across all subcounties.",
                    className="text-muted mb-4"
                ),
        
                dcc.Graph(
                    id="malaria-prevalence-age-year",
                    figure=prevalence_fig,
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
