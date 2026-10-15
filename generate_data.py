"""Generate a fake event log for a social app: 500 users over 60 days.

The events are saved as JSON Lines files (one JSON object per line),
one file per day, the way an app would send its log files to S3.
Users are saved to a separate file.

How to run from the project folder:
    python generate_data.py
"""
import json
import os
import random
from datetime import datetime, timedelta

random.seed(42)  # Using the same seed reproduces the same results later

NUM_USERS = 500
START = datetime(2026, 8, 1)
END = START + timedelta(days=60)  # ends at midnight on Sept 30, so Sept 29 is the last full day
COUNTRIES = ["US", "IN", "BR", "GB", "DE"]

users = []
events = []

for user_id in range(1, NUM_USERS + 1):
    signup = START + timedelta(days=random.randint(0, 59),
                               minutes=random.randint(0, 1439))
    users.append({"user_id": user_id,
                  "country": random.choice(COUNTRIES),
                  "signup_ts": signup})
    events.append({"user_id": user_id, "event_type": "signup", "event_ts": signup})

    # Each user opens the app between 5% and 60% on a given day
    p_active = random.uniform(0.05, 0.6)

    # Each day after signup has a random chance of the user opening the app
    day = signup + timedelta(days=1)
    while day < END:
        if random.random() < p_active:
            ts = day.replace(hour=random.randint(0, 23), minute=random.randint(0, 59))
            events.append({"user_id": user_id, "event_type": "app_open", "event_ts": ts})

            # 30% of users will create a post 5 minutes after opening (=5 for simplification)
            if random.random() < 0.3:
                events.append({"user_id": user_id, "event_type": "post",
                               "event_ts": ts + timedelta(minutes=5)})

        # Users' chance of opening the app drops 3% each day (lose interest)
        p_active *= 0.97
        day += timedelta(days=1)

# JSON can't store Python datetimes, so timestamps become text like "2026-08-01 14:05:00"
TS_FORMAT = "%Y-%m-%d %H:%M:%S"

# Write all users to one file
os.makedirs("data/users", exist_ok=True)
with open("data/users/users.jsonl", "w") as f:
    for user in users:
        row = {"user_id": user["user_id"],
               "country": user["country"],
               "signup_ts": user["signup_ts"].strftime(TS_FORMAT)}
        f.write(json.dumps(row) + "\n")

# Group the events by day, like daily log files
events_by_day = {}
for event in events:
    day = event["event_ts"].strftime("%Y-%m-%d")
    if day not in events_by_day:
        events_by_day[day] = []
    events_by_day[day].append(event)

# Write one file per day into a folder named dt=YYYY-MM-DD
for day, day_events in events_by_day.items():
    folder = f"data/events/dt={day}"
    os.makedirs(folder, exist_ok=True)
    with open(f"{folder}/events.jsonl", "w") as f:
        for event in day_events:
            row = {"user_id": event["user_id"],
                   "event_type": event["event_type"],
                   "event_ts": event["event_ts"].strftime(TS_FORMAT)}
            f.write(json.dumps(row) + "\n")

print(f"Generated {len(users)} users and {len(events)} events "
      f"across {len(events_by_day)} daily files")

