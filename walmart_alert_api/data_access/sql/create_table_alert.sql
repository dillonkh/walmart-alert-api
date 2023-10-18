CREATE TABLE alert(
   alert_id TEXT PRIMARY KEY NOT NULL,
   service_id TEXT NOT NULL,
   service_name TEXT,
   model TEXT,
   alert_type TEXT,
   alert_ts INT,
   severity TEXT,
   team_slack TEXT
);
