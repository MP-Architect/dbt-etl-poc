-- Staging: rename columns, cast types, filter bad data
SELECT
    order_id,
    UPPER(TRIM(customer))           AS customer_name,
    UPPER(TRIM(product))            AS product_name,
    CAST(amount AS DECIMAL(10, 2))  AS order_amount,
    LOWER(status)                   AS order_status,
    created_at,
    updated_at
FROM etl_poc.source_schema.orders
WHERE amount > 0   -- data quality guard
