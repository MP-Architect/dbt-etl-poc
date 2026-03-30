-- Mart: aggregate by product and status — the destination table
SELECT
    product_name,
    order_status,
    COUNT(*)                    AS order_count,
    SUM(order_amount)           AS total_revenue,
    AVG(order_amount)           AS avg_order_value,
    MIN(order_amount)           AS min_order,
    MAX(order_amount)           AS max_order,
    CAST(GETDATE() AS DATE)     AS snapshot_date
FROM {{ ref('stg_orders') }}
GROUP BY product_name, order_status
