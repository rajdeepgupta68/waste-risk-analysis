
-- Perishable sales as a share of total sales, per store - flags stores
-- with disproportionately high perishable exposure.

WITH store_totals AS (
    SELECT
        f.store_id,
        SUM(f.sales_value) AS total_sales,
        SUM(CASE WHEN p.is_perishable THEN f.sales_value ELSE 0 END) AS perishable_sales
    FROM fact_transactions f
    JOIN dim_product p ON f.product_id = p.product_id
    GROUP BY f.store_id
)
SELECT
    store_id,
    ROUND(total_sales, 2)      AS total_sales,
    ROUND(perishable_sales, 2) AS perishable_sales,
    ROUND(100.0 * perishable_sales / NULLIF(total_sales, 0), 1) AS pct_perishable
FROM store_totals
WHERE total_sales > 1000  -- exclude near-empty stores that would skew the ranking
ORDER BY pct_perishable DESC
LIMIT 15;