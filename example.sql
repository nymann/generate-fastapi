CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE TABLE tlog_entries (
    identifier UUID DEFAULT uuid_generate_v4(),
    ts TIMESTAMP WITH TIME ZONE NOT NULL,
    day DATE,
    operator_name VARCHAR(512),
    operator_station_name VARCHAR(512),
    subsystem VARCHAR(512),
    element_type VARCHAR(512),
    element_name VARCHAR(512),
    tlog TEXT,
    PRIMARY KEY (identifier,ts),
    UNIQUE (ts,day,operator_name,operator_station_name,subsystem,element_type,element_name,tlog)
) PARTITION BY RANGE (ts);
-- Create indexes on all collumns, since insert time is irrelevant
CREATE INDEX tlog_entries_ts_idx ON tlog_entries USING btree (ts);
CREATE INDEX tlog_entries_day_idx ON tlog_entries USING btree (day);
CREATE INDEX tlog_entries_operator_name_idx ON tlog_entries USING btree (operator_name);
CREATE INDEX tlog_entries_operator_station_name_idx ON tlog_entries USING btree (operator_station_name);
CREATE INDEX tlog_entries_subsystem ON tlog_entries USING btree (subsystem);
CREATE INDEX tlog_entries_element_type ON tlog_entries USING btree (element_type);
CREATE INDEX tlog_entries_element_name ON tlog_entries USING btree (element_name);
CREATE INDEX tlog_entries_tlog ON tlog_entries USING btree (tlog);
-- Fail safe table if client tries to insert with a 'ts' that doesn't match a
-- partition.
CREATE TABLE tlog_entries_default PARTITION OF tlog_entries DEFAULT;

-- Creates partitions for the next 50 years.
CREATE OR REPLACE FUNCTION create_partitions(
    from_year INTEGER,
    to_year INTEGER
)
RETURNS VOID AS $$
BEGIN
    FOR year IN from_year..to_year LOOP
        EXECUTE format(E'CREATE TABLE tlog_entries_%s PARTITION OF tlog_entries FOR VALUES FROM (''%s-01-01'') TO (''%s-01-01'');', year, year, year + 1);
    END LOOP;
END;
$$ LANGUAGE plpgsql;
-- Run the function
SELECT create_partitions(2020, 2120);
-- Copy over data from AKTV table to the new one.
-- Run this inside a transaction so we don't lose data in case it fails.
BEGIN TRANSACTION;
INSERT INTO tlog_entries(ts, day, operator_name, operator_station_name, subsystem, element_type, element_name, tlog)
SELECT ts, day, operator_name, operator_station_name, subsystem, element_type, element_name, tlog
FROM aktv;
-- configuration, so that we can remove those too instead of doing CASCADE.
DROP TABLE aktv CASCADE;
COMMIT TRANSACTION;
