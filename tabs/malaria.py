from dash import callback, Input, Output, html, dcc
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import glob
import os
import gdown

# THEME
PRIMARY = "#274C77"
PRIMARY_DARK = "#1F3B5B"
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

#====================================================================
# Bednet data
BEDNET_URL = ("https://drive.google.com/drive/folders/1M3EJCQDhv5IUjFTMSPXN4OLJm8L0dfMv?usp=sharing")
BEDNET_FOLDER = "/tmp/Bednet_Data"
os.makedirs(BEDNET_FOLDER,exist_ok=True)

# Download Bednet folder from Google Drive
gdown.download_folder(
    url=BEDNET_URL,
    output=BEDNET_FOLDER,
    quiet=False,
    use_cookies=False
)

# Find Excel files
bednet_files = glob.glob(
    os.path.join(
        BEDNET_FOLDER,
        "*.xlsx"
    )
)

if not bednet_files:
    raise ValueError("No Excel files were found.")


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

#==============================================================================
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


#===================================================
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


# =========================================================
# SANKEY - helper function 
def format_sankey_value(value):
    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    elif value >= 1_000:
        return f"{value / 1_000:.0f}k"
    else:
        return f"{value:,.0f}"


def format_sankey_label(name, value, total):
    percent = (value / total) * 100 if total > 0 else 0

    return (
        f"{name}<br>"
        f"{format_sankey_value(value)} ({percent:.0f}%)"
    )


def create_sankey_figure(data):
    # Fever cases
    under5_cases = (pd.to_numeric(data["Cases.Fever < 5"],errors="coerce").fillna(0).sum())
    over5_cases = (pd.to_numeric(data["Cases.Fever >= 5"],errors="coerce").fillna(0).sum())

    # RDT positive
    positive_under5 = (pd.to_numeric(data["Cases.Fever.with.RDT.Positive < 5"],errors="coerce").fillna(0).sum())
    positive_over5 = (pd.to_numeric(data["Cases.Fever.with.RDT.Positive >= 5"],errors="coerce").fillna(0).sum())

    # RDT negative
    negative_under5 = (pd.to_numeric(data["Cases.Fever.with.RDT. negative < 5"],errors="coerce").fillna(0).sum())
    negative_over5 = (pd.to_numeric(data["Cases.Fever.with.RDT. negative >= 5"],errors="coerce").fillna(0).sum())

    # Not tested
    not_tested_under5 = max(under5_cases - positive_under5 - negative_under5,0)
    not_tested_over5 = max(over5_cases - positive_over5 - negative_over5,0)
    total_fever_cases = under5_cases + over5_cases

    # Node labels with counts and percentages
    sankey_labels = [
        format_sankey_label(
            "Fever Cases",
            total_fever_cases,
            total_fever_cases
        ),
        format_sankey_label(
            "Children <5",
            under5_cases,
            total_fever_cases
        ),
        format_sankey_label(
            "Individuals ≥5",
            over5_cases,
            total_fever_cases
        ),
        format_sankey_label(
            "RDT Positive <5",
            positive_under5,
            under5_cases
        ),
        format_sankey_label(
            "RDT Negative <5",
            negative_under5,
            under5_cases
        ),
        format_sankey_label(
            "Not Tested <5",
            not_tested_under5,
            under5_cases
        ),
        format_sankey_label(
            "RDT Positive ≥5",
            positive_over5,
            over5_cases
        ),
        format_sankey_label(
            "RDT Negative ≥5",
            negative_over5,
            over5_cases
        ),
        format_sankey_label(
            "Not Tested ≥5",
            not_tested_over5,
            over5_cases
        ),
    ]

    link_values = [
        under5_cases,
        over5_cases,
        positive_under5,
        negative_under5,
        not_tested_under5,
        positive_over5,
        negative_over5,
        not_tested_over5,
    ]

    link_totals = [
        total_fever_cases,
        total_fever_cases,
        under5_cases,
        under5_cases,
        under5_cases,
        over5_cases,
        over5_cases,
        over5_cases,
    ]

    link_customdata = []

    for value, total in zip(link_values, link_totals):
        percent = (value / total) * 100 if total > 0 else 0

        link_customdata.append(
            f"{format_sankey_value(value)} ({percent:.1f}%)"
        )

    sankey_fig = go.Figure(
        go.Sankey(
            arrangement="snap",

            node=dict(
                pad=30,
                thickness=24,

                line=dict(
                    color="#FFFFFF",
                    width=1.5,
                ),

                label=sankey_labels,

                # Restrained research-dashboard palette
                color=[
                    "#274C77",
                    "#708EAA",
                    "#557C71",
                    "#A95D5D",
                    "#BDA46D",
                    "#8A9199",
                    "#8F4F4F",
                    "#C4B17C",
                    "#9AA0A6",
                ],

                hovertemplate=(
                    "%{label}"
                    "<extra></extra>"
                ),
            ),

            link=dict(
                source=[
                    0, 0,
                    1, 1, 1,
                    2, 2, 2,
                ],

                target=[
                    1, 2,
                    3, 4, 5,
                    6, 7, 8,
                ],

                value=link_values,
                customdata=link_customdata,

                color=[
                    "rgba(112,142,170,0.30)",
                    "rgba(85,124,113,0.30)",
                    "rgba(169,93,93,0.30)",
                    "rgba(189,164,109,0.30)",
                    "rgba(138,145,153,0.25)",
                    "rgba(143,79,79,0.30)",
                    "rgba(196,177,124,0.30)",
                    "rgba(154,160,166,0.25)",
                ],

                hovertemplate=(
                    "<b>%{source.label}</b>"
                    "<br>to"
                    "<br><b>%{target.label}</b>"
                    "<br><br>"
                    "%{customdata}"
                    "<extra></extra>"
                ),
            ),
        )
    )

    sankey_fig.update_layout(
        template="plotly_white",
        height=680,

        margin=dict(
            l=30,
            r=30,
            t=20,
            b=20,
        ),

        paper_bgcolor="white",

        font=dict(
            family="Segoe UI",
            size=14,
            color=TEXT,
        ),
    )

    return sankey_fig

# Initial Sankey
fever_age_fig = create_sankey_figure(df)

# =========================================================
# COMMODITY STOCK + WEIGHT-BASED ACT DATA
# Aggregate all available records by month.
# This prevents multiple bars from being drawn on top of each other for the same month.
commodity_monthly = (
    df
    .groupby("Month", as_index=False)
    .agg(
        Stock_mRDTs=("Stock mRDTs", "sum"),
        Stock_ACTs=("Stock ACTs", "sum"),

        Weight_5_15=(
            "CHEW Weight band 5 to <15 kg  (<3 yrs)",
            "sum"
        ),

        Weight_15_25=(
            "CHEW Weight band 15 to <25 kg  (3 to <8 yrs)",
            "sum"
        ),

        Weight_25_35=(
            "CHEW Weight band 25 to <35 kg (8 to <12 yrs)",
            "sum"
        ),

        Weight_35plus=(
            "CHEW Weight band ≥ 35 kg (≥ 12 yrs)",
            "sum"
        ),
    )
    .sort_values("Month")
)

# =========================================================
# COMMODITY STOCK LEVELS
stock_fig = go.Figure()

stock_fig.add_trace(
    go.Bar(
        x=commodity_monthly["Month"],
        y=commodity_monthly["Stock_mRDTs"],

        name="mRDT Stock",

        marker_color="#527A9B",

        hovertemplate=(
            "Month: %{x}<br>"
            "mRDT Stock: %{y:,.0f}"
            "<extra></extra>"
        ),
    )
)


stock_fig.add_trace(
    go.Bar(
        x=commodity_monthly["Month"],
        y=commodity_monthly["Stock_ACTs"],

        name="ACT Stock",

        marker_color="#688B78",

        hovertemplate=(
            "Month: %{x}<br>"
            "ACT Stock: %{y:,.0f}"
            "<extra></extra>"
        ),
    )
)


stock_fig.update_layout(
    barmode="group",
    template="plotly_white",

    height=450,

    margin=dict(
        l=55,
        r=20,
        t=45,
        b=55
    ),

    font=dict(
        family="Segoe UI",
        size=13,
        color=TEXT,
    ),

    paper_bgcolor="white",
    plot_bgcolor="white",

    legend=dict(
        orientation="h",
        x=0.5,
        xanchor="center",
        y=1.08,
        yanchor="bottom",
    ),

    bargap=0.25,
    bargroupgap=0.08,
)


stock_fig.update_xaxes(
    title_text="Month",

    tickmode="array",
    tickvals=list(range(1, 13)),

    ticktext=[
        "Jan", "Feb", "Mar", "Apr",
        "May", "Jun", "Jul", "Aug",
        "Sep", "Oct", "Nov", "Dec"
    ],

    showgrid=False,
)


stock_fig.update_yaxes(
    title_text="Stock level (count)",
    gridcolor="#EDF1F4",
    zeroline=False,
)


# =========================================================
# WEIGHT-BASED ACT DISTRIBUTION
weight_fig = go.Figure()

weight_fig.add_trace(
    go.Bar(
        name="5 to <15 kg (<3 yrs old)",

        x=commodity_monthly["Month"],
        y=commodity_monthly["Weight_5_15"],

        marker_color="#6C8EBF",

        hovertemplate=(
            "Month: %{x}<br>"
            "5 to <15 kg: %{y:,.0f}"
            "<extra></extra>"
        ),
    )
)


weight_fig.add_trace(
    go.Bar(
        name="15 to <25 kg (3 to <8 yrs old)",

        x=commodity_monthly["Month"],
        y=commodity_monthly["Weight_15_25"],

        marker_color="#7F9F8D",

        hovertemplate=(
            "Month: %{x}<br>"
            "15 to <25 kg: %{y:,.0f}"
            "<extra></extra>"
        ),
    )
)


weight_fig.add_trace(
    go.Bar(
        name="25 to <35 kg (8 to <12 yrs old)",

        x=commodity_monthly["Month"],
        y=commodity_monthly["Weight_25_35"],

        marker_color="#B5A07A",

        hovertemplate=(
            "Month: %{x}<br>"
            "25 to <35 kg: %{y:,.0f}"
            "<extra></extra>"
        ),
    )
)


weight_fig.add_trace(
    go.Bar(
        name="≥35 kg (≥12 yrs old)",

        x=commodity_monthly["Month"],
        y=commodity_monthly["Weight_35plus"],

        marker_color="#8A6F73",

        hovertemplate=(
            "Month: %{x}<br>"
            "≥35 kg: %{y:,.0f}"
            "<extra></extra>"
        ),
    )
)


weight_fig.update_layout(
    barmode="stack",
    template="plotly_white",

    height=450,

    margin=dict(
        l=55,
        r=20,
        t=45,
        b=55
    ),

    font=dict(
        family="Segoe UI",
        size=13,
        color=TEXT,
    ),

    paper_bgcolor="white",
    plot_bgcolor="white",

    legend=dict(
        orientation="h",
        x=0.5,
        xanchor="center",
        y=1.10,
        yanchor="bottom",
    ),

    bargap=0.25,
)


weight_fig.update_xaxes(
    title_text="Month",

    tickmode="array",
    tickvals=list(range(1, 13)),

    ticktext=[
        "Jan", "Feb", "Mar", "Apr",
        "May", "Jun", "Jul", "Aug",
        "Sep", "Oct", "Nov", "Dec"
    ],

    showgrid=False,
)


weight_fig.update_yaxes(
    title_text="ACT distribution (count)",
    gridcolor="#EDF1F4",
    zeroline=False,
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
non_malaria_data["Subcounty"] = (non_malaria_data["Subcounty"].astype(str).str.replace(" Sub County", "", regex=False).str.strip())

# Sort data by Subcounty and date
non_malaria_data = non_malaria_data.sort_values(["Subcounty", "Date"])

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

#====================================================
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


# Subjects with Fever
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

# Subjects RDT Tested
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

# Subjects with RDT+
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

#===========================================================
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


#=====================================================
# Proportion of Non-Malarial Fever
# by Year, Subcounty, and Age Group

non_malaria_age = df.copy()

# Clean subcounty names for visualization
non_malaria_age["Subcounty"] = (
    non_malaria_age["Subcounty"]
    .astype(str)
    .str.replace(" Sub County", "", regex=False)
    .str.strip()
)

# Make sure values are numeric
numeric_cols = [
    "Cases.Fever < 5",
    "Cases.Fever >= 5",
    "Cases.Fever.with.RDT. negative < 5",
    "Cases.Fever.with.RDT. negative >= 5",
]

for col in numeric_cols:
    non_malaria_age[col] = pd.to_numeric(
        non_malaria_age[col],
        errors="coerce"
    ).fillna(0)

non_malaria_age["Year"] = pd.to_numeric(
    non_malaria_age["Year"],
    errors="coerce"
)

non_malaria_age_summary = (
    non_malaria_age
    .groupby(
        ["Year", "Subcounty"],
        as_index=False
    )
    .agg(
        Fever_U5=(
            "Cases.Fever < 5",
            "sum"
        ),

        Fever_5plus=(
            "Cases.Fever >= 5",
            "sum"
        ),

        Negative_U5=(
            "Cases.Fever.with.RDT. negative < 5",
            "sum"
        ),

        Negative_5plus=(
            "Cases.Fever.with.RDT. negative >= 5",
            "sum"
        )
    )
)

non_malaria_age_summary["Percent_U5"] = np.where(
    non_malaria_age_summary["Fever_U5"] > 0,

    (
        non_malaria_age_summary["Negative_U5"]
        / non_malaria_age_summary["Fever_U5"]
    ) * 100,

    np.nan
)

non_malaria_age_summary["Percent_5plus"] = np.where(
    non_malaria_age_summary["Fever_5plus"] > 0,

    (
        non_malaria_age_summary["Negative_5plus"]
        / non_malaria_age_summary["Fever_5plus"]
    ) * 100,

    np.nan
)

u5_df = non_malaria_age_summary[
    ["Year", "Subcounty", "Percent_U5"]
].copy()

u5_df["Age_Group"] = "<5"

u5_df.rename(
    columns={
        "Percent_U5": "Non_Malarial_Percent"
    },
    inplace=True
)


plus5_df = non_malaria_age_summary[
    ["Year", "Subcounty", "Percent_5plus"]
].copy()

plus5_df["Age_Group"] = "5+"

plus5_df.rename(
    columns={
        "Percent_5plus": "Non_Malarial_Percent"
    },
    inplace=True
)


non_malaria_age_long = pd.concat(
    [u5_df, plus5_df],
    ignore_index=True
)

# ============================================
# Visualization
non_malaria_age_fig = px.bar(
    non_malaria_age_long,

    x="Year",
    y="Non_Malarial_Percent",

    color="Subcounty",

    facet_col="Age_Group",

    barmode="group",

    category_orders={
        "Age_Group": ["<5", "5+"],

        "Subcounty": [
            "Alego Usonga",
            "Bondo",
            "Gem",
            "Rarieda",
            "Ugenya",
            "Ugunja"
        ]
    },

    labels={
        "Year": "Year",
        "Non_Malarial_Percent": "% Non-Malarial Fever",
        "Subcounty": "SubCounty"
    }
)

# Formatting
# Clean facet titles
non_malaria_age_fig.for_each_annotation(
    lambda a: a.update(
        text=a.text.replace("Age_Group=", "")
    )
)


non_malaria_age_fig.update_traces(
    hovertemplate=(
        "Year: %{x}<br>"
        "Non-Malarial Fever: %{y:.1f}%"
        "<extra></extra>"
    )
)


non_malaria_age_fig.update_yaxes(
    ticksuffix="%",
    rangemode="tozero",

    showgrid=True,
    gridcolor="rgba(0,0,0,0.08)",

    title=None
)

non_malaria_age_fig.update_xaxes(
    title=None,

    tickmode="linear",
    dtick=1,

    showgrid=True,
    gridcolor="rgba(0,0,0,0.08)"
)

non_malaria_age_fig.update_layout(
    template="plotly_white",

    height=600,

    margin=dict(
        l=80,
        r=140,
        t=60,
        b=80
    ),

    legend_title_text="SubCounty",

    legend=dict(
        orientation="v",
        x=1.02,
        y=0.5,
        yanchor="middle"
    ),

    bargap=0.20,
    bargroupgap=0.03
)

# Shared X-axis title
non_malaria_age_fig.add_annotation(
    text="Year",

    x=0.5,
    y=-0.11,

    xref="paper",
    yref="paper",

    showarrow=False,

    font=dict(
        size=16
    )
)

# Shared Y-axis title
non_malaria_age_fig.add_annotation(
    text="% Non-Malarial Fever",

    x=-0.06,
    y=0.5,

    xref="paper",
    yref="paper",

    textangle=-90,

    showarrow=False,

    font=dict(
        size=16
    )
)

#=====================================================
# Distribution of Non-Malarial Fever
# by Subcounty and Age Group
box_data = df.copy()

# Clean subcounty names for display
box_data["Subcounty"] = (
    box_data["Subcounty"]
    .astype(str)
    .str.replace(" Sub County", "", regex=False)
    .str.strip()
)

# Make sure needed columns are numeric
numeric_cols = [
    "Cases.Fever < 5",
    "Cases.Fever >= 5",
    "Cases.Fever.with.RDT. negative < 5",
    "Cases.Fever.with.RDT. negative >= 5",
]

for col in numeric_cols:
    box_data[col] = pd.to_numeric(
        box_data[col],
        errors="coerce"
    )


box_data["Percent_U5"] = np.where(
    box_data["Cases.Fever < 5"] > 0,
    (
        box_data["Cases.Fever.with.RDT. negative < 5"]
        / box_data["Cases.Fever < 5"]
    ) * 100,
    np.nan
)

box_data["Percent_5plus"] = np.where(
    box_data["Cases.Fever >= 5"] > 0,
    (
        box_data["Cases.Fever.with.RDT. negative >= 5"]
        / box_data["Cases.Fever >= 5"]
    ) * 100,
    np.nan
)

# Long format for Plotly
box_u5 = box_data[
    ["Subcounty", "Year", "Month", "Percent_U5"]
].copy()

box_u5["Age_Group"] = "<5"

box_u5.rename(
    columns={
        "Percent_U5": "Non_Malarial_Percent"
    },
    inplace=True
)


box_5plus = box_data[
    ["Subcounty", "Year", "Month", "Percent_5plus"]
].copy()

box_5plus["Age_Group"] = "5+"

box_5plus.rename(
    columns={
        "Percent_5plus": "Non_Malarial_Percent"
    },
    inplace=True
)


box_long = pd.concat(
    [box_u5, box_5plus],
    ignore_index=True
)

# Remove missing percentages
box_long = box_long.dropna(
    subset=["Non_Malarial_Percent"]
)

# ---
# Boxplot visualization
non_malaria_box_fig = px.box(
    box_long,

    x="Subcounty",
    y="Non_Malarial_Percent",

    color="Age_Group",

    category_orders={
        "Subcounty": [
            "Alego Usonga",
            "Bondo",
            "Gem",
            "Rarieda",
            "Ugenya",
            "Ugunja"
        ],
        "Age_Group": ["<5", "5+"]
    },

    color_discrete_map={
        "<5": "#F8766D",
        "5+": "#00BFC4"
    },

    labels={
        "Subcounty": "Subcounty",
        "Non_Malarial_Percent": "% Non-Malarial Fever",
        "Age_Group": "AgeGroup"
    }
)

# Formatting
non_malaria_box_fig.update_traces(
    boxpoints="outliers",
    jitter=0,
    pointpos=0,

    line=dict(
        width=1.5
    ),

    marker=dict(
        size=6
    ),

    hovertemplate=(
        "Subcounty: %{x}<br>"
        "Non-Malarial Fever: %{y:.1f}%"
        "<extra></extra>"
    )
)

non_malaria_box_fig.update_yaxes(
    ticksuffix="%",
    rangemode="tozero",

    showgrid=True,
    gridcolor="rgba(0,0,0,0.08)",

    title_text="% Non-Malarial Fever"
)

non_malaria_box_fig.update_xaxes(
    title_text="Subcounty",

    showgrid=True,
    gridcolor="rgba(0,0,0,0.08)"
)

non_malaria_box_fig.update_layout(
    template="plotly_white",

    height=600,

    margin=dict(
        l=70,
        r=130,
        t=30,
        b=70
    ),

    boxmode="group",

    legend_title_text="AgeGroup",

    legend=dict(
        orientation="v",
        x=1.02,
        y=0.5,
        yanchor="middle"
    )
)

# =========================================================
# LAYOUT
layout = dbc.Container(
    [
        # =================================================
        # MALARIA SURVEILLANCE OVERVIEW + FILTERS
        dbc.Card(
            dbc.CardBody(
                [
                    #Title
                    html.H3(
                        "Malaria Surveillance Overview",
                        className="fw-bold mb-1",
                        style={"color": "#274C77","fontSize": "28px",},
                    ),
                    # Small divider under title
                    html.Div(
                        style={
                            "width": "55px",
                            "height": "3px",
                            "backgroundColor": "#274C77",
                            "borderRadius": "2px",
                            "marginBottom": "24px",
                        }
                    ),

                    html.P(
                        "Malaria remains a major public health concern in Siaya County, "
                        "with transmission patterns varying across subcounties due to differences "
                        "in environmental conditions, population characteristics, healthcare access, "
                        "and malaria prevention efforts. This dashboard provides an overview of malaria-related "
                        "fever cases, diagnostic testing, treatment outcomes, and commodity availability. "
                        "By comparing trends across the six subcounties, users can identify differences "
                        "in disease burden, healthcare utilization, testing practices, treatment coverage, "
                        "and resource availability. Use the filters below to explore malaria surveillance "
                        "indicators by subcounty and year.",
                        className="mb-4",
                        style={
                            "color": "#1F2937",
                            "fontSize": "20px",
                            "lineHeight": "1.8",
                        },
                    ),

                    html.Div(
                        [
                            dbc.Row(
                                [

                                    dbc.Col(
                                        [

                                            html.Label(
                                                "Subcounty",
                                                className="fw-semibold mb-2",
                                                style={
                                                    "color": TEXT,
                                                    "fontSize": "18px",
                                                },
                                            ),

                                            dcc.Dropdown(
                                                id="malaria-subcounty-dropdown",

                                                options=[
                                                    {
                                                        "label": "All Subcounties",
                                                        "value": "ALL",
                                                    }
                                                ]
                                                +
                                                [
                                                    {
                                                        "label": str(s).replace(
                                                            " Sub County",
                                                            ""
                                                        ),
                                                        "value": str(s),
                                                    }

                                                    for s in sorted(
                                                        df["Subcounty"]
                                                        .dropna()
                                                        .unique()
                                                    )
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
                                                className="fw-semibold mb-2",
                                                style={
                                                    "color": TEXT,
                                                    "fontSize": "18px",
                                                },
                                            ),

                                            dcc.Dropdown(
                                                id="malaria-year-dropdown",

                                                options=[
                                                    {
                                                        "label": "All Years",
                                                        "value": "ALL",
                                                    }
                                                ]
                                                +
                                                [
                                                    {
                                                        "label": str(int(y)),
                                                        "value": str(int(y)),
                                                    }

                                                    for y in sorted(
                                                        df["Year"]
                                                        .dropna()
                                                        .unique()
                                                    )
                                                ],

                                                value="ALL",
                                                clearable=False,
                                            ),

                                        ],
                                        lg=4,
                                    ),

                                ],
                                className="g-3",
                            )
                        ],
                    ),
                ],
                style={
                    "padding": "24px",
                },
            ),

            style=CARD_STYLE,
            className="mb-4",
        ),


        # =================================================
        # SANKEY
        dbc.Card(
            dbc.CardBody(
                [

                    html.H4(
                        "Fever Cases by Age Group and RDT Outcome",
                        className="fw-bold mb-1",
                        style={"color": TEXT},
                    ),

                    html.P(
                        "Flow of reported fever cases from age group to malaria "
                        "diagnostic outcome. Counts and proportions are shown for "
                        "each stage of the diagnostic pathway.",
                        className="mb-4",
                        style={
                            "color": TEXT_MUTED,
                            "fontSize": "14px",
                        },
                    ),

                    dcc.Graph(
                        id="malaria-sankey",
                        figure=fever_age_fig,
                        config={
                            "displayModeBar": False,
                            "responsive": True,
                        },
                        style={
                            "height": "680px",
                        },
                    ),

                ],
                style={
                    "padding": "24px",
                },
            ),

            style=CARD_STYLE,
            className="mb-4",
        ),

        # =================================================
        # COMMODITY / ACT DISTRIBUTION
        dbc.Row(
            [
                # COMMODITY STOCK LEVELS
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
        
                                html.H5(
                                    "Commodity Stock Levels",
                                    className="fw-bold mb-1",
                                    style={
                                        "color": TEXT,
                                    },
                                ),
        
                                html.P(
                                    "Monthly mRDT and ACT stock availability.",
                                    className="mb-3",
                                    style={
                                        "color": TEXT_MUTED,
                                        "fontSize": "14px",
                                    },
                                ),
        
                                dcc.Graph(
                                    id="malaria-stock",
                                    figure=stock_fig,
        
                                    config={
                                        "displayModeBar": False,
                                        "responsive": True,
                                    },
        
                                    style={
                                        "height": "450px",
                                        "width": "100%",
                                    },
                                ),
        
                            ],
        
                            style={
                                "padding": "22px",
                            },
                        ),
        
                        style={
                            **CARD_STYLE,
        
                            # IMPORTANT:
                            # fixed/controlled card height
                            "height": "550px",
                        },
                    ),
        
                    lg=6,
                    className="mb-4",
                ),
        
                # =================================================
                # WEIGHT-BASED ACT DISTRIBUTION
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
        
                                html.H5(
                                    "Weight-Based ACT Distribution",
                                    className="fw-bold mb-1",
                                    style={
                                        "color": TEXT,
                                    },
                                ),
        
                                html.P(
                                    "Monthly ACT distribution across weight categories "
                                    "and corresponding age guides.",
                                    className="mb-3",
                                    style={
                                        "color": TEXT_MUTED,
                                        "fontSize": "14px",
                                    },
                                ),
        
                                dcc.Graph(
                                    id="malaria-weight",
                                    figure=weight_fig,
        
                                    config={
                                        "displayModeBar": False,
                                        "responsive": True,
                                    },
        
                                    style={
                                        "height": "450px",
                                        "width": "100%",
                                    },
                                ),
        
                            ],
        
                            style={
                                "padding": "22px",
                            },
                        ),
        
                        style={
                            **CARD_STYLE,
        
                            # Same height as left card
                            "height": "550px",
                        },
                    ),
        
                    lg=6,
                    className="mb-4",
                ),
        
            ],
        
            # Do NOT use align-items-stretch here
            className="mb-2",
        ),

        # =================================================
        # NON-MALARIAL FEVER OVER TIME
        dbc.Card(
            dbc.CardBody(
                [

                    html.H4(
                        "Proportion of Non-Malarial Fever Cases",
                        className="fw-bold mb-1",
                        style={"color": TEXT},
                    ),

                    html.P(
                        "Monthly proportion of reported fever cases that tested "
                        "negative for malaria across all subcounties.",
                        className="mb-4",
                        style={
                            "color": TEXT_MUTED,
                            "fontSize": "14px",
                        },
                    ),

                    dcc.Graph(
                        id="non-malaria-fever",
                        figure=non_malaria_fig,
                        config={
                            "displayModeBar": False,
                            "responsive": True,
                        },
                    ),

                ],
                style={"padding": "24px"},
            ),

            style=CARD_STYLE,
            className="mb-4",
        ),

        # =================================================
        # FEVER TESTING AND TREATMENT
        dbc.Card(
            dbc.CardBody(
                [

                    html.H4(
                        "Fever Testing and Treatment by Age Group",
                        className="fw-bold mb-1",
                        style={"color": TEXT},
                    ),

                    html.P(
                        "Annual fever cases, malaria testing, positive RDT results, "
                        "and treatment by age group across all subcounties.",
                        className="mb-4",
                        style={
                            "color": TEXT_MUTED,
                            "fontSize": "14px",
                        },
                    ),

                    dcc.Graph(
                        id="malaria-age-summary",
                        figure=age_group_fig,
                        config={
                            "displayModeBar": False,
                            "responsive": True,
                        },
                    ),

                ],
                style={"padding": "24px"},
            ),

            style=CARD_STYLE,
            className="mb-4",
        ),

        # =================================================
        # NON-MALARIAL FEVER BY YEAR / COUNTY / AGE
        dbc.Card(
            dbc.CardBody(
                [

                    html.H4(
                        "Proportion of Non-Malarial Fever by Year, Subcounty, and Age Group",
                        className="fw-bold mb-1",
                        style={"color": TEXT},
                    ),

                    html.P(
                        "Annual proportion of reported fever cases that tested "
                        "negative for malaria by age group and subcounty.",
                        className="mb-4",
                        style={
                            "color": TEXT_MUTED,
                            "fontSize": "14px",
                        },
                    ),

                    dcc.Graph(
                        id="non-malaria-age-group",
                        figure=non_malaria_age_fig,
                        config={
                            "displayModeBar": False,
                            "responsive": True,
                        },
                    ),

                ],
                style={"padding": "24px"},
            ),

            style=CARD_STYLE,
            className="mb-4",
        ),


        # =================================================
        # MALARIA PREVALENCE
        dbc.Card(
            dbc.CardBody(
                [

                    html.H4(
                        "Malaria Estimated Prevalence by Age Group and Year",
                        className="fw-bold mb-1",
                        style={"color": TEXT},
                    ),

                    html.P(
                        "Monthly estimated malaria prevalence among RDT-tested "
                        "fever cases by age group across all subcounties.",
                        className="mb-4",
                        style={
                            "color": TEXT_MUTED,
                            "fontSize": "14px",
                        },
                    ),

                    dcc.Graph(
                        id="malaria-prevalence-age-year",
                        figure=prevalence_fig,
                        config={
                            "displayModeBar": False,
                            "responsive": True,
                        },
                    ),

                ],
                style={"padding": "24px"},
            ),

            style=CARD_STYLE,
            className="mb-4",
        ),


        # =================================================
        # NON-MALARIAL FEVER DISTRIBUTION
        dbc.Card(
            dbc.CardBody(
                [

                    html.H4(
                        "Distribution of Non-Malarial Fever by Subcounty and Age Group",
                        className="fw-bold mb-1",
                        style={"color": TEXT},
                    ),

                    html.P(
                        "Distribution of monthly non-malarial fever percentages "
                        "across all years by subcounty and age group.",
                        className="mb-4",
                        style={
                            "color": TEXT_MUTED,
                            "fontSize": "14px",
                        },
                    ),

                    dcc.Graph(
                        id="non-malaria-boxplot",
                        figure=non_malaria_box_fig,
                        config={
                            "displayModeBar": False,
                            "responsive": True,
                        },
                    ),

                ],
                style={"padding": "24px"},
            ),

            style=CARD_STYLE,
            className="mb-4",
        ),

        # =================================================
        # BED NET DISTRIBUTION
        dbc.Card(
            dbc.CardBody(
                [

                    html.H5(
                        "ANC Bed Net Distribution",
                        className="fw-bold mb-1",
                        style={"color": TEXT},
                    ),

                    html.P(
                        "Long-lasting insecticidal nets distributed to antenatal "
                        "care clients.",
                        className="mb-3",
                        style={
                            "color": TEXT_MUTED,
                            "fontSize": "14px",
                        },
                    ),

                    dcc.Graph(
                        figure=bednet_fig,
                        config={
                            "displayModeBar": False,
                            "responsive": True,
                        },
                    ),

                ],
                style={"padding": "22px"},
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

# =========================================================
# MALARIA CALLBACK
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

    # =====================================================
    # SANKEY
    sankey_fig = create_sankey_figure(filtered_df)

    # =========================================================
    # AGGREGATE COMMODITY DATA BY MONTH
    commodity_filtered = (
        filtered_df
        .groupby("Month", as_index=False)
        .agg(
            Stock_mRDTs=("Stock mRDTs", "sum"),
            Stock_ACTs=("Stock ACTs", "sum"),
    
            Weight_5_15=(
                "CHEW Weight band 5 to <15 kg  (<3 yrs)",
                "sum"
            ),
    
            Weight_15_25=(
                "CHEW Weight band 15 to <25 kg  (3 to <8 yrs)",
                "sum"
            ),
    
            Weight_25_35=(
                "CHEW Weight band 25 to <35 kg (8 to <12 yrs)",
                "sum"
            ),
    
            Weight_35plus=(
                "CHEW Weight band ≥ 35 kg (≥ 12 yrs)",
                "sum"
            ),
        )
        .sort_values("Month")
    )
    
    
    # =========================================================
    # COMMODITY STOCK LEVELS
    stock_fig = go.Figure()
    
    stock_fig.add_trace(
        go.Bar(
            x=commodity_filtered["Month"],
            y=commodity_filtered["Stock_mRDTs"],
            name="mRDT Stock",
            marker_color="#527A9B",
    
            hovertemplate=(
                "Month: %{x}<br>"
                "mRDT Stock: %{y:,.0f}"
                "<extra></extra>"
            ),
        )
    )
    
    stock_fig.add_trace(
        go.Bar(
            x=commodity_filtered["Month"],
            y=commodity_filtered["Stock_ACTs"],
            name="ACT Stock",
            marker_color="#688B78",
    
            hovertemplate=(
                "Month: %{x}<br>"
                "ACT Stock: %{y:,.0f}"
                "<extra></extra>"
            ),
        )
    )
    
    stock_fig.update_layout(
        barmode="group",
        template="plotly_white",
        height=450,
    
        margin=dict(
            l=55,
            r=20,
            t=45,
            b=55,
        ),
    
        font=dict(
            family="Segoe UI",
            size=13,
            color=TEXT,
        ),
    
        paper_bgcolor="white",
        plot_bgcolor="white",
    
        legend=dict(
            orientation="h",
            x=0.5,
            xanchor="center",
            y=1.08,
            yanchor="bottom",
        ),
    
        bargap=0.25,
        bargroupgap=0.08,
    )
    
    stock_fig.update_xaxes(
        title_text="Month",
    
        tickmode="array",
        tickvals=list(range(1, 13)),
    
        ticktext=[
            "Jan", "Feb", "Mar", "Apr",
            "May", "Jun", "Jul", "Aug",
            "Sep", "Oct", "Nov", "Dec",
        ],
    
        showgrid=False,
    )
    
    stock_fig.update_yaxes(
        title_text="Stock level (count)",
        gridcolor="#EDF1F4",
        zeroline=False,
    )
    
    # =========================================================
    # WEIGHT-BASED ACT DISTRIBUTION
    weight_fig = go.Figure()
    
    weight_fig.add_trace(
        go.Bar(
            x=commodity_filtered["Month"],
            y=commodity_filtered["Weight_5_15"],
    
            name="5 to <15 kg (<3 yrs old)",
            marker_color="#6C8EBF",
    
            hovertemplate=(
                "Month: %{x}<br>"
                "5 to <15 kg: %{y:,.0f}"
                "<extra></extra>"
            ),
        )
    )
    
    weight_fig.add_trace(
        go.Bar(
            x=commodity_filtered["Month"],
            y=commodity_filtered["Weight_15_25"],
    
            name="15 to <25 kg (3 to <8 yrs old)",
            marker_color="#7F9F8D",
    
            hovertemplate=(
                "Month: %{x}<br>"
                "15 to <25 kg: %{y:,.0f}"
                "<extra></extra>"
            ),
        )
    )
    
    weight_fig.add_trace(
        go.Bar(
            x=commodity_filtered["Month"],
            y=commodity_filtered["Weight_25_35"],
    
            name="25 to <35 kg (8 to <12 yrs old)",
            marker_color="#B5A07A",
    
            hovertemplate=(
                "Month: %{x}<br>"
                "25 to <35 kg: %{y:,.0f}"
                "<extra></extra>"
            ),
        )
    )
    
    weight_fig.add_trace(
        go.Bar(
            x=commodity_filtered["Month"],
            y=commodity_filtered["Weight_35plus"],
    
            name="≥35 kg (≥12 yrs old)",
            marker_color="#8A6F73",
    
            hovertemplate=(
                "Month: %{x}<br>"
                "≥35 kg: %{y:,.0f}"
                "<extra></extra>"
            ),
        )
    )
    
    weight_fig.update_layout(
        barmode="stack",
        template="plotly_white",
        height=450,
    
        margin=dict(
            l=55,
            r=20,
            t=45,
            b=55,
        ),
    
        font=dict(
            family="Segoe UI",
            size=13,
            color=TEXT,
        ),
    
        paper_bgcolor="white",
        plot_bgcolor="white",
    
        legend=dict(
            orientation="h",
            x=0.5,
            xanchor="center",
            y=1.10,
            yanchor="bottom",
        ),
    
        bargap=0.25,
    )
    
    weight_fig.update_xaxes(
        title_text="Month",
    
        tickmode="array",
        tickvals=list(range(1, 13)),
    
        ticktext=[
            "Jan", "Feb", "Mar", "Apr",
            "May", "Jun", "Jul", "Aug",
            "Sep", "Oct", "Nov", "Dec",
        ],
    
        showgrid=False,
    )
    
    weight_fig.update_yaxes(
        title_text="ACT distribution (count)",
        gridcolor="#EDF1F4",
        zeroline=False,
    )

    return (
        sankey_fig,
        stock_fig,
        weight_fig
    )
