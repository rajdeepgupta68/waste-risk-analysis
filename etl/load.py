# etl/load.py
import pandas as pd
import duckdb
from datetime import datetime, timedelta

DATA_DIR = "data"
DB_PATH = "sainsburys_waste_risk.duckdb"

# --- Perishable classification lists (from docs/perishable_mapping.md) ---
PERISHABLE_DEPARTMENTS = {
    'PRODUCE', 'MEAT', 'MEAT-PCKGD', 'MEAT-WHSE', 'PORK', 'DELI',
    'DELI/SNACK BAR', 'DAIRY DELI', 'PASTRY', 'GRO BAKERY', 'SEAFOOD',
    'SEAFOOD-PCKGD', 'SALAD BAR', 'FLORAL', 'FROZEN GROCERY'
}

PERISHABLE_GROCERY_COMMODITIES = {
    # fresh-adjacent dairy/bakery
    'CHEESE', 'YOGURT', 'FLUID MILK PRODUCTS', 'MILK BY-PRODUCTS',
    'REFRGRATD DOUGH PRODUCTS', 'REFRGRATD JUICES/DRNKS',
    'BAKED BREAD/BUNS/ROLLS', 'BAKED SWEET GOODS', 'EGGS', 'BUTTER',
    'MARGARINES',
    # frozen
    'FRZN MEAT/MEAT DINNERS', 'FROZEN PIZZA', 'FRZN VEGETABLE/VEG DSH',
    'FRZN NOVELTIES/WTR ICE', 'FRZN BREAKFAST FOODS', 'FROZEN PIE/DESSERTS',
    'FRZN POTATOES', 'FROZEN BREAD/DOUGH', 'FRZN JCE CONC/DRNKS',
    'FRZN FRUITS', 'FRZN ICE', 'FROZEN CHICKEN', 'FRZN SEAFOOD'
}

EXCLUDED_DEPARTMENTS = {
    'MISC. TRANS.', 'MISC SALES TRAN', 'COUP/STR & MFG', 'TRAVEL & LEISUR',
    'KIOSK-GAS', 'CHEF SHOPPE', 'CNTRL/STORE SUP', 'GM MERCH EXP',
    'POSTAL CENTER', 'CHARITABLE CONT', 'PROD-WHS SALES', 'RESTAURANT', ''
}

# Assumed anchor date: DAY 1 = this date. Dunnhumby doesn't publish a real
# start date, so this is a documented assumption, not a fact.
ANCHOR_DATE = datetime(2017, 1, 1)


def is_perishable(department, commodity_desc):
    if department in PERISHABLE_DEPARTMENTS:
        return True
    if department == 'GROCERY' and commodity_desc in PERISHABLE_GROCERY_COMMODITIES:
        return True
    return False


def build_dim_product():
    df = pd.read_csv(f"{DATA_DIR}/product.csv")
    df.columns = [c.strip().upper() for c in df.columns]

    # drop excluded departments entirely
    df = df[~df['DEPARTMENT'].isin(EXCLUDED_DEPARTMENTS)].copy()

    df['IS_PERISHABLE'] = df.apply(
        lambda r: is_perishable(r['DEPARTMENT'], r['COMMODITY_DESC']), axis=1
    )

    dim_product = df.rename(columns={
        'PRODUCT_ID': 'product_id',
        'MANUFACTURER': 'manufacturer',
        'DEPARTMENT': 'department',
        'BRAND': 'brand',
        'COMMODITY_DESC': 'commodity_desc',
        'SUB_COMMODITY_DESC': 'sub_commodity_desc',
        'CURR_SIZE_OF_PRODUCT': 'curr_size_of_product',
        'IS_PERISHABLE': 'is_perishable'
    })[['product_id', 'department', 'commodity_desc', 'sub_commodity_desc',
        'brand', 'manufacturer', 'curr_size_of_product', 'is_perishable']]

    return dim_product


def build_dim_date(max_day=711):
    rows = []
    for day_number in range(1, max_day + 1):
        cal_date = ANCHOR_DATE + timedelta(days=day_number - 1)
        rows.append({
            'date_key': day_number,
            'day_number': day_number,
            'calendar_date': cal_date.date(),
            'week_no': (day_number - 1) // 7 + 1,
            'day_of_week': cal_date.strftime('%A'),
            'month': cal_date.month,
            'is_weekend': cal_date.weekday() >= 5
        })
    return pd.DataFrame(rows)


def build_dim_store(transactions):
    stores = transactions['STORE_ID'].drop_duplicates().rename('store_id')
    return stores.to_frame()


def build_dim_household():
    df = pd.read_csv(f"{DATA_DIR}/hh_demographic.csv")
    df.columns = [c.strip().upper() for c in df.columns]
    return df.rename(columns={
        'HOUSEHOLD_KEY': 'household_key',
        'AGE_DESC': 'age_desc',
        'MARITAL_STATUS_CODE': 'marital_status_code',
        'INCOME_DESC': 'income_desc',
        'HOMEOWNER_DESC': 'homeowner_desc',
        'HH_COMP_DESC': 'hh_comp_desc',
        'HOUSEHOLD_SIZE_DESC': 'household_size_desc',
        'KID_CATEGORY_DESC': 'kid_category_desc'
    })


def build_dim_promotion():
    df = pd.read_csv(f"{DATA_DIR}/causal_data.csv")
    df.columns = [c.strip().upper() for c in df.columns]
    df['HAD_DISPLAY'] = df['display'.upper()] != '0'
    df['HAD_MAILER'] = df['mailer'.upper()] != '0'
    return df.rename(columns={
        'PRODUCT_ID': 'product_id',
        'STORE_ID': 'store_id',
        'WEEK_NO': 'week_no',
        'HAD_DISPLAY': 'had_display',
        'HAD_MAILER': 'had_mailer'
    })[['product_id', 'store_id', 'week_no', 'had_display', 'had_mailer']]


def build_fact_transactions(dim_product):
    df = pd.read_csv(f"{DATA_DIR}/transaction_data.csv")
    df.columns = [c.strip().upper() for c in df.columns]

    # only keep transactions for products we kept in dim_product
    df = df[df['PRODUCT_ID'].isin(dim_product['product_id'])].copy()

    return df.rename(columns={
        'BASKET_ID': 'basket_id',
        'household_key'.upper(): 'household_key',
        'PRODUCT_ID': 'product_id',
        'STORE_ID': 'store_id',
        'DAY': 'date_key',
        'QUANTITY': 'quantity',
        'SALES_VALUE': 'sales_value',
        'RETAIL_DISC': 'retail_disc',
        'COUPON_DISC': 'coupon_disc',
        'TRANS_TIME': 'trans_time'
    })[['basket_id', 'household_key', 'product_id', 'store_id', 'date_key',
        'quantity', 'sales_value', 'retail_disc', 'coupon_disc', 'trans_time']]


def main():
    print("Building dim_product...")
    dim_product = build_dim_product()

    print("Building dim_date...")
    dim_date = build_dim_date()

    print("Loading transaction_data for dim_store + fact_transactions...")
    raw_txn = pd.read_csv(f"{DATA_DIR}/transaction_data.csv")
    raw_txn.columns = [c.strip().upper() for c in raw_txn.columns]

    dim_store = build_dim_store(raw_txn)
    dim_household = build_dim_household()
    dim_promotion = build_dim_promotion()
    fact_transactions = build_fact_transactions(dim_product)

    print("Writing to DuckDB...")
    con = duckdb.connect(DB_PATH)
    con.execute("DROP TABLE IF EXISTS dim_product")
    con.execute("DROP TABLE IF EXISTS dim_date")
    con.execute("DROP TABLE IF EXISTS dim_store")
    con.execute("DROP TABLE IF EXISTS dim_household")
    con.execute("DROP TABLE IF EXISTS dim_promotion")
    con.execute("DROP TABLE IF EXISTS fact_transactions")

    con.execute("CREATE TABLE dim_product AS SELECT * FROM dim_product")
    con.execute("CREATE TABLE dim_date AS SELECT * FROM dim_date")
    con.execute("CREATE TABLE dim_store AS SELECT * FROM dim_store")
    con.execute("CREATE TABLE dim_household AS SELECT * FROM dim_household")
    con.execute("CREATE TABLE dim_promotion AS SELECT * FROM dim_promotion")
    con.execute("CREATE TABLE fact_transactions AS SELECT * FROM fact_transactions")

    print("Row counts:")
    for table in ['dim_product', 'dim_date', 'dim_store', 'dim_household',
                   'dim_promotion', 'fact_transactions']:
        count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {count:,}")

    con.close()
    print(f"\nDone. Database written to {DB_PATH}")


if __name__ == "__main__":
    main()