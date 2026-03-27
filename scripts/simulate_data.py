"""Run this any time to insert new rows or update existing ones."""

import os
import random

import pyodbc
from dotenv import load_dotenv

load_dotenv()

PRODUCTS = ["Widget A", "Gadget B", "Doohickey C", "Thingamajig D"]
CUSTOMERS = ["Alice", "Bob", "Carol", "David", "Eve"]
STATUSES = ["pending", "shipped", "cancelled"]


def get_conn():
    return pyodbc.connect(
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={os.getenv('DBT_SQLSERVER_HOST')},{os.getenv('DBT_SQLSERVER_PORT')};"
        f"DATABASE=etl_poc;UID={os.getenv('DBT_SQLSERVER_USER')};"
        f"PWD={os.getenv('DBT_SQLSERVER_PASSWORD')}"
    )


def insert_orders(n=5):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT ISNULL(MAX(order_id), 0) FROM source_schema.orders")
    max_id = cur.fetchone()[0]
    for i in range(1, n + 1):
        cur.execute(
            """
            INSERT INTO source_schema.orders (order_id, customer, product, amount, status)
            VALUES (?, ?, ?, ?, 'pending')
        """,
            max_id + i,
            random.choice(CUSTOMERS),
            random.choice(PRODUCTS),
            round(random.uniform(10, 500), 2),
        )
    conn.commit()
    print(f"✓ Inserted {n} new orders (ids {max_id + 1}–{max_id + n})")


def update_statuses():
    """Randomly advance some pending orders to shipped or cancelled."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT order_id FROM source_schema.orders WHERE status='pending'")
    pending = [row[0] for row in cur.fetchall()]
    to_update = random.sample(pending, min(3, len(pending)))
    for oid in to_update:
        new_status = random.choice(["shipped", "cancelled"])
        cur.execute(
            """
            UPDATE source_schema.orders
            SET status=?, updated_at=GETDATE()
            WHERE order_id=?
        """,
            new_status,
            oid,
        )
    conn.commit()
    print(f"✓ Updated {len(to_update)} orders: {to_update}")


if __name__ == "__main__":
    insert_orders(5)
    update_statuses()
