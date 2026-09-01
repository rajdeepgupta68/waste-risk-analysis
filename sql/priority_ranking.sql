-- Combines revenue exposure and demand volatility into a single
-- waste-risk priority score per perishable category.
-- Both components are normalized (0-1) then averaged equally.

WITH category_sales AS (
    SELECT
        p.department,
        p.commodity_desc,
        SUM(f.sales_value) AS total_sales_value
    FROM fact_transactions f
    JOIN dim_product p ON f.product_id = p.product_id
    WHERE p.is_perishable = TRUE
    GROUP BY p.department, p.commodity_desc
),
weekly_sales AS (
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
),
volatility AS (
    SELECT
        department,
        commodity_desc,
        COUNT(*) AS weeks_with_sales,
        ROUND(STDDEV(weekly_value) / NULLIF(AVG(weekly_value), 0), 3) AS coefficient_of_variation
    FROM weekly_sales
    GROUP BY department, commodity_desc
    HAVING COUNT(*) >= 20
),
combined AS (
    SELECT
        s.department,
        s.commodity_desc,
        s.total_sales_value,
        v.coefficient_of_variation,
        -- normalize each metric to 0-1 range across all categories
        (s.total_sales_value - MIN(s.total_sales_value) OVER ()) /
            NULLIF(MAX(s.total_sales_value) OVER () - MIN(s.total_sales_value) OVER (), 0) AS revenue_score,
        (v.coefficient_of_variation - MIN(v.coefficient_of_variation) OVER ()) /
            NULLIF(MAX(v.coefficient_of_variation) OVER () - MIN(v.coefficient_of_variation) OVER (), 0) AS volatility_score
    FROM category_sales s
    JOIN volatility v
        ON s.department = v.department AND s.commodity_desc = v.commodity_desc
)
SELECT
    department,
    commodity_desc,
    ROUND(total_sales_value, 2)     AS total_sales_value,
    coefficient_of_variation,
    ROUND(revenue_score, 3)         AS revenue_score,
    ROUND(volatility_score, 3)      AS volatility_score,
    ROUND((revenue_score + volatility_score) / 2, 3) AS priority_score
FROM combined
ORDER BY priority_score DESC
LIMIT 20;