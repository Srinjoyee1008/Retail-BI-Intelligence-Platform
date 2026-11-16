from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src.analytics import (
    anomaly_detection,
    category_breakdown,
    compute_kpis,
    customer_segments,
    inventory_alerts,
    recommendation_table,
    sales_forecast,
    sales_trend,
)
from src.db import ensure_demo_data, reset_demo_data

st.set_page_config(page_title="Retail BI Intelligence Platform", layout="wide")


@st.cache_data
def refresh_metrics():
    ensure_demo_data()
    return {
        "kpis": compute_kpis(),
        "sales": sales_trend(),
        "category": category_breakdown(),
        "segments": customer_segments(),
        "inventory": inventory_alerts(),
        "forecast": sales_forecast(),
        "anomalies": anomaly_detection(),
        "recommendations": recommendation_table(),
    }


st.title("Retail BI Intelligence Platform")
st.caption("Local-first retail intelligence dashboard powered by the exact five-dataset schema.")

with st.sidebar:
    st.header("Controls")
    if st.button("Refresh demo data"):
        reset_demo_data()
        st.cache_data.clear()
        st.success("Demo datasets were refreshed.")
    st.caption("The app loads CSV-backed demo data and stores it in SQLite by default. Set DATABASE_URL to a PostgreSQL connection string to target Postgres.")

metrics = refresh_metrics()

kpis = metrics["kpis"]
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total revenue", f"${kpis['total_revenue']:,.2f}")
col2.metric("Customers", f"{kpis['total_customers']:,}")
col3.metric("Average order value", f"${kpis['avg_order_value']:,.2f}")
col4.metric("Active customers", f"{kpis['active_customers']:,}")

sales = metrics["sales"]
fig_sales = px.line(sales, x="Month", y="Revenue", title="Monthly revenue trend")
fig_sales.update_layout(template="plotly_white")
st.plotly_chart(fig_sales, use_container_width=True)

left, right = st.columns(2)
with left:
    category = metrics["category"]
    fig_category = px.bar(category, x="Category", y="Final_Amount", title="Category revenue")
    fig_category.update_layout(template="plotly_white")
    st.plotly_chart(fig_category, use_container_width=True)

with right:
    forecast = metrics["forecast"]
    fig_forecast = px.line(forecast, x="Month", y="Revenue", title="Revenue forecast")
    fig_forecast.update_layout(template="plotly_white")
    st.plotly_chart(fig_forecast, use_container_width=True)

left, right = st.columns(2)
with left:
    segments = metrics["segments"]
    fig_segments = px.scatter(
        segments,
        x="Lifetime_Value",
        y="Total_Spent",
        color="Cluster",
        size="Purchase_Frequency",
        hover_data=["Customer_ID", "Customer_Segment"],
        title="Customer value segmentation",
    )
    fig_segments.update_layout(template="plotly_white")
    st.plotly_chart(fig_segments, use_container_width=True)

with right:
    inventory = metrics["inventory"]
    if inventory.empty:
        st.info("No inventory issues in the current dataset.")
    else:
        st.dataframe(inventory, use_container_width=True, hide_index=True)

anomalies = metrics["anomalies"]
if anomalies.empty:
    st.info("No significant anomalies were detected in daily revenue.")
else:
    st.subheader("Anomaly detection")
    st.dataframe(anomalies, use_container_width=True, hide_index=True)

st.subheader("Top product recommendations")
recommendations = metrics["recommendations"]
if recommendations.empty:
    st.info("No recommendation rows to display.")
else:
    st.dataframe(recommendations.head(20), use_container_width=True, hide_index=True)

with st.expander("Dataset preview"):
    for table_name in ["PRODUCTS", "CUSTOMERS", "TRANSACTIONS", "INVENTORY", "RECOMMENDATION"]:
        st.write(f"### {table_name}")
        df = pd.read_sql_table(table_name, "sqlite:///" + str(__import__("pathlib").Path(__file__).resolve().parent / "retail_bi.db"))
        st.dataframe(df.head(5), use_container_width=True, hide_index=True)
