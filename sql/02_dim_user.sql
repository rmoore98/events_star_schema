-- dim_user: one row for each user
CREATE OR REPLACE TABLE dim_user (
    user_id   INTEGER PRIMARY KEY,
    country   VARCHAR,
    signup_ts TIMESTAMP
);

INSERT INTO dim_user
SELECT user_id, country, CAST(signup_ts AS TIMESTAMP)
FROM read_json_auto('data/users/users.jsonl');