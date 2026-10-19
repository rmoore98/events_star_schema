# Events Star Schema

Turns raw app event logs (JSON Lines) into a star schema in DuckDB, then answers analysis questions with simple joins.

## Why a star schema

App data is generally stored in a normalized database. These databases are designed for record-keeping, not for answering business-oriented analysis questions. Dimensional modeling reshapes the data into a fact table focusing on the event – what happened – and multiple dimension tables that focus on the event’s descriptions – the who, when, and what kind. Some information is redundant on purpose. For example, each row in the `dim_date` table stores the day name and a weekend flag. This information can be worked out from the table’s `full_date` column, but queries are simpler and run quicker when the information is precalculated into the table rather than calculated with each query. 

## Schema

```
                 dim_user
                    |
dim_event_type -- fact_events -- dim_date
```

| Table | One row per | Key |
|---|---|---|
| `fact_events` | event | links to the dimensions through `user_id`, `event_type_key`, `date_key` |
| `dim_user` | user | `user_id` |
| `dim_date` | calendar day, Aug 1 – Sep 30, 2026 | `date_key` (YYYYMMDD, e.g. 20260801) |
| `dim_event_type` | event type (signup, app_open, post) | `event_type_key` |

The date range runs through September 30 because a few posts made late on September 29 have timestamps just after midnight.

## Project structure

```
generate_data.py     creates fake event logs as daily JSON Lines files
build.py             runs the SQL files in sql/ in order and prints row counts
run_queries.py       runs the analysis queries in queries/ and prints results
sql/                 one file per table (dimensions first, fact table last)
queries/             analysis questions answered with the star schema
```

## How to run

```
python -m pip install -r requirements.txt
python generate_data.py
python build.py
python run_queries.py
```

## Data checks

`build.py` prints the row count of every table after each build. The `fact_events` count should equal the total number of events `generate_data.py` creates.

This check matters because the fact table is built with an inner join to `dim_event_type`. If an event had a type missing from the dimension, the join would drop it without any error, and the row count is what would catch it.

## Findings

The data is randomly generated, so these results show the method rather than real user behavior.

- **Posts by country:** posts per user ranges from 1.6 to 1.8, so countries are about the same. Germany has the most total posts (189), but also the most users (105). Comparing per user keeps larger countries from looking more active just because they're larger.
- **Weekend vs. weekday:** average events per day are nearly identical (for example, 47.8 app opens per weekend day vs. 47.1 per weekday). I used daily averages because there are more weekdays than weekend days, so raw totals would always favor weekdays.
- **Active users by month:** September has 432 active users compared with 197 in August. This isn't rising engagement. Signups are spread across the 60 days, so more users exist by September, and each user's activity declines over time.

## Next steps

- Load the tables into AWS (Athena or Redshift), connecting this project to my [aws-events-pipeline](https://github.com/rmoore98/aws-events-pipeline) repo
- Add data quality checks beyond row counts, such as confirming every key in `fact_events` matches a dimension row
- Build a simple dashboard on top of the query results