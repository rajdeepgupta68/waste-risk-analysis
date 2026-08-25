-- dim_date: built manually, not from a source file
CREATE TABLE dim_date (
    date_key        INTEGER PRIMARY KEY,
    day_number      INTEGER NOT NULL,      -- original relative DAY from transaction_data
    calendar_date   DATE NOT NULL,         -- reconstructed real date
    week_no         INTEGER NOT NULL,
    day_of_week     VARCHAR,
    month           INTEGER,
    is_weekend      BOOLEAN
);

-- dim_product: from product.csv, plus derived waste-risk flag
CREATE TABLE dim_product (
    product_id              INTEGER PRIMARY KEY,
    department              VARCHAR,
    commodity_desc          VARCHAR,
    sub_commodity_desc      VARCHAR,
    brand                   VARCHAR,
    manufacturer            VARCHAR,
    curr_size_of_product    VARCHAR,
    is_perishable           BOOLEAN         
);

-- dim_store: minimal, no attributes in this dataset
CREATE TABLE dim_store (
    store_id    INTEGER PRIMARY KEY
);

-- dim_household: optional enrichment, ~32% coverage
CREATE TABLE dim_household (
    household_key       INTEGER PRIMARY KEY,
    age_desc             VARCHAR,
    marital_status_code  VARCHAR,
    income_desc           VARCHAR,
    homeowner_desc        VARCHAR,
    hh_comp_desc          VARCHAR,
    household_size_desc  VARCHAR,
    kid_category_desc    VARCHAR
);

-- dim_promotion: from causal_data.csv, simplified to binary flags
CREATE TABLE dim_promotion (
    product_id   INTEGER NOT NULL,
    store_id     INTEGER NOT NULL,
    week_no      INTEGER NOT NULL,
    had_display  BOOLEAN,
    had_mailer   BOOLEAN,
    PRIMARY KEY (product_id, store_id, week_no)
);

-- fact_transactions: the core fact table
CREATE TABLE fact_transactions (
    basket_id         BIGINT NOT NULL,
    household_key     INTEGER,
    product_id        INTEGER NOT NULL REFERENCES dim_product(product_id),
    store_id          INTEGER NOT NULL REFERENCES dim_store(store_id),
    date_key          INTEGER NOT NULL REFERENCES dim_date(date_key),
    quantity          INTEGER,
    sales_value       DECIMAL(10,2),
    retail_disc       DECIMAL(10,2),
    coupon_disc       DECIMAL(10,2),
    trans_time        INTEGER
);