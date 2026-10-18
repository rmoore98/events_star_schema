"""Run each query in the queries folder and print the results."""
import glob
import duckdb

con = duckdb.connect("star.duckdb")
for path in sorted(glob.glob("queries/*.sql")):
    print(f"\n{path}")
    with open(path) as f:
        print(con.sql(f.read()))
con.close()