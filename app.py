"""Pocket Supply Chain Intelligence — independent synthetic-data portfolio demo."""
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Pocket | Supply Chain Intelligence", page_icon="📦", layout="wide", initial_sidebar_state="expanded")
ROOT = Path(__file__).parent / "data"

st.markdown("""<style>
.block-container{max-width:1450px;padding-top:1.6rem;padding-bottom:3rem}
[data-testid="stAppViewContainer"]{background:#f6f8fc;color:#17243a}
[data-testid="stSidebar"]{background:#ffffff;border-right:1px solid #e5eaf2}
h1,h2,h3{letter-spacing:-.035em;color:#17243a}
h1{font-size:2.1rem !important}
[data-testid="stMetric"]{background:white;border:1px solid #e5eaf2;padding:18px 19px;border-radius:15px;box-shadow:0 4px 15px #17243a08}
[data-testid="stMetricLabel"]{color:#58677d}
[data-testid="stMetricValue"]{font-size:1.75rem}
div[data-testid="stAlert"]{border-radius:12px}
.note{padding:13px 16px;border:1px solid #dbe4f1;border-radius:12px;background:#edf3ff;font-size:.91rem;color:#344762;margin:.8rem 0}
.brand{font-size:1.05rem;font-weight:750;letter-spacing:-.035em;color:#182a4f}
.kicker{color:#526683;font-size:.9rem;margin-bottom:1rem}
</style>""", unsafe_allow_html=True)

@st.cache_data
def get_data(filename):
    path = ROOT / (filename + ".csv")
    if not path.exists():
        st.error(f"Missing file: data/{filename}.csv. Keep all CSV datasets inside the data/ folder in GitHub.")
        st.stop()
    return pd.read_csv(path)

forecast = get_data("demand_forecast")
backtest = get_data("forecast_backtest")
planning = get_data("inventory_planning")
orders = get_data("purchase_orders")
scenarios = get_data("scenario_summary")
mitigation = get_data("risk_mitigation")
fba = get_data("fba_replenishment")
allocation = get_data("fba_allocation")
warehouse = get_data("warehouse_inventory")
fulfillment = get_data("fulfillment_performance")
projection = get_data("inventory_projection")
scenario_daily = get_data("scenario_daily")

forecast['week'] = pd.to_datetime(forecast['week'], errors='coerce')
for date_col in ['recommended_order_date','recommended_arrival_date','first_safety_breach']:
    if date_col in orders: orders[date_col] = pd.to_datetime(orders[date_col], errors='coerce')
if 'date' in projection: projection['date'] = pd.to_datetime(projection['date'], errors='coerce')
if 'date' in scenario_daily: scenario_daily['date'] = pd.to_datetime(scenario_daily['date'], errors='coerce')

# Reference period is a historical hypothetical snapshot; not current live operational data.
SNAPSHOT = "2026-11-05"
BLUE = "#3a69e6"
ORANGE = "#f39b47"
RED = "#d94862"
GREEN = "#16856a"
PALETTE = [BLUE, "#62a9ed", ORANGE, RED, GREEN]

st.sidebar.markdown('<div class="brand">◈ POCKET / OPS LAB</div>', unsafe_allow_html=True)
st.sidebar.caption("Independent analytical prototype")
page = st.sidebar.radio("WORKSPACE", ["Executive Overview", "Demand Forecast", "Inventory & Purchase Orders", "Amazon FBA & Warehouses", "Fulfillment & Costs", "Methodology & Limitations"])
sku_options = ["All products"] + sorted(planning['sku'].dropna().unique().tolist())
selected_sku = st.sidebar.selectbox("Product / colorway", sku_options)
st.sidebar.markdown("---")
st.sidebar.caption("SIMULATED DATA · Not affiliated with Pocket")
st.sidebar.caption(f"Inventory planning snapshot: {SNAPSHOT}")

def filtered(data):
    if selected_sku != "All products" and 'sku' in data.columns:
        return data[data['sku'] == selected_sku].copy()
    return data.copy()

def fmtint(x): return f"{x:,.0f}"
def fmtmoney(x): return f"${x:,.0f}"
def chart(fig):
    fig.update_layout(template="plotly_white", font=dict(color="#26364f"), margin=dict(l=15,r=15,t=55,b=18), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", legend_title_text="")
    st.plotly_chart(fig, use_container_width=True)

def table(data):
    st.dataframe(data, hide_index=True, use_container_width=True)

f = filtered(forecast)
b = filtered(backtest)
p = filtered(planning)
o = filtered(orders)
s = filtered(scenarios)
m = filtered(mitigation)
a = filtered(allocation)
w = filtered(warehouse)
fb = filtered(fba)

ma = b[b['model'] == '4-Week Moving Average'] if 'model' in b else pd.DataFrame()
wape = (100*ma['absolute_error'].sum()/ma['actual'].sum()) if len(ma) and ma['actual'].sum() else None
spike = s[s['scenario'] == '30% Demand Spike']
baseline = s[s['scenario'] == 'Baseline']
delay = s[s['scenario'] == '7-Day Supplier Delay']

st.title("Pocket | Supply Chain Intelligence")
st.markdown('<div class="kicker">Executive decision support · Demand → Replenishment → Warehouse placement → Fulfillment</div>', unsafe_allow_html=True)
st.markdown('<div class="note">🧪 <b>Independent portfolio case study.</b> All device counts, warehouse locations, pricing and scenarios are simulated. These are not Pocket\'s actual operations or financials. Forecast WAPE is from a <b>one-week-ahead</b> backtest, not the 12-week forecast.</div>', unsafe_allow_html=True)

if page == "Executive Overview":
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("12-week baseline demand", fmtint(f['forecast_units'].sum()), help="4-week moving-average extrapolation, not validated 12-week accuracy")
    c2.metric("1-week backtest WAPE", f"{wape:.2f}%" if wape is not None else "N/A", help="Rolling one-week-ahead test on synthetic data. Lower is better.")
    c3.metric("Baseline unmet demand", fmtint(baseline['unmet_demand'].sum()))
    c4.metric("30% spike: unmet units", fmtint(spike['unmet_demand'].sum()), help="60-day stress test with proposed baseline purchase orders")

    st.subheader("Decision brief")
    st.error(f"🔴 **Demand spike exposure:** {fmtint(spike['unmet_demand'].sum())} simulated units unmet over 60 days. Review contingency inventory and supplier capacity before promising availability.")
    if len(w):
        at_risk = w.sort_values('coverage_days').iloc[0]
        st.warning(f"🟠 **Warehouse watch:** {at_risk['warehouse_id']} / {at_risk['sku']} has {at_risk['coverage_days']:.2f} days of post-transfer coverage. Protect non-Amazon demand before approving FBA shipments.")
    st.success("🟢 **Baseline plan:** No unmet demand and no safety-stock breaches in the deterministic 60-day simulation.")
    left, right = st.columns([1.25,1])
    with left:
        st.subheader("12-week demand by channel")
        channels = f.groupby('channel', as_index=False)['forecast_units'].sum()
        fig = px.bar(channels, x='channel', y='forecast_units', color='channel', text='forecast_units', color_discrete_sequence=PALETTE)
        fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig.update_layout(showlegend=False, yaxis_title='Forecast units', xaxis_title='')
        chart(fig)
    with right:
        st.subheader("60-day risk: unmet demand")
        riskbar = s.groupby('scenario',as_index=False)['unmet_demand'].sum()
        fig=px.bar(riskbar,x='scenario',y='unmet_demand',color='scenario',text='unmet_demand',color_discrete_sequence=[GREEN,RED,ORANGE])
        fig.update_traces(texttemplate='%{text:,.0f}',textposition='outside')
        fig.update_layout(showlegend=False, xaxis_title='',yaxis_title='Units',xaxis_tickangle=-15)
        chart(fig)
    st.subheader("Priority actions · simulated as-of November 5, 2026")
    actions=o[['sku','recommended_order_date','recommended_arrival_date','recommended_units']].copy()
    if len(actions):
        actions['recommended_order_date']=actions['recommended_order_date'].dt.strftime('%b %d, %Y')
        actions['recommended_arrival_date']=actions['recommended_arrival_date'].dt.strftime('%b %d, %Y')
        actions=actions.rename(columns={'sku':'SKU','recommended_order_date':'Order by','recommended_arrival_date':'Target arrival','recommended_units':'Units to review'})
        table(actions)
    st.caption("These are hypothetical planning decisions from a historical scenario, not live action deadlines. Purchasing feasibility and supplier capacity are not yet confirmed.")

elif page == "Demand Forecast":
    st.header("Weekly demand forecast")
    st.caption("Fixed 4-week moving-average baseline projected forward 12 weeks. Forecast is not seasonally adjusted.")
    c1,c2,c3=st.columns(3)
    c1.metric('Total forecast · 12 weeks',fmtint(f['forecast_units'].sum()))
    c2.metric('Backtest WAPE · 1 week',f'{wape:.2f}%' if wape is not None else 'N/A')
    c3.metric('Average forecast / week',fmtint(f['forecast_units'].sum()/12))
    weekly_ch = f.groupby(['week','channel'],as_index=False)['forecast_units'].sum()
    fig=px.line(weekly_ch,x='week',y='forecast_units',color='channel',markers=True,color_discrete_sequence=PALETTE)
    fig.update_layout(yaxis_title='Units / week',xaxis_title='Week')
    chart(fig)
    st.subheader("Forecast error by model")
    if len(b):
        compare=b.groupby('model',as_index=False).agg(actual=('actual','sum'),abs_error=('absolute_error','sum'))
        compare['WAPE (%)']=100*compare['abs_error']/compare['actual']
        fig=px.bar(compare,x='model',y='WAPE (%)',color='model',text='WAPE (%)',color_discrete_sequence=[BLUE,ORANGE])
        fig.update_traces(texttemplate='%{text:.2f}%',textposition='outside')
        fig.update_layout(showlegend=False,xaxis_title='')
        chart(fig)
    st.info("The one-week WAPE does **not** establish accuracy over 12 weeks. Additional holdout tests over 12-week horizons and seasonality controls are needed.")
    table(f.sort_values(['week','channel','sku']))

elif page == "Inventory & Purchase Orders":
    st.header("Inventory health & purchase planning")
    c1,c2,c3=st.columns(3)
    c1.metric('Available units',fmtint(p['available_stock'].sum()))
    c2.metric('Incoming units',fmtint(p['incoming_units'].sum()))
    c3.metric('Proposed PO units',fmtint(o['recommended_units'].sum()))
    if len(p):
        fig=px.bar(p,x='sku',y='days_of_coverage',color='sku',color_discrete_sequence=PALETTE,text='days_of_coverage')
        fig.update_traces(texttemplate='%{text:.1f} d',textposition='outside')
        fig.update_layout(showlegend=False,xaxis_title='',yaxis_title='Days')
        chart(fig)
    st.subheader('Safety-stock-aware purchase orders')
    table(o)
    st.subheader('60-day inventory simulation (baseline plan)')
    proj=filtered(projection)
    fig=px.line(proj,x='date',y='ending_stock',color='sku',color_discrete_sequence=PALETTE)
    fig.update_layout(yaxis_title='Ending stock (units)',xaxis_title='Date')
    chart(fig)
    st.subheader('Contingency inventory estimates')
    table(m)
    st.warning("Contingency units assume stock is available from the beginning of the simulation. Supplier availability, actual lead times and cost must be checked before placement.")

elif page == "Amazon FBA & Warehouses":
    st.header('Amazon FBA replenishment & warehouse allocation')
    c1,c2,c3=st.columns(3)
    c1.metric('Proposed FBA transfer units',fmtint(fb['transfer_units'].sum()))
    c2.metric('Allocated FBA transfer units',fmtint(a['transfer_units'].sum()))
    c3.metric('Estimated transfer cost',fmtmoney(a['estimated_transfer_cost'].sum()))
    if len(fb):
        fig=px.bar(fb,x='sku',y='days_of_coverage',color='sku',text='days_of_coverage',color_discrete_sequence=PALETTE)
        fig.update_traces(texttemplate='%{text:.1f} d',textposition='outside')
        fig.update_layout(showlegend=False,xaxis_title='',yaxis_title='Days of FBA coverage')
        chart(fig)
    st.subheader('FBA replenishment by colorway')
    table(fb)
    st.subheader('Source-warehouse transfer proposals')
    table(a)
    st.subheader('3PL inventory after proposed transfers')
    if len(w):
        w2=w.copy()
        w2['label']=w2['warehouse_id']+' · '+w2['sku']
        fig=px.bar(w2,x='label',y='coverage_days',color='warehouse_id',text='coverage_days',color_discrete_sequence=PALETTE)
        fig.update_traces(texttemplate='%{text:.2f} d',textposition='outside')
        fig.add_hline(y=10,line_dash='dash',line_color=RED,annotation_text='10-day planning floor')
        fig.update_layout(xaxis_title='',yaxis_title='Days of post-transfer coverage')
        chart(fig)
    table(w)
    st.warning('Transfers are preliminary: FBA inbound limits, receiving times, in-transit units, regional demand and 3PL handling constraints are not modeled.')

elif page == "Fulfillment & Costs":
    st.header('Fulfillment costs & delivery operations')
    c1,c2,c3=st.columns(3)
    c1.metric('Sample units shipped',fmtint(fulfillment['total_units'].sum()))
    c2.metric('Sample shipment costs',fmtmoney(fulfillment['total_cost'].sum()))
    overall=fulfillment['total_cost'].sum()/fulfillment['total_units'].sum()
    c3.metric('Weighted shipping cost / unit',f'${overall:.2f}')
    fig=px.bar(fulfillment,x='warehouse_id',y='cost_per_unit',color='warehouse_id',text='cost_per_unit',color_discrete_sequence=PALETTE)
    fig.update_traces(texttemplate='$%{text:.2f}',textposition='outside')
    fig.update_layout(xaxis_title='',yaxis_title='Shipping cost / unit',showlegend=False)
    chart(fig)
    st.subheader('3PL / FBA scorecard')
    table(fulfillment)
    st.info('The delivery completion rate is the percentage marked Delivered at this snapshot, **not** on-time delivery. Data contains only eight simulated shipments and excludes storage and FBA service fees.')

else:
    st.header('Methodology & limitations')
    st.markdown('''**What the prototype demonstrates**\n\n- Synthetic sales generated across two illustrative SKUs and four sales channels.\n- Weekly baseline projections from a 4-week moving average, compared with linear trend on historical backtests.\n- Lead-time demand, simplified 7-day safety stock, reorder points, and 60-day inventory projection.\n- Purchase-order feasibility screening, demand-spike and supplier-delay stress tests.\n- FBA replenishment, cost-first warehouse transfers, and a sample fulfillment scorecard.\n\n**Limitations that matter before real operations**\n\n- The 12-week forecast has **not** been validated at a 12-week horizon; 3.89% WAPE applies only to a synthetic one-week rolling test.\n- Warehouse and supply records are an illustrative snapshot, not connected to live systems.\n- Demand forecasts, inbound orders, SKU quantities and costs use simplifying assumptions.\n- Mitigation units assume stock exists immediately; they are **not executable orders**.\n- FBA allocation omits Amazon receiving time, regional destination demand and some fees.\n- Fulfillment data is too small to establish actual warehouse efficiency.\n- The forecast and inventory simulations use different simplified horizons/assumptions; future work should reconcile these in one integrated planner.\n''')
    st.caption('Designed to demonstrate analytical thinking and decision trade-offs—not to represent or impersonate Pocket operational software.')

st.divider()
st.caption('INDEPENDENT PORTFOLIO PROJECT · ALL DATA SIMULATED · NOT AFFILIATED WITH POCKET · Developed as a supply chain analytics case study')
