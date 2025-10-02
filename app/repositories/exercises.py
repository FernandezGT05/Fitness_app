from ..db_manager import get_connection

def add_exercise(exercise_name, muscle_group, description=None):
    conn=get_connection()
    cur=conn.cursor()

    cur.execute("INSERT INTO exercises(exercise_name,muscle_group,description) VALUES(?,?,?)",(exercise_name,muscle_group,description))
    conn.commit()
    conn.close()

