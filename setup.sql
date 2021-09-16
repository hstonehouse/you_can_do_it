CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name TEXT, email TEXT, password_hash TEXT);

CREATE TABLE friendships (
    friend1_id INTEGER, 
    friend2_id INTEGER,
    PRIMARY KEY (friend1_id, friend2_id),
    CONSTRAINT fk_friendships_friend1_id
        FOREIGN KEY(friend1_id)
        REFERENCES users(id),
    CONSTRAINT fk_friendships_friend2_id
        FOREIGN KEY(friend2_id)
        REFERENCES users(id)
    );

CREATE TABLE goals (
    id SERIAL PRIMARY KEY, 
    user_id INTEGER, 
    goal TEXT, 
    nudged_by INTEGER,
    CONSTRAINT fk_goals_user_id
        FOREIGN KEY(user_id)
        REFERENCES users(id),
    CONSTRAINT fk_goals_nudged_by
        FOREIGN KEY(nudged_by)
        REFERENCES users(id)
    );