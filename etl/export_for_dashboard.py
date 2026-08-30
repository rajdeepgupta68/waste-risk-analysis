import duckdb
import os

DB_PATH = "sainsburys_waste_risk.duckdb"
OUTPUT_DIR = "dashboard/data"

QUERIES = {
    "perishable_share": "sql/perishable_share.sql",
    "category_breakdown": "sql/category_breakdown.sql",
    "promotion_effect": "sql/promotion_effect.sql",
    "weekly_volatility": "sql/weekly_volatility.sql",
    "store_variation": "sql/store_variation.sql",
    "priority_ranking": "sql/priority_ranking.sql",
}

# Extra query: full weekly time series per category, needed for the
# Page 3 line chart (click a category, see its weekly trend).
# Not tied to a numbered analysis query since it's dashboard-only.
WEEKLY_TIMESERIES_SQL = """
SELECT
    p.department,
    p.commodity_desc,
    d.week_no,
    ROUND(SUM(f.sales_value), 2) AS weekly_sales_value
FROM fact_transactions f
JOIN dim_product p ON f.product_id = p.product_id
JOIN dim_date d ON f.date_key = d.date_key
WHERE p.is_perishable = TRUE
GROUP BY p.department, p.commodity_desc, d.week_no
ORDER BY p.department, p.commodity_desc, d.week_no;
"""


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    con = duckdb.connect(DB_PATH)

    for name, sql_file in QUERIES.items():
        with open(sql_file) as f:
            query = f.read()
        df = con.execute(query).fetchdf()
        out_path = f"{OUTPUT_DIR}/{name}.csv"
        df.to_csv(out_path, index=False)
        print(f"Wrote {out_path} ({len(df)} rows)")

    # weekly time series (for the drill-down line chart)
    df_ts = con.execute(WEEKLY_TIMESERIES_SQL).fetchdf()
    out_path = f"{OUTPUT_DIR}/weekly_timeseries.csv"
    df_ts.to_csv(out_path, index=False)
    print(f"Wrote {out_path} ({len(df_ts)} rows)")

    con.close()
    print("\nAll dashboard data exported.")


if __name__ == "__main__":
    main()