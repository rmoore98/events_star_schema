-- fact_events: one row for each event, linked to the dimension tables
CREATE OR REPLACE TABLE fact_events (
    user_id        INTEGER,
    event_type_key INTEGER,
    date_key       INTEGER,
    event_ts       TIMESTAMP
);

WITH raw_events AS (
    SELECT user_id, event_type, CAST(event_ts AS TIMESTAMP) AS event_ts
    FROM read_json_auto('data/events/*/events.jsonl')
)
INSERT INTO fact_events
SELECT
    r.user_id,
    t.event_type_key,
    CAST(strftime(r.event_ts, '%Y%m%d') AS INTEGER),
    r.event_ts
FROM raw_events r
JOIN dim_event_type t 
ON r.event_type = t.event_type;