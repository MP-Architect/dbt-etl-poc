-- This test PASSES when the query returns 0 rows.
-- Any row returned = a failure.

WITH source_total AS (
    SELECT SUM(amount) AS total
    FROM etl_poc.source_schema.orders
    WHERE amount > 0          -- same filter as stg_orders.sql
),
dest_total AS (
    SELECT SUM(total_revenue) AS total
    FROM {{ ref('orders_summary') }}
),
comparison AS (
    SELECT
        source_total.total  AS source_revenue,
        dest_total.total    AS dest_revenue,
        ABS(
            source_total.total - dest_total.total
        )                   AS discrepancy
    FROM source_total
    CROSS JOIN dest_total
)
SELECT *
FROM comparison
WHERE discrepancy > 0.01    -- allow 1 cent rounding tolerance
