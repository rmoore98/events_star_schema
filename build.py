"""Build the star schema: run each SQL file in the sql folder, in order."""
import glob
import duckdb

con = duckdb.connect("star.duckdb")
for path in sorted(glob.glob("sql/*.sql")):
    print(f"Running {path}")
    with open(path) as f:
        con.execute(f.read())
con.close()