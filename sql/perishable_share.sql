-- What share of transactions/revenue comes from perishable vs non-perishable products?

SELECT
    p.is_perishable,
    COUNT(*)                       AS line_items,
    SUM(f.quantity)                AS total_units,
    ROUND(SUM(f.sales_value), 2)   AS total_sales_value,
    ROUND(100.0 * SUM(f.sales_value) / SUM(SUM(f.sales_value)) OVER (), 1) AS pct_of_total_sales
FROM fact_transactions f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY p.is_perishable
ORDER BY p.is_perishable DESC;