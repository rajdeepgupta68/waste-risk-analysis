import duckdb
import sys

DB_PATH = "sainsburys_waste_risk.duckdb"

def run(sql_file):
    con = duckdb.connect(DB_PATH)
    with open(sql_file) as f:
        query = f.read()
    df = con.execute(query).fetchdf()
    con.close()
    print(df.to_string(index=False))
    return df

if __name__ == "__main__":
    run(sys.argv[1])