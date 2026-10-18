"""Build the star schema: run each SQL file in the sql folder, in order."""
import glob
import duckdb

con = duckdb.connect("star.duckdb")
for path in sorted(glob.glob("sql/*.sql")):
    print(f"Running {path}")
    with open(path) as f:
        con.execute(f.read())

# Print how many rows each table has, as a quick check
for table in ["dim_event_type", "dim_user", "dim_date", "fact_events"]:
    count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"{table}: {count} rows")
    
con.close()