-- dim_event_type: one row for each kind of event
CREATE OR REPLACE TABLE dim_event_type (
    event_type_key INTEGER PRIMARY KEY,
    event_type     VARCHAR,
    description    VARCHAR
);

INSERT INTO dim_event_type VALUES
    (1, 'signup',   'User created an account'),
    (2, 'app_open', 'User opened the app'),
    (3, 'post',     'User created a post');