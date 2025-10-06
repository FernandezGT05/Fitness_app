from ..db_manager import get_connection
from app.repositories.workout_sets import add_workout_set
from datetime import datetime
def add_workout_session(user_id,split_name):
    from app.repositories.workout_exercises import add_workout_exercise
    conn=get_connection()
    cur=conn.cursor()
    
    try:

        conn.execute("BEGIN")
        while True:
            date_str=input("Enter the session date (YYYY-MM-DD) or press Enter for today: ")
            if date_str.strip()=="":
                session_date=datetime.now().strftime('%Y-%m-%d')
                break
            else:
                try:
                    session_date=datetime.strptime(date_str,'%Y-%m-%d').strftime('%Y-%m-%d')
                    break
                except ValueError:
                    print("Invalid date format.Enter in YYYY-MM-DD format.")

        notes=input("Any notes for this session? (press enter to skip): ")
        
        cur.execute("INSERT INTO workout_session(user_id,date,split_name,notes) VALUES(?,?,?,?)",(user_id,session_date,split_name,notes))
        session_id=cur.lastrowid
        print("Session created successfully.\n")
            
        while True:
            cur.execute("SELECT exercise_id,exercise_name FROM exercises")
            exercises=cur.fetchall()
            for exercise in exercises:
                print(f"ID:{exercise[0]} - {exercise[1]}")
            try:
                exercise_id=int(input("Enter the exercise ID: ").strip())
                order=int(input("Enter the order in session: ").strip())
            except ValueError:
                print("Enter numeric values.")
                continue
            we_id=add_workout_exercise(cur,exercise_id,session_id,order)
            print("Exercise created.")

            while True:
                try:
                    set_amount = int(input("Number of sets: "))
                    break
                except ValueError:
                    print("Please enter a number for sets.")
            for set_number in range(1,set_amount+1):
                print("\n", end="")
                print(f"Set No.{set_number}")
                reps=input("Number of reps: ")
                weight=input("Weight used in kg (press enter to skip): ")
                add_workout_set(cur,we_id,set_number,reps,weight)
            print("\n", end="")
            new = input("Add another exercise? (y/n): ").strip().lower()
            if new != "y":
                break

        conn.commit()
        print("Workout logged successfully!")
    
    except Exception as e:
        conn.rollback()
        print("Workout not saved:", e)

    finally:
        conn.close()

def list_sessions(user_id):
    with get_connection() as conn:
        cur=conn.cursor()
        cur.execute("SELECT session_id,date,notes,split_name FROM workout_session WHERE user_id=?",(user_id,))
        session=cur.fetchall()

        if not session:
            print("No sessions found.")
            return
        sessions=[]
        for rows in  session:
            session_id,date,notes,split_name=rows
            print(f"|session {session_id}| --- |{split_name} day| --- |{date}|")
            sessions.append(session_id)
            if notes:
                print(f"Notes: {notes}")
        
        while True:
            num=input("Enter the session number to view (or press 'enter' to exit): ").strip()
            if num=="":
                return
            try:
                num=int(num)
                if num in sessions:
                    _print_session_details(cur,num)
                    break
                else:
                    print("Enter a valid session ID.")
            except ValueError:
                print("Enter a numeric value.")
                continue

def edit_workout_session(user_id,field_to_edit):
    with get_connection() as conn:
        cur=conn.cursor()
        
        cur.execute("SELECT session_id,date,notes,split_name FROM workout_session WHERE user_id=?",(user_id,))
        session=cur.fetchall()
        session_ids=[]
        for rows in  session:
            session_id,date,notes,split_name=rows
            print(f"|session {session_id}| --- |{split_name} day| --- |{date}|")
            session_ids.append(session_id)
            if notes:
                print(f"Notes: {notes}")
        while True:
            session_to_edit=input("Enter the session ID to edit :")
            
            if not session_to_edit:
                return
            
            try:
                session_to_edit=int(session_to_edit)
                if session_to_edit in session_ids:
                    break
                else:
                    print("Enter a valid session ID.")
            except ValueError:
                print("Enter a valid numeric session ID.")
                continue
            
        if field_to_edit!="date":
            new_field_value=input(f"Enter the new {field_to_edit} :")
            query=f"UPDATE workout_session SET {field_to_edit}=? WHERE session_id=?"
            cur.execute(query,(new_field_value,session_to_edit))
        elif field_to_edit=="date":
            while True:
                new_date=input("Enter the new Date (YYYY-MM-DD): ")
                if new_date.strip()=="":
                    return
                try:
                    session_date=datetime.strptime(new_date,'%Y-%m-%d').strftime('%Y-%m-%d')
                    cur.execute("UPDATE workout_session SET date=? WHERE session_id=?",(session_date,session_to_edit))
                    break
                except ValueError:
                    print("Invalid date format.Enter in YYYY-MM-DD format.")

def _print_session_details(cur,session_to_edit):
        cur.execute("SELECT we_id,exercise_id,order_in_session FROM workout_exercises WHERE session_id=? ORDER BY order_in_session ASC",(session_to_edit,))
        sesh=cur.fetchall()
        for row in sesh:
            we_id,exercise_id,order_in_session=row
            cur.execute("SELECT exercise_name FROM exercises WHERE exercise_id=?",(exercise_id,))
            exercise_name=cur.fetchone()
            cur.execute("SELECT set_number,reps,weight FROM workout_sets WHERE we_id=? ORDER BY set_number ASC",(we_id,))
            set_info=cur.fetchall()
            print(f"         {order_in_session}. |--- {exercise_name[0]} ---|")
            for set_row in set_info:
                set_number,reps,weight=set_row
                print(f"              - |Set {set_number}| - |{weight}kg| - |{reps} reps|")
