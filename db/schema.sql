PRAGMA foreign_keys = ON;

CREATE TABLE if not exists users(
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user',
    height INTEGER,
    weight INTEGER,
    age INTEGER NOT NULL
); 

CREATE TABLE if not exists exercises(
    exercise_id INTEGER PRIMARY KEY AUTOINCREMENT,
    exercise_name TEXT NOT NULL,
    description TEXT,
    muscle_group TEXT NOT NULL
);

CREATE TABLE if not exists workout_session(
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    notes TEXT,
    split_name TEXT NOT NULL,
    FOREIGN KEY (user_id)REFERENCES users(user_id)
        ON DELETE CASCADE
);

CREATE TABLE if not exists workout_exercises(
    we_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL,
    exercise_id INTEGER NOT NULL,
    order_in_session INTEGER,
    FOREIGN KEY (session_id) REFERENCES workout_session(session_id)
        ON DELETE CASCADE,
    FOREIGN KEY (exercise_id) REFERENCES exercises(exercise_id)
        ON DELETE CASCADE
);

CREATE TABLE if not exists workout_sets(
    set_id INTEGER PRIMARY KEY AUTOINCREMENT,
    we_id INTEGER NOT NULL,
    set_number INTEGER NOT NULL,
    reps INTEGER NOT NULL,
    weight INTEGER,
    FOREIGN KEY (we_id) REFERENCES workout_exercises(we_id)
        ON DELETE CASCADE
);