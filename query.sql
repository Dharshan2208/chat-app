-- Execute these queries in the SQL Shell in the CockroachDB to create
-- table for users and messages

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username STRING UNIQUE NOT NULL,
    password STRING NOT NULL
);

CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sender_id UUID REFERENCES users(id),
    content STRING NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);
