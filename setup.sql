CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT, email TEXT, password_hash TEXT);

CREATE TABLE friendships (
    friend1_id INTEGER, friend2_id INTEGER);

CREATE TABLE goals (
    id SERIAL PRIMARY KEY, user_id INTEGER, goal TEXT, nudged_by TEXT);