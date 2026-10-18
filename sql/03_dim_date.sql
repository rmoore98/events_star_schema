-- dim_date: one row for each day in the data's date range
CREATE OR REPLACE TABLE dim_date (
    date_key   INTEGER PRIMARY KEY,
    full_date  DATE,
    day_name   VARCHAR,
    month_name VARCHAR,
    is_weekend BOOLEAN
);

WITH days AS (
    SELECT CAST(generate_series AS DATE) AS day
    FROM generate_series(DATE '2026-08-01', DATE '2026-09-30', INTERVAL 1 DAY)
)
INSERT INTO dim_date
SELECT
    CAST(strftime(day, '%Y%m%d') AS INTEGER),
    day,
    dayname(day),
    monthname(day),
    dayname(day) IN ('Saturday', 'Sunday')
FROM days;