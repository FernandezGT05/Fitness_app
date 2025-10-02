def add_workout_exercise(cur,exercise_id,session_id,order_in_session):
    cur.execute("INSERT INTO workout_exercises(exercise_id,session_id,order_in_session) VALUES(?,?,?)",
                (exercise_id,session_id,order_in_session))
    we_id=cur.lastrowid
    return we_id