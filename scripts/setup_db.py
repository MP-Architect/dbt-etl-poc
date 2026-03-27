import os

import pyodbc
from dotenv import load_dotenv

load_dotenv()

conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={os.getenv('DBT_SQLSERVER_HOST')},{os.getenv('DBT_SQLSERVER_PORT')};"
    f"DATABASE=master;"
    f"UID={os.getenv('DBT_SQLSERVER_USER')};"
    f"PWD={os.getenv('DBT_SQLSERVER_PASSWORD')};"
    f"TrustServerCertificate=yes;"
    f"Encrypt=no;"
)
conn.autocommit = True
cur = conn.cursor()

cur.execute(
    "IF NOT EXISTS (SELECT 1 FROM sys.databases WHERE name='etl_poc') CREATE DATABASE etl_poc"
)
cur.execute("USE etl_poc")

cur.execute("""
IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name='source_schema')
    EXEC('CREATE SCHEMA source_schema')
""")
cur.execute("""
IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name='dest_schema')
    EXEC('CREATE SCHEMA dest_schema')
""")

cur.execute("""
IF OBJECT_ID('source_schema.orders', 'U') IS NULL
CREATE TABLE source_schema.orders (
    order_id    INT PRIMARY KEY,
    customer    VARCHAR(100),
    product     VARCHAR(100),
    amount      DECIMAL(10,2),
    status      VARCHAR(20),   -- 'pending', 'shipped', 'cancelled'
    created_at  DATETIME DEFAULT GETDATE(),
    updated_at  DATETIME DEFAULT GETDATE()
)
""")

print("✓ Database and tables created")
