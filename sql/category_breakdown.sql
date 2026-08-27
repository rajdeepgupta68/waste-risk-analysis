-- Sales value and volume by perishable category, ranked by revenue

SELECT
    p.department,
    p.commodity_desc,
    COUNT(*)                       AS line_items,
    SUM(f.quantity)                AS total_units,
    ROUND(SUM(f.sales_value), 2)   AS total_sales_value,
    ROUND(AVG(f.sales_value), 2)   AS avg_line_value
FROM fact_transactions f
JOIN dim_product p ON f.product_id = p.product_id
WHERE p.is_perishable = TRUE
GROUP BY p.department, p.commodity_desc
ORDER BY total_sales_value DESC
LIMIT 20;