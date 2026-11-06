# 📦  Inspired by Pocket AI — Supply Chain Intelligence & Inventory Optimization

### End-to-End Supply Chain Analytics | Python • SQL • Forecasting • Streamlit

> **Independent Portfolio Project | Simulated Data | Not Affiliated with Pocket**

## 🚀 Project Overview

An end-to-end supply chain analytics and decision-support system inspired by the operational challenges of Pocket (YC W26), an AI hardware startup.

This project demonstrates how data analytics can support demand forecasting, inventory optimization, purchase-order planning, Amazon FBA replenishment, warehouse allocation, and fulfillment operations.

The primary objective is to answer three critical business questions:

1. **How many units will we sell?**
2. **When should we reorder inventory, and how much?**
3. **Where should inventory be positioned to balance availability, delivery speed, and cost?**

The project uses synthetic sales, inventory, supplier, and fulfillment data to simulate the challenges of scaling a physical consumer product business.

---

## 📊 Executive Summary

| KPI | Simulated Result |
|-----|------------------|
| 12-Week Demand Forecast | 525,780 units |
| One-Week Forecast WAPE | 3.89% |
| One-Week Forecast Accuracy (100% − WAPE) | 96.11% |
| Baseline Unmet Demand | 0 units |
| Unmet Demand Under 30% Spike | 68,698 units |
| Recommended Black Device PO | 68,000 units |
| Recommended Silver Device PO | 42,000 units |
| Amazon FBA Transfer Recommendation | 40,011 units |
| Estimated FBA Transfer Cost | $48,993.60 |
| Average Fulfillment Cost | $4.25 per unit |

**Note:** All results are based on simulated data. The 3.89% WAPE applies to a historical one-week-ahead backtest, not the full 12-week forecast.

---

## 🎯 Business Problems Addressed

### 1. Demand Forecasting

Built a forecasting framework to estimate future device demand across:

- Amazon
- Direct-to-Consumer (DTC)
- Retail
- International markets

Compared linear regression with a four-week moving-average model.

**Results:**

| Forecasting Model | One-Week WAPE |
|-------------------|---------------|
| Linear Trend | 8.04% |
| 4-Week Moving Average | 3.89% |

The four-week moving average performed better in the simulated historical backtest.

Generated a 12-week baseline demand forecast of approximately **525,780 units**.

### 2. Inventory Optimization

Developed inventory planning calculations covering:

- Available inventory
- Days of inventory coverage
- Supplier lead times
- Safety stock
- Reorder points
- Inventory position
- Minimum order quantities (MOQ)

The model evaluates projected demand and incoming purchase orders to identify inventory risks.

### 3. Purchase Order Recommendations

Created a purchase-order recommendation engine using demand estimates, supplier lead times, incoming orders, and inventory requirements.

| Product | Recommended Quantity | Order Date |
|---------|----------------------|------------|
| Pocket Black | 68,000 units | November 28, 2026 |
| Pocket Silver | 42,000 units | November 21, 2026 |

Validated recommendations using a 60-day inventory simulation.

**Baseline validation results:**
- Zero unmet demand
- Zero days below safety stock
- Inventory maintained above the simulated safety-stock thresholds

### 4. Supply Chain Risk Simulation

Developed scenario simulations to evaluate inventory resilience.

| Scenario | Unmet Demand | Operational Impact |
|----------|--------------|--------------------|
| Baseline | 0 units | Inventory plan meets projected demand |
| 30% Demand Spike | 68,698 units | Additional replenishment required |
| 7-Day Supplier Delay | 0 units | Safety-stock buffer breached |

Estimated additional inventory required to maintain safety-stock targets:

| Scenario | Black | Silver |
|----------|-------|--------|
| 30% Demand Spike | 79,000 | 34,000 |
| 7-Day Supplier Delay | 25,000 | 10,000 |

These estimates assume additional inventory is available at the beginning of the simulation. They are not yet validated expedited purchase orders.

### 5. Amazon FBA Replenishment

Developed an Amazon FBA inventory planning model covering:

- FBA available inventory
- Daily Amazon demand
- Days of inventory coverage
- Target stock levels
- Replenishment requirements
- Warehouse-to-FBA allocation

**Simulated recommendation:**

| Product | Current Coverage | FBA Transfer Units |
|---------|------------------|--------------------|
| Black | 13.57 days | 28,748 |
| Silver | 15.07 days | 11,263 |
| **Total** | | **40,011** |

### 6. Warehouse Allocation Optimization

Modeled inventory transfers from hypothetical California and New Jersey warehouses to Amazon FBA.

The allocation logic prioritizes lower transportation costs while protecting inventory for non-Amazon sales.

**Estimated transfer cost: $48,993.60**

Validated that all four warehouse/SKU combinations maintain at least 10 days of projected inventory coverage after transfers.

### 7. Fulfillment Performance Analytics

Analyzed fulfillment efficiency across Amazon FBA and third-party logistics (3PL) warehouses.

| Fulfillment Location | Shipping Cost per Unit |
|----------------------|------------------------|
| Amazon FBA | $3.12 |
| California Warehouse | $4.72 |
| New Jersey Warehouse | $5.52 |

**Overall simulated fulfillment cost: $4.25 per unit.**

The analysis also examines delivery duration, shipment status, and fulfillment performance.

---

## 🛠️ Technology Stack

| Technology | Application |
|------------|-------------|
| Python | Data processing and business logic |
| Pandas | Data transformation and analytics |
| NumPy | Numerical calculations and simulations |
| SQL / SQLite | Relational data modeling and analysis |
| Plotly | Interactive data visualizations |
| Streamlit | Web-based executive dashboard |
| Google Colab | Python development and experimentation |
| GitHub | Version control and project documentation |

---

## 📁 Project Structure

```text
pocket-supply-chain-intelligence/
│
├── README.md
├── app.py
├── requirements.txt
│
└── data/
    ├── sales_history.csv
    ├── demand_forecast.csv
    ├── forecast_backtest.csv
    ├── inventory_planning.csv
    ├── purchase_orders.csv
    ├── inventory_projection.csv
    ├── scenario_summary.csv
    ├── scenario_daily.csv
    ├── risk_mitigation.csv
    ├── fba_replenishment.csv
    ├── fba_allocation.csv
    ├── warehouse_inventory.csv
    └── fulfillment_performance.csv
```

---

## 💻 How to Run the Dashboard

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/pocket-supply-chain-intelligence.git
```

### 2. Navigate to the project

```bash
cd pocket-supply-chain-intelligence
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Launch the application

```bash
streamlit run app.py
```

The dashboard will open in your browser.

---

## 📈 Dashboard Features

The interactive dashboard includes five sections:

**Executive Overview**
- 12-week projected demand
- Forecast accuracy
- Inventory risk exposure
- Business performance indicators

**Demand Forecasting**
- Demand by sales channel
- SKU-level demand projections
- Forecast model comparisons

**Inventory Planning**
- Days of coverage
- Purchase-order recommendations
- Safety-stock requirements
- Risk mitigation analysis

**Amazon FBA**
- FBA inventory health
- Transfer planning
- Warehouse allocation
- Estimated transportation costs

**Fulfillment Operations**
- Shipping costs
- Fulfillment performance
- Warehouse comparisons

---

## 💡 Key Business Insights

1. Historical forecasting accuracy should be evaluated before relying on projected demand for purchasing decisions.

2. Inventory-position calculations alone can conceal shortages when incoming purchase orders arrive too late.

3. Supply chain plans that perform well under normal conditions may fail during unexpected demand spikes.

4. Amazon FBA replenishment decisions must account for inventory requirements across DTC, retail, and international channels.

5. Transportation cost optimization should not compromise inventory availability or delivery performance.

6. Supply chain dashboards are most valuable when they translate operational data into actionable recommendations.

---

## ⚠️ Data and Methodology Disclaimer

This project is an independent educational and portfolio demonstration.

All sales volumes, SKUs, product variations, costs, suppliers, purchase orders, warehouse locations, fulfillment metrics, and inventory quantities are synthetic or illustrative.

The project does not use Pocket's confidential operational information.

Forecasting results were evaluated against synthetic historical demand. Actual business performance could differ significantly.

Certain calculations use simplified assumptions regarding supplier lead times, demand variability, warehouse allocation, inventory availability, and purchase-order fulfillment.

The dashboard is a decision-support prototype, not a production-ready supply chain management system.

---

## 🔮 Future Improvements

- Probabilistic demand forecasting
- Service-level-based safety stock optimization
- Amazon FBA inbound receiving constraints
- Regional warehouse demand allocation
- Supplier reliability scoring
- Working capital optimization
- Automated inventory reconciliation
- Real-time WMS and ERP integration
- AI-powered supply chain insights

---

## 👨‍💻 Project Author

**Vedatava Upadhyay**

Business Analytics | Data Analytics | Supply Chain Analytics

*Independent portfolio project demonstrating the application of data analytics to supply chain planning and operational decision-making.*
