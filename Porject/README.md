# Retail BI Intelligence Platform

This project delivers a local-first retail business intelligence dashboard for the exact five datasets described in the project brief:

- PRODUCTS
- CUSTOMERS
- TRANSACTIONS
- INVENTORY
- RECOMMENDATION

It is built with Python, Streamlit, pandas, scikit-learn, and SQLAlchemy. The app defaults to SQLite for local execution and supports PostgreSQL by setting `DATABASE_URL`.

## Quick start

1. Open a terminal in this folder.
2. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Start the app:

```bash
streamlit run app.py
```

4. To run PostgreSQL locally, use Docker Compose:

```bash
docker compose up -d postgres
```

Set the environment variable:

```bash
export DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/retail_bi
```

Then start the app again.

## Project structure

```text
Porject/
├── app.py
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── README.md
├── data/
│   ├── PRODUCTS.csv
│   ├── CUSTOMERS.csv
│   ├── TRANSACTIONS.csv
│   ├── INVENTORY.csv
│   └── RECOMMENDATION.csv
├── src/
│   ├── __init__.py
│   ├── analytics.py
│   ├── config.py
│   ├── data_generation.py
│   └── db.py
└── retail_bi.db
```

## Included analytical features

- KPI overview for revenue, customers, and order value
- Monthly sales trend analysis
- Category performance analysis
- Customer segmentation with K-Means clustering
- Inventory health monitoring
- Daily revenue anomaly detection
- Product recommendation display
