def add_workout_set(cur,we_id,set_number,reps,weight=None):
    cur.execute("INSERT INTO workout_sets(we_id,set_number,reps,weight) VALUES(?,?,?,?)",
                (we_id,set_number,reps,weight,))