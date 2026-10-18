-- Which countries have the most (total) posts? Average per user?
WITH country_users AS (
    SELECT country, COUNT(*) AS users
    FROM dim_user
    GROUP BY country
),
country_posts AS (
    SELECT u.country, COUNT(*) AS posts
    FROM fact_events f
    JOIN dim_user u 
        ON f.user_id = u.user_id
    JOIN dim_event_type t 
        ON f.event_type_key = t.event_type_key
    WHERE t.event_type = 'post'
    GROUP BY u.country
)
SELECT
    p.country,
    p.posts,
    c.users,
    ROUND(p.posts / c.users, 1) AS posts_per_user
FROM country_posts p
JOIN country_users c 
    ON p.country = c.country
ORDER BY posts_per_user DESC;
