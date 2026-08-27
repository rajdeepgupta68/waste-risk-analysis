-- Compare average units sold per transaction for promoted vs non-promoted perishable products, joined via product+store+week

SELECT
    (dp.had_display OR dp.had_mailer) AS was_promoted,
    COUNT(*)                          AS line_items,
    SUM(f.quantity)                   AS total_units,
    ROUND(AVG(f.quantity), 2)         AS avg_units_per_line,
    ROUND(SUM(f.sales_value), 2)      AS total_sales_value
FROM fact_transactions f
JOIN dim_product p ON f.product_id = p.product_id
JOIN dim_date d ON f.date_key = d.date_key
LEFT JOIN dim_promotion dp
    ON f.product_id = dp.product_id
    AND f.store_id = dp.store_id
    AND d.week_no = dp.week_no
WHERE p.is_perishable = TRUE
GROUP BY (dp.had_display OR dp.had_mailer)
ORDER BY was_promoted DESC NULLS LAST;