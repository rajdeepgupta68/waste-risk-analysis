-- Coefficient of variation in weekly sales per perishable category.
-- Higher CV = more unpredictable demand = higher waste/overstock risk.

WITH weekly_sales AS (
    SELECT
        p.department,
        p.commodity_desc,
        d.week_no,
        SUM(f.sales_value) AS weekly_value
    FROM fact_transactions f
    JOIN dim_product p ON f.product_id = p.product_id
    JOIN dim_date d ON f.date_key = d.date_key
    WHERE p.is_perishable = TRUE
    GROUP BY p.department, p.commodity_desc, d.week_no
)
SELECT
    department,
    commodity_desc,
    COUNT(*)                           AS weeks_with_sales,
    ROUND(AVG(weekly_value), 2)        AS avg_weekly_sales,
    ROUND(STDDEV(weekly_value), 2)     AS stddev_weekly_sales,
    ROUND(STDDEV(weekly_value) / NULLIF(AVG(weekly_value), 0), 3) AS coefficient_of_variation
FROM weekly_sales
GROUP BY department, commodity_desc
HAVING COUNT(*) >= 20  
ORDER BY coefficient_of_variation DESC
LIMIT 20;