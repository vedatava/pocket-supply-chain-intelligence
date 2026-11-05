
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Pocket | Supply Chain Intelligence",
    page_icon="📦",
    layout="wide"
)

DATA = Path(__file__).parent / "data"

@st.cache_data
def load(name):
    return pd.read_csv(DATA / f"{name}.csv")

forecast = load("demand_forecast")
backtest = load("forecast_backtest")
planning = load("inventory_planning")
orders = load("purchase_orders")
scenarios = load("scenario_summary")
mitigation = load("risk_mitigation")
fba = load("fba_replenishment")
allocation = load("fba_allocation")
warehouse = load("warehouse_inventory")
fulfillment = load("fulfillment_performance")

st.title("Pocket | Supply Chain Intelligence")
st.caption(
    "Independent portfolio project | "
    "100% simulated data | Not affiliated with Pocket"
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Executive Overview",
        "Demand Forecast",
        "Inventory Planning",
        "Amazon FBA",
        "Fulfillment Operations"
    ]
)

sku_options = ["All"] + sorted(planning["sku"].unique())

selected_sku = st.sidebar.selectbox(
    "Product / Colorway", sku_options
)

def filter_sku(data):
    if selected_sku != "All" and "sku" in data.columns:
        return data[data["sku"] == selected_sku]
    return data

def table(data):
    st.dataframe(
        data,
        use_container_width=True,
        hide_index=True
    )

if page == "Executive Overview":
    st.header("Executive Supply Chain Overview")

    f = filter_sku(forecast)
    b = filter_sku(backtest)
    s = filter_sku(scenarios)

    ma = b[b["model"] == "4-Week Moving Average"]
    wape = (
        ma["absolute_error"].sum() /
        ma["actual"].sum() * 100
    )

    baseline = s[s["scenario"] == "Baseline"]
    spike = s[s["scenario"] == "30% Demand Spike"]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "12-Week Forecast",
        f"{f['forecast_units'].sum():,.0f}"
    )
    c2.metric("1-Week Backtest WAPE", f"{wape:.2f}%")
    c3.metric(
        "Baseline Unmet Units",
        f"{baseline['unmet_demand'].sum():,.0f}"
    )
    c4.metric(
        "Demand Spike Unmet Units",
        f"{spike['unmet_demand'].sum():,.0f}"
    )

    st.subheader("Projected Demand by Channel")
    chart_data = (
        f.groupby("channel", as_index=False)
        ["forecast_units"].sum()
    )
    st.plotly_chart(
        px.bar(
            chart_data,
            x="channel",
            y="forecast_units",
            color="channel"
        ),
        use_container_width=True
    )

    st.subheader("Supply Chain Risk Scenarios")
    table(s)

elif page == "Demand Forecast":
    st.header("12-Week Demand Forecast")

    f = filter_sku(forecast).copy()
    f["week"] = pd.to_datetime(f["week"])

    chart = (
        f.groupby(["week", "channel"], as_index=False)
        ["forecast_units"].sum()
    )

    st.plotly_chart(
        px.line(
            chart,
            x="week",
            y="forecast_units",
            color="channel",
            markers=True
        ),
        use_container_width=True
    )

    st.info(
        "Forecast uses a fixed 4-week moving-average "
        "baseline. Reported WAPE applies only to "
        "the historical one-week-ahead backtest."
    )

    st.subheader("Forecast Model Backtest")
    table(filter_sku(backtest))

elif page == "Inventory Planning":
    st.header("Inventory & Purchase Planning")

    p = filter_sku(planning)
    po = filter_sku(orders)
    m = filter_sku(mitigation)

    st.subheader("Inventory Coverage")
    st.plotly_chart(
        px.bar(
            p,
            x="sku",
            y="days_of_coverage",
            color="sku"
        ),
        use_container_width=True
    )

    st.subheader("Recommended Purchase Orders")
    table(po)

    st.subheader("Risk Mitigation")
    st.plotly_chart(
        px.bar(
            m,
            x="scenario",
            y="extra_units_required",
            color="sku",
            barmode="group"
        ),
        use_container_width=True
    )

elif page == "Amazon FBA":
    st.header("Amazon FBA Replenishment")

    st.subheader("FBA Inventory Health")
    table(filter_sku(fba))

    st.subheader("Warehouse Transfer Allocation")
    a = filter_sku(allocation)
    table(a)

    st.metric(
        "Estimated Transfer Cost",
        f"${a['estimated_transfer_cost'].sum():,.2f}"
    )

    st.subheader("Post-Transfer Inventory")
    table(filter_sku(warehouse))

elif page == "Fulfillment Operations":
    st.header("Fulfillment Cost & Performance")

    st.plotly_chart(
        px.bar(
            fulfillment,
            x="warehouse_id",
            y="cost_per_unit",
            color="warehouse_id",
            title="Shipping Cost Per Unit"
        ),
        use_container_width=True
    )

    st.subheader("3PL Performance Scorecard")
    table(fulfillment)

st.divider()
st.caption(
    "All products, warehouses, costs, forecasts, "
    "and recommendations are simulated. "
    "Results are illustrative, not Pocket company data."
)
