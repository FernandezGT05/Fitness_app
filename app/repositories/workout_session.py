from ..db_manager import get_connection
from app.repositories.workout_exercises import add_workout_exercise
from app.repositories.workout_sets import add_workout_set
from datetime import datetime
def add_workout_session(user_id,split_name):
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
            exercise_id=int(input("Enter the exercise ID: "))
            order=int(input("Enter the order in session: "))
            we_id=add_workout_exercise(cur,exercise_id,session_id,order)
            print("Exercise created.")

            set_amount=int(input("Number of sets: "))
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
