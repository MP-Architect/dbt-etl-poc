-- Verifies every source order appears in the summary aggregation.
-- The summary groups by product+status, so we check total row counts
-- match between source and the rolled-up grain.

WITH source_count AS (
    SELECT COUNT(*) AS cnt
    FROM etl_poc.source_schema.orders
    WHERE amount > 0
),
dest_count AS (
    SELECT SUM(order_count) AS cnt
    FROM {{ ref('orders_summary') }}
),
comparison AS (
    SELECT
        source_count.cnt    AS source_rows,
        dest_count.cnt      AS dest_rows,
        source_count.cnt - dest_count.cnt AS diff
    FROM source_count
    CROSS JOIN dest_count
)
SELECT *
FROM comparison
WHERE diff <> 0
