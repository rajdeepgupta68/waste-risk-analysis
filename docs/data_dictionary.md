# Data Dictionary — Dunnhumby Complete Journey

## Tables used in this analysis

### transaction_data.csv
Grain: one row per product per basket (line item)
Rows: 2,595,732
Key columns: household_key, BASKET_ID, PRODUCT_ID, STORE_ID, DAY, WEEK_NO
Notes: DAY is a relative day number (1–711ish), not a calendar date - must be anchored to an assumed start date for seasonality features. No nulls.

### product.csv
Grain: one row per product (SKU)
Rows: 92,353
Key columns: PRODUCT_ID, DEPARTMENT, COMMODITY_DESC, SUB_COMMODITY_DESC
Notes: Category naming isn't literal about freshness (e.g. "FRUIT - SHELF STABLE" is canned, not fresh) - perishability must be manually mapped from DEPARTMENT/COMMODITY_DESC, not inferred from department name alone. No nulls.

### causal_data.csv
Grain: one row per product per store per week
Rows: 36,786,524
Key columns: PRODUCT_ID, STORE_ID, WEEK_NO, display, mailer
Notes: display/mailer are categorical placement codes; simplified to binary had_display / had_mailer flags for this analysis. No nulls. Large table — join via SQL/DuckDB, not pandas merge.

### hh_demographic.csv (optional enrichment)
Grain: one row per household
Rows: 801 (partial coverage - ~32% of households in transaction_data)
Notes: Use left join; treat missing demographics as "unknown" rather than dropping. Not required for core waste-risk analysis.

## Tables considered, excluded from scope
- coupon.csv, coupon_redempt.csv, campaign_desc.csv, campaign_table.csv - coupon/campaign volume is negligible (2,318 redemptions vs 2.6M transactions); out of scope for waste-risk framing.