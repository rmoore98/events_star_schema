-- Are users more active on weekdays or weekends? (average events per day)
SELECT
    d.is_weekend,
    t.event_type,
    ROUND(COUNT(*) / COUNT(DISTINCT d.date_key), 1) AS avg_events_per_day
FROM fact_events f
JOIN dim_date d 
    ON f.date_key = d.date_key
JOIN dim_event_type t 
    ON f.event_type_key = t.event_type_key
GROUP BY d.is_weekend, t.event_type
ORDER BY t.event_type, d.is_weekend;