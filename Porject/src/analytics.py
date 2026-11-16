from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

from .db import get_all_tables


def _prepare_frames() -> dict[str, pd.DataFrame]:
    tables = get_all_tables()
    products = tables["products"].copy()
    customers = tables["customers"].copy()
    transactions = tables["transactions"].copy()
    inventory = tables["inventory"].copy()
    recommendations = tables["recommendation"].copy()

    transactions["Transaction_Date"] = pd.to_datetime(transactions["Transaction_Date"])
    transactions["Final_Amount"] = pd.to_numeric(transactions["Final_Amount"], errors="coerce")
    products["Price"] = pd.to_numeric(products["Price"], errors="coerce")
    customers["Lifetime_Value"] = pd.to_numeric(customers["Lifetime_Value"], errors="coerce")
    customers["Purchase_Frequency"] = pd.to_numeric(customers["Purchase_Frequency"], errors="coerce")
    inventory["Current_Stock"] = pd.to_numeric(inventory["Current_Stock"], errors="coerce")
    return {
        "products": products,
        "customers": customers,
        "transactions": transactions,
        "inventory": inventory,
        "recommendations": recommendations,
    }


def compute_kpis() -> dict[str, float | int]:
    data = _prepare_frames()
    tx = data["transactions"]
    customers = data["customers"]
    inventory = data["inventory"]
    total_revenue = float(tx["Final_Amount"].sum())
    total_customers = int(customers["Customer_ID"].nunique())
    avg_order_value = float(tx.groupby("Transaction_ID")["Final_Amount"].sum().mean())
    active_customers = int(customers[customers["Account_Status"] == "Active"].shape[0])
    stock_items = int(inventory[inventory["Current_Stock"] > 0].shape[0])
    return {
        "total_revenue": total_revenue,
        "total_customers": total_customers,
        "avg_order_value": avg_order_value,
        "active_customers": active_customers,
        "stock_items": stock_items,
    }


def sales_trend() -> pd.DataFrame:
    tx = _prepare_frames()["transactions"]
    trend = tx.groupby(tx["Transaction_Date"].dt.to_period("M").astype(str), as_index=False)["Final_Amount"].sum()
    trend = trend.rename(columns={"Transaction_Date": "Month", "Final_Amount": "Revenue"})
    trend["Month"] = pd.to_datetime(trend["Month"].astype(str) + "-01")
    return trend.sort_values("Month")


def category_breakdown() -> pd.DataFrame:
    frames = _prepare_frames()
    tx = frames["transactions"].merge(frames["products"][["Product_ID", "Category"]], on="Product_ID", how="left")
    return tx.groupby("Category", as_index=False)["Final_Amount"].sum().sort_values("Final_Amount", ascending=False)


def customer_segments() -> pd.DataFrame:
    frames = _prepare_frames()
    customer_metrics = frames["customers"].copy()
    spend = frames["transactions"].groupby("Customer_ID", as_index=False)["Final_Amount"].sum().rename(columns={"Final_Amount": "Total_Spent"})
    customer_metrics = customer_metrics.merge(spend, on="Customer_ID", how="left")
    customer_metrics["Total_Spent"] = customer_metrics["Total_Spent"].fillna(0)
    customer_metrics["Recency_Days"] = (
        pd.Timestamp.today().normalize() - pd.to_datetime(customer_metrics["Last_Purchase_Date"]).dt.normalize()
    ).dt.days
    features = customer_metrics[["Lifetime_Value", "Purchase_Frequency", "Total_Spent", "Recency_Days"]]
    scaler = StandardScaler()
    scaled = scaler.fit_transform(features)
    model = KMeans(n_clusters=4, random_state=42, n_init=10)
    customer_metrics["Cluster"] = model.fit_predict(scaled)
    return customer_metrics[["Customer_ID", "Customer_Segment", "Cluster", "Lifetime_Value", "Total_Spent", "Purchase_Frequency", "Recency_Days"]]


def inventory_alerts() -> pd.DataFrame:
    inventory = _prepare_frames()["inventory"]
    return inventory[(inventory["Current_Stock"] <= 25) | (inventory["Status"] == "Out of Stock")].sort_values("Current_Stock")


def sales_forecast() -> pd.DataFrame:
    trend = sales_trend()
    if len(trend) < 2:
        return trend
    x = np.arange(len(trend)).reshape(-1, 1)
    y = trend["Revenue"].to_numpy()
    model = LinearRegression().fit(x, y)
    next_point = model.predict(np.array([[len(trend)]], dtype=float))[0]
    forecast = trend.copy()
    forecast = pd.concat([forecast, pd.DataFrame({"Month": [trend["Month"].max() + pd.DateOffset(months=1)], "Revenue": [next_point]})], ignore_index=True)
    return forecast


def anomaly_detection() -> pd.DataFrame:
    frames = _prepare_frames()
    daily = frames["transactions"].copy()
    daily["Day"] = daily["Transaction_Date"].dt.floor("D")
    daily = daily.groupby("Day", as_index=False)["Final_Amount"].sum().rename(columns={"Final_Amount": "Daily_Revenue"})
    daily["z_score"] = (daily["Daily_Revenue"] - daily["Daily_Revenue"].mean()) / (daily["Daily_Revenue"].std(ddof=0) or 1)
    return daily.loc[abs(daily["z_score"]) > 1.5].sort_values("z_score", ascending=False)


def recommendation_table() -> pd.DataFrame:
    frames = _prepare_frames()
    recommendations = frames["recommendations"].copy()
    rows = []
    for _, row in recommendations.iterrows():
        for idx in range(1, 6):
            rows.append({
                "Customer_ID": row["Customer_ID"],
                "Product_ID": row[f"Product_ID_{idx}"],
                "Match": row[f"Match_{idx}"],
                "Reason": row[f"Reason_{idx}"],
            })
    return pd.DataFrame(rows)
