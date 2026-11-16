from __future__ import annotations

import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


PRODUCTS = [
    ("PROD-001", "Aurora Trail Jacket", "Clothing", 129.0, "Lightweight outdoor jacket", "product_001.jpg", "Navy", "M", "Polyester", "Northwind", True, 48, 72.0),
    ("PROD-002", "Summit Running Tee", "Clothing", 45.0, "Moisture-wicking athletic shirt", "product_002.jpg", "Black", "L", "Cotton blend", "PeakMove", True, 78, 22.0),
    ("PROD-003", "Harbor Leather Boot", "Footwear", 180.0, "Premium casual boot", "product_003.jpg", "Brown", "9", "Leather", "Harbor & Co", True, 32, 92.0),
    ("PROD-004", "Crest Crossbody", "Accessories", 68.0, "Compact everyday crossbody bag", "product_004.jpg", "Tan", "One Size", "Canvas", "Crest", True, 61, 34.0),
    ("PROD-005", "Drift Running Sneaker", "Footwear", 110.0, "Responsive everyday sneaker", "product_005.jpg", "White", "7", "Mesh", "Stride", True, 85, 54.0),
    ("PROD-006", "Horizon Knit Polo", "Clothing", 95.0, "Structured knit polo", "product_006.jpg", "Ocean", "M", "Cotton", "Harbor & Co", True, 59, 41.0),
    ("PROD-007", "Breeze Travel Tote", "Accessories", 88.0, "Roomy carry-all with organizer pockets", "product_007.jpg", "Sand", "One Size", "Nylon", "Northwind", True, 42, 43.0),
    ("PROD-008", "Summit Hiker Boot", "Footwear", 160.0, "Water-resistant hiking footwear", "product_008.jpg", "Olive", "10", "Suede", "PeakMove", True, 30, 75.0),
    ("PROD-009", "Metro Wool Scarf", "Accessories", 54.0, "Soft knit scarf", "product_009.jpg", "Charcoal", "One Size", "Wool", "Meridian", True, 75, 22.0),
    ("PROD-010", "Valiant Hoodie", "Clothing", 118.0, "Midweight fleece hoodie", "product_010.jpg", "Slate", "XL", "Cotton fleece", "Northwind", True, 36, 58.0),
    ("PROD-011", "Coast Daypack", "Accessories", 72.0, "Weather-ready daypack", "product_011.jpg", "Forest", "One Size", "Ripstop", "Crest", True, 49, 31.0),
    ("PROD-012", "Velvet Evening Dress", "Clothing", 142.0, "Flattering party dress", "product_012.jpg", "Wine", "S", "Velvet", "Aster", True, 22, 78.0),
    ("PROD-013", "Solstice Sunglasses", "Accessories", 66.0, "Polarized everyday shades", "product_013.jpg", "Black", "One Size", "ACR", "Luma", True, 55, 24.0),
    ("PROD-014", "Ridge Sandal", "Footwear", 90.0, "Lightweight city sandal", "product_014.jpg", "Taupe", "8", "Synthetic", "Stride", True, 58, 40.0),
    ("PROD-015", "Harbor Knit Beanie", "Accessories", 40.0, "Warm knit cap", "product_015.jpg", "Midnight", "One Size", "Wool", "Meridian", True, 63, 15.0),
    ("PROD-016", "Marlow Chino", "Clothing", 88.0, "Classic tailored trouser", "product_016.jpg", "Stone", "32", "Cotton twill", "Northwind", True, 44, 39.0),
    ("PROD-017", "Cinder Trail Sneaker", "Footwear", 126.0, "Adventure-ready sneaker", "product_017.jpg", "Graphite", "9", "Mesh", "PeakMove", True, 50, 58.0),
    ("PROD-018", "Pine Lumen Watch", "Accessories", 220.0, "Minimalist analog watch", "product_018.jpg", "Silver", "One Size", "Steel", "Luma", True, 19, 113.0),
    ("PROD-019", "Echo Performance Tee", "Clothing", 52.0, "Performance shirt for active days", "product_019.jpg", "Cobalt", "L", "Performance knit", "Stride", True, 66, 23.0),
    ("PROD-020", "Moss Utility Cap", "Accessories", 48.0, "Structured cap with adjustable fit", "product_020.jpg", "Olive", "One Size", "Cotton", "Harbor & Co", True, 72, 18.0),
]


random.seed(42)


def build_products() -> pd.DataFrame:
    product_rows = []
    for product_id, name, category, price, description, image_file, colour, size, material, brand, in_stock, stock_qty, cost_price in PRODUCTS:
        product_rows.append({
            "Product_ID": product_id,
            "Product_Name": name,
            "Category": category,
            "Price": price,
            "Description": description,
            "Image_File": image_file,
            "Colour": colour,
            "Size": size,
            "Material": material,
            "Brand": brand,
            "In_Stock": "Yes" if in_stock else "No",
            "Stock_Qty": stock_qty,
            "Cost_Price": cost_price,
        })
    return pd.DataFrame(product_rows)


def build_customers() -> pd.DataFrame:
    segments = ["Premium", "Regular", "New", "VIP"]
    countries = ["USA", "Canada", "UK", "Germany", "France", "Australia"]
    first_names = ["Ava", "Noah", "Mia", "Leo", "Sophia", "Lucas", "Emma", "Ethan", "Olivia", "Mason", "Ella", "Jack"]
    last_names = ["Brown", "Smith", "Davis", "Miller", "Wilson", "Taylor", "Clark", "Moore", "Johnson", "Lee", "Anderson", "Baker"]
    rows = []
    for i in range(1, 251):
        customer_id = f"CUST-{i:03d}"
        segment = random.choice(segments)
        country = random.choice(countries)
        state = random.choice(["CA", "TX", "NY", "FL", "WA", "ON", "AL", "IL", "SF", "MEL"])
        lifetime_value = round(random.uniform(90, 4800), 2)
        if segment == "VIP":
            lifetime_value = round(random.uniform(2200, 9200), 2)
        if segment == "Premium":
            lifetime_value = round(random.uniform(800, 4200), 2)
        purchase_frequency = round(random.uniform(0.5, 6.0), 2)
        registration_date = (datetime(2021, 1, 1) + timedelta(days=random.randint(0, 1200))).strftime("%Y-%m-%d")
        last_purchase_date = (datetime(2024, 1, 1) + timedelta(days=random.randint(0, 700))).strftime("%Y-%m-%d")
        account_status = random.choice(["Active", "Inactive"])
        rows.append({
            "Customer_ID": customer_id,
            "Email": f"{first_names[i % len(first_names)].lower()}.{last_names[i % len(last_names)].lower()}{i}@example.com",
            "First_Name": first_names[i % len(first_names)],
            "Last_Name": last_names[i % len(last_names)],
            "Registration_Date": registration_date,
            "Customer_Segment": segment,
            "Country": country,
            "State": state,
            "Lifetime_Value": lifetime_value,
            "Last_Purchase_Date": last_purchase_date,
            "Purchase_Frequency": purchase_frequency,
            "Account_Status": account_status,
        })
    return pd.DataFrame(rows)


def build_transactions(products_df: pd.DataFrame, customers_df: pd.DataFrame, months: int = 12) -> pd.DataFrame:
    rows = []
    start = datetime(2024, 1, 1)
    product_ids = products_df["Product_ID"].tolist()
    customer_ids = customers_df["Customer_ID"].tolist()
    for i in range(1, 1801):
        customer_id = random.choice(customer_ids)
        product_id = random.choice(product_ids)
        product = products_df[products_df["Product_ID"] == product_id].iloc[0]
        date = start + timedelta(days=random.randint(0, 365))
        quantity = random.randint(1, 4)
        unit_price = float(product["Price"])
        total_price = round(quantity * unit_price, 2)
        discount = round(random.uniform(0.0, 0.25) * total_price, 2)
        final_amount = round(total_price - discount, 2)
        rows.append({
            "Transaction_ID": f"TXN-{i:04d}",
            "Customer_ID": customer_id,
            "Product_ID": product_id,
            "Transaction_Date": date.strftime("%Y-%m-%d"),
            "Quantity": quantity,
            "Unit_Price": unit_price,
            "Total_Price": total_price,
            "Discount": discount,
            "Final_Amount": final_amount,
            "Order_Status": "Completed",
        })
    return pd.DataFrame(rows)


def build_inventory(products_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, product in products_df.iterrows():
        current_stock = max(0, int(product["Stock_Qty"]))
        status = "In Stock" if current_stock > 0 else "Out of Stock"
        rows.append({
            "Product_ID": product["Product_ID"],
            "Current_Stock": current_stock,
            "Status": status,
            "Last_Updated": (datetime.now() - timedelta(days=random.randint(0, 15))).strftime("%Y-%m-%d"),
        })
    return pd.DataFrame(rows)


def build_recommendations(customers_df: pd.DataFrame, products_df: pd.DataFrame) -> pd.DataFrame:
    product_ids = products_df["Product_ID"].tolist()
    rows = []
    reasons = [
        "Popular with similar customers",
        "Frequently bought together",
        "Matches customer preferences",
        "High-value seasonal pickup",
        "Strong price-to-quality fit",
    ]
    for _, customer in customers_df.iterrows():
        recommended = []
        for idx in range(5):
            product_id = random.choice(product_ids)
            match = round(random.uniform(62.0, 98.0), 1)
            reason = reasons[random.randint(0, len(reasons) - 1)]
            recommended.append((product_id, match, reason))
        row = {"Customer_ID": customer["Customer_ID"]}
        for idx, item in enumerate(recommended, start=1):
            product_id, match, reason = item
            row[f"Product_ID_{idx}"] = product_id
            row[f"Match_{idx}"] = match
            row[f"Reason_{idx}"] = reason
        rows.append(row)
    return pd.DataFrame(rows)


def generate_demo_datasets(output_dir: str | Path) -> Path:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    products_df = build_products()
    customers_df = build_customers()
    transactions_df = build_transactions(products_df, customers_df)
    inventory_df = build_inventory(products_df)
    recommendations_df = build_recommendations(customers_df, products_df)

    products_df.to_csv(output_dir / "PRODUCTS.csv", index=False)
    customers_df.to_csv(output_dir / "CUSTOMERS.csv", index=False)
    transactions_df.to_csv(output_dir / "TRANSACTIONS.csv", index=False)
    inventory_df.to_csv(output_dir / "INVENTORY.csv", index=False)
    recommendations_df.to_csv(output_dir / "RECOMMENDATION.csv", index=False)
    return output_dir
