-- How many different users opened the app each month?
SELECT 
    d.month_name, 
    COUNT(DISTINCT f.user_id) AS active_users
FROM fact_events f
JOIN dim_date d 
    ON f.date_key = d.date_key
JOIN dim_event_type t 
    ON f.event_type_key = t.event_type_key
WHERE t.event_type = 'app_open'
GROUP BY d.month_name
ORDER BY d.month_name;