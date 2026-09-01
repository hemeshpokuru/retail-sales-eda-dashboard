import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# RETAIL SALES INTELLIGENCE DASHBOARD
# Streamlit App for the Retail Sales EDA Assignment
# =========================================================

st.set_page_config(
    page_title="Retail Sales Intelligence",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Design system
# -----------------------------
BG = "#0B1020"
PANEL = "#11182A"
PANEL_2 = "#151E32"
BORDER = "rgba(255,255,255,0.09)"
TEXT = "#F5F7FB"
MUTED = "#98A2B3"
BLUE = "#5B8DEF"
CYAN = "#45C4D9"
GREEN = "#43C59E"
GOLD = "#F4B942"
RED = "#F06C75"
PURPLE = "#9B8AFB"

st.markdown(
    f"""
<style>
:root {{
    --bg:{BG};
    --panel:{PANEL};
    --panel2:{PANEL_2};
    --border:{BORDER};
    --text:{TEXT};
    --muted:{MUTED};
    --blue:{BLUE};
    --cyan:{CYAN};
    --green:{GREEN};
    --gold:{GOLD};
    --red:{RED};
    --purple:{PURPLE};
}}

.stApp {{
    background:
        radial-gradient(circle at 85% 0%, rgba(91,141,239,.12), transparent 28%),
        radial-gradient(circle at 5% 15%, rgba(67,197,158,.07), transparent 24%),
        var(--bg);
    color: var(--text);
}}

.block-container {{
    max-width: 1500px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}}

[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #0D1425 0%, #0A0F1D 100%);
    border-right: 1px solid var(--border);
}}

[data-testid="stSidebar"] .block-container {{
    padding-top: 1.4rem;
}}

h1, h2, h3 {{
    letter-spacing: -0.02em;
}}

.hero {{
    background:
        linear-gradient(135deg, rgba(91,141,239,.16), rgba(67,197,158,.05)),
        rgba(17,24,42,.84);
    border: 1px solid var(--border);
    border-radius: 22px;
    padding: 28px 32px;
    margin-bottom: 18px;
    box-shadow: 0 18px 50px rgba(0,0,0,.20);
}}

.eyebrow {{
    color: var(--cyan);
    font-size: .76rem;
    font-weight: 800;
    letter-spacing: .14em;
    text-transform: uppercase;
    margin-bottom: 8px;
}}

.hero-title {{
    font-size: 2.35rem;
    line-height: 1.08;
    font-weight: 800;
    margin: 0;
    color: var(--text);
}}

.hero-sub {{
    color: var(--muted);
    margin-top: 10px;
    font-size: .98rem;
}}

.status-pill {{
    display:inline-block;
    padding: 6px 11px;
    border-radius: 999px;
    background: rgba(67,197,158,.12);
    border: 1px solid rgba(67,197,158,.25);
    color: #7DE1C2;
    font-size: .78rem;
    font-weight: 700;
}}

.kpi {{
    background: linear-gradient(145deg, rgba(21,30,50,.96), rgba(15,22,39,.96));
    border: 1px solid var(--border);
    border-radius: 17px;
    padding: 18px 18px 16px;
    min-height: 118px;
    box-shadow: 0 10px 28px rgba(0,0,0,.16);
}}

.kpi-label {{
    color: var(--muted);
    font-size: .78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: .08em;
}}

.kpi-value {{
    color: var(--text);
    font-size: 1.75rem;
    font-weight: 800;
    margin-top: 8px;
}}

.kpi-foot {{
    color: #7F8AA0;
    font-size: .74rem;
    margin-top: 4px;
}}

.section {{
    margin-top: 25px;
    margin-bottom: 10px;
}}

.section-kicker {{
    color: var(--blue);
    font-size: .73rem;
    text-transform: uppercase;
    letter-spacing: .12em;
    font-weight: 800;
}}

.section-title {{
    font-size: 1.25rem;
    font-weight: 800;
    margin-top: 3px;
}}

.insight {{
    background: linear-gradient(145deg, rgba(21,30,50,.95), rgba(17,24,42,.92));
    border: 1px solid var(--border);
    border-left: 4px solid var(--blue);
    border-radius: 14px;
    padding: 15px 17px;
    margin-bottom: 10px;
}}

.insight.warn {{ border-left-color: var(--red); }}
.insight.good {{ border-left-color: var(--green); }}
.insight.gold {{ border-left-color: var(--gold); }}

.insight-title {{
    font-weight: 800;
    color: var(--text);
    margin-bottom: 5px;
}}

.insight-text {{
    color: #B6BECC;
    font-size: .88rem;
    line-height: 1.5;
}}

.metric-card {{
    background: rgba(17,24,42,.82);
    border: 1px solid var(--border);
    border-radius: 15px;
    padding: 15px 16px;
}}

.metric-card .label {{
    color: var(--muted);
    font-size: .78rem;
}}

.metric-card .value {{
    color: var(--text);
    font-size: 1.2rem;
    font-weight: 800;
    margin-top: 4px;
}}

.small-note {{
    color: var(--muted);
    font-size: .78rem;
}}

[data-testid="stTabs"] button {{
    font-weight: 700;
}}

[data-testid="stDataFrame"] {{
    border: 1px solid var(--border);
    border-radius: 12px;
}}

.stDownloadButton button {{
    border-radius: 10px;
}}

[data-testid="stSidebar"] [data-testid="stMultiSelect"] div[data-baseweb="select"] {{
    min-height: 42px;
}}

[data-testid="stSidebar"] [data-testid="stMultiSelect"] input::placeholder {{
    color: #7F8AA0 !important;
}}

[data-testid="stSidebar"] .stButton > button {{
    border: 1px solid rgba(91,141,239,.30);
    background: rgba(91,141,239,.08);
    color: #DCE6FF;
    font-weight: 700;
    border-radius: 10px;
}}

footer {{
    visibility: hidden;
}}
</style>
""",
    unsafe_allow_html=True,
)


# -----------------------------
# Helpers
# -----------------------------
def money(v):
    v = float(v)
    sign = "-" if v < 0 else ""
    v = abs(v)
    if v >= 1_000_000:
        return f"{sign}${v/1_000_000:.2f}M"
    if v >= 1_000:
        return f"{sign}${v/1_000:.1f}K"
    return f"{sign}${v:,.0f}"


def pct(v):
    return f"{float(v):.1f}%"


def fig_style(fig, height=360):
    fig.update_layout(
        height=height,
        margin=dict(l=8, r=8, t=30, b=8),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT, size=12),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11),
        ),
        hoverlabel=dict(
            bgcolor=PANEL_2,
            bordercolor=BORDER,
            font=dict(color=TEXT),
        ),
    )
    fig.update_xaxes(
        gridcolor="rgba(255,255,255,.07)",
        zerolinecolor="rgba(255,255,255,.10)",
        linecolor="rgba(255,255,255,.08)",
    )
    fig.update_yaxes(
        gridcolor="rgba(255,255,255,.07)",
        zerolinecolor="rgba(255,255,255,.10)",
        linecolor="rgba(255,255,255,.08)",
    )
    return fig


@st.cache_data
def load_data():
    raw = pd.read_csv("superstore.csv")

    required = [
        "Order Date", "Ship Date", "Ship Mode", "Customer ID",
        "Customer Name", "Segment", "Country", "City", "State",
        "Region", "Product ID", "Category", "Sub-Category",
        "Product Name", "Sales", "Quantity", "Discount", "Profit",
    ]

    # -----------------------------
    # Data cleaning & consistency
    # -----------------------------
    # Remove exact duplicate rows first.
    duplicate_rows = raw.duplicated().sum()

    df = raw.drop_duplicates().copy()

    # Normalize text fields to remove accidental leading/trailing spaces.
    text_cols = df.select_dtypes(include=["object"]).columns
    for col in text_cols:
        df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)

    # Convert numeric fields safely; invalid values become NaN and are handled below.
    numeric_cols = ["Sales", "Quantity", "Discount", "Profit"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Convert dates safely.
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df["Ship Date"] = pd.to_datetime(df["Ship Date"], errors="coerce")

    # Required business fields.
    df = df.dropna(subset=required).copy()

    # Date consistency: shipment cannot occur before order.
    invalid_date_order = df["Ship Date"] < df["Order Date"]
    invalid_date_count = int(invalid_date_order.sum())
    df = df.loc[~invalid_date_order].copy()

    # Business consistency: sales quantity should be positive.
    invalid_quantity = df["Quantity"] <= 0
    invalid_quantity_count = int(invalid_quantity.sum())
    df = df.loc[~invalid_quantity].copy()

    df["Year"] = df["Order Date"].dt.year.astype(int)
    df["Month"] = df["Order Date"].dt.month.astype(int)
    df["Month Name"] = df["Order Date"].dt.strftime("%b")
    df["Order Month"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()
    df["Delivery Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
    df["Profit Margin"] = np.where(
        df["Sales"] != 0, df["Profit"] / df["Sales"] * 100, np.nan
    )
    return raw, df


raw_df, df = load_data()

# Data-quality audit values used throughout the dashboard.
raw_duplicate_count = int(raw_df.duplicated().sum())
clean_duplicate_count = int(df.duplicated().sum())
raw_missing_cells = int(raw_df.isna().sum().sum())
clean_missing_cells = int(df.isna().sum().sum())


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.markdown("## Retail Intelligence")
st.sidebar.caption("Interactive business performance dashboard")

# Empty multiselect = ALL values.
# This keeps the sidebar clean instead of displaying hundreds of selected cities.
def optional_filter(series, selected_values):
    if selected_values:
        return series.isin(selected_values)
    return pd.Series(True, index=series.index)


def clear_all_filters():
    for key in [
        "filter_years",
        "filter_categories",
        "filter_segments",
        "filter_regions",
        "filter_cities",
        "filter_ship_modes",
    ]:
        st.session_state[key] = []


with st.sidebar.expander("FILTERS", expanded=True):
    years = sorted(df["Year"].unique())
    selected_years = st.multiselect(
        "Year",
        years,
        default=[],
        key="filter_years",
        placeholder="All years",
        help="Leave empty to include all years.",
    )

    categories = sorted(df["Category"].unique())
    selected_categories = st.multiselect(
        "Category",
        categories,
        default=[],
        key="filter_categories",
        placeholder="All categories",
        help="Leave empty to include all categories.",
    )

    segments = sorted(df["Segment"].unique())
    selected_segments = st.multiselect(
        "Customer Segment",
        segments,
        default=[],
        key="filter_segments",
        placeholder="All customer segments",
        help="Leave empty to include all customer segments.",
    )

    regions = sorted(df["Region"].unique())
    selected_regions = st.multiselect(
        "Region",
        regions,
        default=[],
        key="filter_regions",
        placeholder="All regions",
        help="Leave empty to include all regions.",
    )

    cities = sorted(df["City"].unique())
    selected_cities = st.multiselect(
        "City",
        cities,
        default=[],
        key="filter_cities",
        placeholder="All cities",
        help="Leave empty to include all cities.",
    )

    min_date = df["Order Date"].min().date()
    max_date = df["Order Date"].max().date()
    selected_dates = st.date_input(
        "Order date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        help="The full range is selected by default.",
    )

    ship_modes = sorted(df["Ship Mode"].unique())
    selected_ship_modes = st.multiselect(
        "Ship Mode",
        ship_modes,
        default=[],
        key="filter_ship_modes",
        placeholder="All ship modes",
        help="Leave empty to include all ship modes.",
    )

    if st.sidebar.button(
        "↺  Clear all filters",
        use_container_width=True,
        help="Return every categorical filter to All.",
    ):
        clear_all_filters()
        st.rerun()

with st.sidebar.expander("QUICK CONTROLS", expanded=True):
    top_n = st.slider("Top N ranking", 5, 15, 10)
    show_outliers = st.checkbox("Show outlier markers", True)

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
else:
    start_date = selected_dates
    end_date = selected_dates

filtered = df[
    optional_filter(df["Year"], selected_years)
    & optional_filter(df["Category"], selected_categories)
    & optional_filter(df["Segment"], selected_segments)
    & optional_filter(df["Region"], selected_regions)
    & optional_filter(df["City"], selected_cities)
    & optional_filter(df["Ship Mode"], selected_ship_modes)
    & (df["Order Date"].dt.date >= start_date)
    & (df["Order Date"].dt.date <= end_date)
].copy()

if filtered.empty:
    st.error("No records match the selected filters. Please broaden the filters.")
    st.stop()


# -----------------------------
# Header
# -----------------------------
active_filter_count = sum([
    bool(selected_years),
    bool(selected_categories),
    bool(selected_segments),
    bool(selected_regions),
    bool(selected_cities),
    bool(selected_ship_modes),
])

filter_summary = (
    f"{active_filter_count} categorical filter(s) active"
    if active_filter_count
    else "All categories, cities, years, regions, segments & ship modes"
)

date_min = filtered["Order Date"].min().strftime("%b %Y")
date_max = filtered["Order Date"].max().strftime("%b %Y")

st.markdown(
    f"""
<div class="hero">
    <div class="eyebrow">RETAIL SALES INTELLIGENCE • EDA</div>
    <div class="hero-title">Performance command center</div>
    <div class="hero-sub">
        Executive view of sales, profitability, customers, products, geography and operational performance.
        <span class="status-pill">● LIVE FILTERED VIEW</span>
    </div>
    <div class="hero-sub">
        Period: <b>{date_min} – {date_max}</b> &nbsp;•&nbsp;
        {len(filtered):,} transaction rows &nbsp;•&nbsp;
        {filtered["City"].nunique():,} cities &nbsp;•&nbsp;
        {filtered["State"].nunique():,} states
    </div>
    <div class="hero-sub">
        Filter status: <b>{filter_summary}</b>
    </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# -----------------------------
# KPI calculations
# -----------------------------
total_sales = filtered["Sales"].sum()
total_profit = filtered["Profit"].sum()
orders = filtered["Order ID"].nunique()
customers = filtered["Customer ID"].nunique()
products = filtered["Product ID"].nunique()
cities = filtered["City"].nunique()
margin = total_profit / total_sales * 100 if total_sales else 0
aov = total_sales / orders if orders else 0

kpi_data = [
    ("TOTAL SALES", money(total_sales), "Revenue generated"),
    ("TOTAL PROFIT", money(total_profit), "Net profit"),
    ("PROFIT MARGIN", pct(margin), "Profit / Sales"),
    ("ORDERS", f"{orders:,}", "Unique orders"),
    ("CUSTOMERS", f"{customers:,}", "Unique customers"),
    ("AVG ORDER VALUE", money(aov), "Sales / order"),
]

cols = st.columns(6)
for col, (label, value, foot) in zip(cols, kpi_data):
    col.markdown(
        f"""
<div class="kpi">
    <div class="kpi-label">{label}</div>
    <div class="kpi-value">{value}</div>
    <div class="kpi-foot">{foot}</div>
</div>
""",
        unsafe_allow_html=True,
    )


# -----------------------------
# Tabs
# -----------------------------
tabs = st.tabs([
    "Executive Overview",
    "Products & Categories",
    "Customers & Cities",
    "Operations",
    "Insights & Statistics",
])


# =========================================================
# TAB 1 — EXECUTIVE OVERVIEW
# =========================================================
with tabs[0]:
    st.markdown(
        '<div class="section"><div class="section-kicker">01 • Trend</div>'
        '<div class="section-title">Sales & profit trajectory</div></div>',
        unsafe_allow_html=True,
    )

    trend = (
        filtered.groupby("Order Month")[["Sales", "Profit"]]
        .sum()
        .reset_index()
        .sort_values("Order Month")
    )

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=trend["Order Month"],
        y=trend["Sales"],
        name="Sales",
        mode="lines+markers",
        line=dict(color=BLUE, width=3),
        marker=dict(size=6),
        fill="tozeroy",
        fillcolor="rgba(91,141,239,.10)",
        hovertemplate="%{x|%b %Y}<br>Sales: $%{y:,.0f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=trend["Order Month"],
        y=trend["Profit"],
        name="Profit",
        mode="lines+markers",
        line=dict(color=GREEN, width=2),
        marker=dict(size=5),
        hovertemplate="%{x|%b %Y}<br>Profit: $%{y:,.0f}<extra></extra>",
    ))
    st.plotly_chart(fig_style(fig, 430), use_container_width=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown(
            '<div class="section"><div class="section-kicker">Mix</div>'
            '<div class="section-title">Category performance</div></div>',
            unsafe_allow_html=True,
        )

        cat = (
            filtered.groupby("Category")
            .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
            .reset_index()
        )
        cat["Margin"] = cat["Profit"] / cat["Sales"] * 100

        fig_cat = px.bar(
            cat.sort_values("Sales"),
            x="Sales",
            y="Category",
            orientation="h",
            color="Category",
            color_discrete_sequence=[BLUE, CYAN, PURPLE],
            text_auto=".3s",
        )
        fig_cat.update_layout(showlegend=False)
        st.plotly_chart(fig_style(fig_cat, 330), use_container_width=True)

    with c2:
        st.markdown(
            '<div class="section"><div class="section-kicker">Geography</div>'
            '<div class="section-title">Regional sales contribution</div></div>',
            unsafe_allow_html=True,
        )

        region = (
            filtered.groupby("Region")["Sales"]
            .sum()
            .reset_index()
            .sort_values("Sales")
        )

        fig_region = px.bar(
            region,
            x="Sales",
            y="Region",
            orientation="h",
            color="Sales",
            color_continuous_scale=["#1B315C", BLUE, CYAN],
            text_auto=".3s",
        )
        fig_region.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_style(fig_region, 330), use_container_width=True)

    # Monthly seasonality
    st.markdown(
        '<div class="section"><div class="section-kicker">Seasonality</div>'
        '<div class="section-title">Average sales by calendar month</div></div>',
        unsafe_allow_html=True,
    )

    season = (
        filtered.groupby("Month")["Sales"]
        .mean()
        .reindex(range(1, 13))
        .reset_index()
    )
    season["Month Name"] = pd.to_datetime(
        season["Month"], format="%m"
    ).dt.strftime("%b")

    fig_season = px.bar(
        season,
        x="Month Name",
        y="Sales",
        text_auto=".3s",
        color="Sales",
        color_continuous_scale=["#1B315C", BLUE, GOLD],
    )
    fig_season.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_style(fig_season, 330), use_container_width=True)


# =========================================================
# TAB 2 — PRODUCTS & CATEGORIES
# =========================================================
with tabs[1]:
    st.markdown(
        '<div class="section"><div class="section-kicker">02 • Product intelligence</div>'
        '<div class="section-title">What drives revenue and profit?</div></div>',
        unsafe_allow_html=True,
    )

    p1, p2 = st.columns(2)

    top_products = (
        filtered.groupby("Product Name")
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        .sort_values("Sales", ascending=False)
        .head(top_n)
        .reset_index()
    )

    with p1:
        fig_top = px.bar(
            top_products.sort_values("Sales"),
            x="Sales",
            y="Product Name",
            orientation="h",
            text_auto=".3s",
            color="Sales",
            color_continuous_scale=["#1B315C", BLUE, CYAN],
        )
        fig_top.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_style(fig_top, 470), use_container_width=True)

    with p2:
        sub = (
            filtered.groupby("Sub-Category")
            .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
            .reset_index()
            .sort_values("Profit")
        )
        fig_sub = px.bar(
            sub,
            x="Profit",
            y="Sub-Category",
            orientation="h",
            color="Profit",
            color_continuous_scale=[RED, "#596579", GREEN],
            text_auto=".3s",
        )
        fig_sub.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_style(fig_sub, 470), use_container_width=True)

    st.markdown(
        '<div class="section"><div class="section-kicker">Profitability matrix</div>'
        '<div class="section-title">Discount vs profit by transaction</div></div>',
        unsafe_allow_html=True,
    )

    sample = filtered.sample(min(1800, len(filtered)), random_state=42)
    fig_scatter = px.scatter(
        sample,
        x="Discount",
        y="Profit",
        size="Sales",
        color="Category",
        hover_data=["Product Name", "City", "Sales", "Profit"],
        color_discrete_sequence=[BLUE, CYAN, PURPLE],
        opacity=.65,
    )
    fig_scatter.add_hline(y=0, line_dash="dot", line_color=RED)
    st.plotly_chart(fig_style(fig_scatter, 430), use_container_width=True)

    st.markdown(
        '<div class="section"><div class="section-kicker">Required EDA</div>'
        '<div class="section-title">Sales distribution across categories</div></div>',
        unsafe_allow_html=True,
    )

    fig_box = px.box(
        filtered,
        x="Category",
        y="Sales",
        color="Category",
        points="outliers" if show_outliers else False,
        color_discrete_sequence=[BLUE, CYAN, PURPLE],
        hover_data=["Sub-Category"],
    )
    st.plotly_chart(fig_style(fig_box, 440), use_container_width=True)

    # Category profitability table
    cat_detail = (
        filtered.groupby("Category")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Avg_Discount=("Discount", "mean"),
            Transactions=("Order ID", "count"),
        )
        .reset_index()
    )
    cat_detail["Profit Margin"] = cat_detail["Profit"] / cat_detail["Sales"] * 100
    cat_detail = cat_detail.sort_values("Sales", ascending=False)

    st.dataframe(
        cat_detail.style.format({
            "Sales": "${:,.2f}",
            "Profit": "${:,.2f}",
            "Avg_Discount": "{:.1%}",
            "Profit Margin": "{:.2f}%",
            "Transactions": "{:,.0f}",
        }),
        use_container_width=True,
        hide_index=True,
    )


# =========================================================
# TAB 3 — CUSTOMERS & CITIES
# =========================================================
with tabs[2]:
    st.markdown(
        '<div class="section"><div class="section-kicker">03 • Customer & geography</div>'
        '<div class="section-title">Where is the business coming from?</div></div>',
        unsafe_allow_html=True,
    )

    city_perf = (
        filtered.groupby("City")
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Customers=("Customer ID", "nunique"),
            Orders=("Order ID", "nunique"),
        )
        .reset_index()
    )
    city_perf["Margin"] = np.where(
        city_perf["Sales"] != 0,
        city_perf["Profit"] / city_perf["Sales"] * 100,
        np.nan,
    )

    c1, c2 = st.columns(2)

    with c1:
        top_cities = city_perf.nlargest(top_n, "Sales").sort_values("Sales")
        fig_city = px.bar(
            top_cities,
            x="Sales",
            y="City",
            orientation="h",
            text_auto=".3s",
            color="Sales",
            color_continuous_scale=["#1B315C", BLUE, CYAN],
        )
        fig_city.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_style(fig_city, 450), use_container_width=True)

    with c2:
        top_profit_cities = city_perf.nlargest(top_n, "Profit").sort_values("Profit")
        fig_city_profit = px.bar(
            top_profit_cities,
            x="Profit",
            y="City",
            orientation="h",
            text_auto=".3s",
            color="Profit",
            color_continuous_scale=["#3A2026", RED, GREEN],
        )
        fig_city_profit.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_style(fig_city_profit, 450), use_container_width=True)

    # Customer probability
    st.markdown(
        '<div class="section"><div class="section-kicker">Probability analysis</div>'
        '<div class="section-title">Probability of selecting a customer from each city</div></div>',
        unsafe_allow_html=True,
    )

    # Customer-level probability:
    # P(city) = distinct customers associated with the city / total distinct customers.
    customer_city_all = (
        filtered[["Customer ID", "City"]]
        .drop_duplicates()
        .groupby("City")["Customer ID"]
        .nunique()
        .reset_index(name="Customer Count")
    )
    total_unique_customers = filtered["Customer ID"].nunique()
    customer_city_all["Probability (%)"] = (
        customer_city_all["Customer Count"] / total_unique_customers * 100
        if total_unique_customers else 0
    )
    customer_city_all = customer_city_all.sort_values(
        "Customer Count", ascending=False
    )

    customer_city = customer_city_all.head(15).copy()

    fig_prob = px.bar(
        customer_city.sort_values("Probability (%)"),
        x="Probability (%)",
        y="City",
        orientation="h",
        text="Probability (%)",
        color="Probability (%)",
        color_continuous_scale=["#1B315C", BLUE, CYAN],
    )
    fig_prob.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside",
    )
    fig_prob.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_style(fig_prob, 460), use_container_width=True)

    st.caption(
        "Probability is based on distinct customers associated with each city. "
        "The table below contains every city in the current filtered view."
    )
    st.dataframe(
        customer_city_all.style.format({
            "Customer Count": "{:,.0f}",
            "Probability (%)": "{:.2f}%",
        }),
        use_container_width=True,
        hide_index=True,
    )

    # City statistical comparison
    st.markdown(
        '<div class="section"><div class="section-kicker">Statistical comparison</div>'
        '<div class="section-title">Top two cities — mean, median & standard deviation</div></div>',
        unsafe_allow_html=True,
    )

    top_two = (
        filtered.groupby("City")["Sales"]
        .sum()
        .nlargest(2)
        .index.tolist()
    )

    if len(top_two) == 2:
        stat_rows = []
        for city in top_two:
            vals = filtered.loc[filtered["City"] == city, "Sales"]
            stat_rows.append({
                "City": city,
                "Mean Sales": vals.mean(),
                "Median Sales": vals.median(),
                "Std Deviation": vals.std(),
                "Skewness": vals.skew(),
            })
        stat_df = pd.DataFrame(stat_rows)

        st.dataframe(
            stat_df.style.format({
                "Mean Sales": "${:,.2f}",
                "Median Sales": "${:,.2f}",
                "Std Deviation": "${:,.2f}",
                "Skewness": "{:.2f}",
            }),
            use_container_width=True,
            hide_index=True,
        )

    # Customer concentration
    top_customer = (
        filtered.groupby("Customer Name")["Sales"]
        .sum()
        .nlargest(top_n)
        .reset_index()
    )
    fig_customer = px.bar(
        top_customer.sort_values("Sales"),
        x="Sales",
        y="Customer Name",
        orientation="h",
        text_auto=".3s",
        color="Sales",
        color_continuous_scale=["#1B315C", BLUE, CYAN],
    )
    fig_customer.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_style(fig_customer, 430), use_container_width=True)


# =========================================================
# TAB 4 — OPERATIONS
# =========================================================
with tabs[3]:
    st.markdown(
        '<div class="section"><div class="section-kicker">04 • Operations</div>'
        '<div class="section-title">Fulfillment performance</div></div>',
        unsafe_allow_html=True,
    )

    op1, op2 = st.columns(2)

    ship = (
        filtered.groupby("Ship Mode")
        .agg(
            Orders=("Order ID", "nunique"),
            Sales=("Sales", "sum"),
            Avg_Delivery_Days=("Delivery Days", "mean"),
        )
        .reset_index()
    )

    with op1:
        fig_ship = px.bar(
            ship.sort_values("Orders"),
            x="Orders",
            y="Ship Mode",
            orientation="h",
            text_auto=".3s",
            color="Orders",
            color_continuous_scale=["#1B315C", BLUE, CYAN],
        )
        fig_ship.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_style(fig_ship, 350), use_container_width=True)

    with op2:
        fig_delivery = px.bar(
            ship.sort_values("Avg_Delivery_Days"),
            x="Avg_Delivery_Days",
            y="Ship Mode",
            orientation="h",
            text_auto=".2f",
            color="Avg_Delivery_Days",
            color_continuous_scale=["#173B3B", GREEN, GOLD],
        )
        fig_delivery.update_layout(
            coloraxis_showscale=False,
            xaxis_title="Average delivery days",
        )
        st.plotly_chart(fig_style(fig_delivery, 350), use_container_width=True)

    # State performance
    state = (
        filtered.groupby("State")
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        .reset_index()
    )
    state["Margin"] = np.where(
        state["Sales"] != 0,
        state["Profit"] / state["Sales"] * 100,
        np.nan,
    )

    c1, c2 = st.columns(2)
    with c1:
        top_states = state.nlargest(15, "Sales").sort_values("Sales")
        fig_states = px.bar(
            top_states,
            x="Sales",
            y="State",
            orientation="h",
            text_auto=".3s",
            color="Sales",
            color_continuous_scale=["#1B315C", BLUE, CYAN],
        )
        fig_states.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_style(fig_states, 470), use_container_width=True)

    with c2:
        risky_states = state.nsmallest(15, "Profit").sort_values("Profit")
        fig_risk = px.bar(
            risky_states,
            x="Profit",
            y="State",
            orientation="h",
            text_auto=".3s",
            color="Profit",
            color_continuous_scale=[RED, "#596579", GREEN],
        )
        fig_risk.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_style(fig_risk, 470), use_container_width=True)

    st.markdown(
        '<div class="section"><div class="section-kicker">Data explorer</div>'
        '<div class="section-title">Filtered transactions</div></div>',
        unsafe_allow_html=True,
    )

    st.download_button(
        "⬇ Download filtered CSV",
        filtered.to_csv(index=False).encode("utf-8"),
        "retail_sales_filtered.csv",
        "text/csv",
    )

    st.dataframe(filtered, use_container_width=True, hide_index=True)


# =========================================================
# TAB 5 — INSIGHTS & STATISTICS
# =========================================================
with tabs[4]:

    # Outlier calculation
    q1 = filtered["Sales"].quantile(.25)
    q3 = filtered["Sales"].quantile(.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    outlier_mask = (filtered["Sales"] < lower) | (filtered["Sales"] > upper)
    outliers = filtered[outlier_mask].copy()

    outlier_count = len(outliers)
    outlier_pct = outlier_count / len(filtered) * 100
    outlier_sales_pct = (
        outliers["Sales"].sum() / filtered["Sales"].sum() * 100
        if total_sales else 0
    )
    outlier_profit_pct = (
        outliers["Profit"].sum() / filtered["Profit"].sum() * 100
        if total_profit else 0
    )

    # Core stats cards
    stats = [
        ("Sales skewness", filtered["Sales"].skew(), "Strong positive skew" if filtered["Sales"].skew() > 0 else "Negative skew"),
        ("Q1", money(q1), "25th percentile"),
        ("Q3", money(q3), "75th percentile"),
        ("IQR", money(iqr), "Q3 − Q1"),
        ("Outlier transactions", f"{outlier_count:,}", f"{outlier_pct:.1f}% of rows"),
        ("Upper bound", money(upper), "1.5 × IQR rule"),
    ]

    cols = st.columns(6)
    for col, (label, value, foot) in zip(cols, stats):
        col.markdown(
            f"""
<div class="metric-card">
    <div class="label">{label}</div>
    <div class="value">{value}</div>
    <div class="small-note">{foot}</div>
</div>
""",
            unsafe_allow_html=True,
        )

    # Five+ insights generated from current filters
    best_cat = (
        filtered.groupby("Category")["Sales"].sum().idxmax()
        if not filtered.empty else "-"
    )
    best_cat_sales = (
        filtered.groupby("Category")["Sales"].sum().max()
        if not filtered.empty else 0
    )

    best_profit_cat = (
        filtered.groupby("Category")["Profit"].sum().idxmax()
        if not filtered.empty else "-"
    )
    worst_profit_sub = (
        filtered.groupby("Sub-Category")["Profit"].sum().idxmin()
        if not filtered.empty else "-"
    )
    worst_profit_value = (
        filtered.groupby("Sub-Category")["Profit"].sum().min()
        if not filtered.empty else 0
    )

    best_city = (
        filtered.groupby("City")["Sales"].sum().idxmax()
        if not filtered.empty else "-"
    )
    best_city_sales = (
        filtered.groupby("City")["Sales"].sum().max()
        if not filtered.empty else 0
    )

    best_month_row = (
        filtered.groupby("Order Month")["Sales"].sum().idxmax()
        if not filtered.empty else None
    )
    best_month_sales = (
        filtered.groupby("Order Month")["Sales"].sum().max()
        if not filtered.empty else 0
    )

    avg_delivery = filtered["Delivery Days"].mean()
    sales_skew = filtered["Sales"].skew()
    skew_direction = (
        "positively skewed (right-skewed)"
        if sales_skew > 0
        else "negatively skewed (left-skewed)"
        if sales_skew < 0
        else "approximately symmetric"
    )

    insights = [
        (
            "Revenue leader",
            f"{best_cat} is the strongest revenue category with {money(best_cat_sales)} in sales.",
            "good",
        ),
        (
            "Profit leader",
            f"{best_profit_cat} generates the highest total profit among the categories in the selected view.",
            "good",
        ),
        (
            "Geographic leader",
            f"{best_city} is the top sales city with {money(best_city_sales)} in revenue.",
            "gold",
        ),
        (
            "Profitability risk",
            f"{worst_profit_sub} is the weakest sub-category by profit at {money(worst_profit_value)}. "
            "Pricing, discounting, product mix and fulfillment economics should be reviewed.",
            "warn",
        ),
        (
            "Seasonal peak",
            f"{best_month_row.strftime('%B %Y') if best_month_row is not None else '-'} is the highest-sales month "
            f"with {money(best_month_sales)} in revenue.",
            "gold",
        ),
        (
            "Outlier concentration",
            f"{outlier_count:,} transactions ({outlier_pct:.1f}%) are sales outliers under the 1.5×IQR rule. "
            f"They contribute {outlier_sales_pct:.1f}% of sales.",
            "warn" if outlier_pct > 10 else "good",
        ),
        (
            "Operational benchmark",
            f"Average delivery time is {avg_delivery:.2f} days across the filtered transactions.",
            "good",
        ),
        (
            "Distribution shape",
            f"Sales skewness is {sales_skew:.2f}, indicating that sales are {skew_direction}.",
            "gold",
        ),
    ]

    left, right = st.columns(2)
    for i, item in enumerate(insights):
        target = left if i % 2 == 0 else right
        with target:
            title, text, cls = item
            st.markdown(
                f"""
<div class="insight {cls}">
    <div class="insight-title">{title}</div>
    <div class="insight-text">{text}</div>
</div>
""",
                unsafe_allow_html=True,
            )

    # Outlier table
    st.markdown(
        '<div class="section"><div class="section-kicker">Outlier investigation</div>'
        '<div class="section-title">Largest sales outliers</div></div>',
        unsafe_allow_html=True,
    )

    if not outliers.empty:
        outlier_cols = [
            "Order ID", "City", "Category", "Sub-Category",
            "Product Name", "Sales", "Discount", "Profit"
        ]
        outlier_view = (
            outliers[outlier_cols]
            .sort_values("Sales", ascending=False)
            .head(15)
        )
        st.dataframe(
            outlier_view.style.format({
                "Sales": "${:,.2f}",
                "Discount": "{:.0%}",
                "Profit": "${:,.2f}",
            }),
            use_container_width=True,
            hide_index=True,
        )

    # Recommendations
    st.markdown(
        '<div class="section"><div class="section-kicker">Management actions</div>'
        '<div class="section-title">Recommended actions</div></div>',
        unsafe_allow_html=True,
    )

    recommendations = [
        ("Protect high-margin categories", "Prioritize inventory, campaigns and cross-sell opportunities around the strongest profit-generating categories and sub-categories."),
        ("Review loss-making products", f"Investigate {worst_profit_sub} for excessive discounts, pricing gaps, returns, freight costs or unfavorable product mix."),
        ("Replicate city success", f"Study the customer mix and product mix in {best_city} and apply successful tactics to lower-performing cities."),
        ("Plan for seasonal peaks", "Use the monthly trend to increase inventory and marketing capacity ahead of recurring high-demand periods."),
        ("Audit high-value outliers", "Large transactions can materially influence total revenue and profit, so review them individually for strategic accounts and unusual discounts."),
    ]

    for title, text in recommendations:
        st.markdown(
            f"""
<div class="insight">
    <div class="insight-title">→ {title}</div>
    <div class="insight-text">{text}</div>
</div>
""",
            unsafe_allow_html=True,
        )


# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.caption(
    f"Retail Sales Intelligence • Cleaned records: {len(df):,} • "
    f"Original records: {len(raw_df):,} • Exact duplicates removed: {raw_duplicate_count:,} • "
    "Dashboard built with Streamlit + Pandas + Plotly"
)
