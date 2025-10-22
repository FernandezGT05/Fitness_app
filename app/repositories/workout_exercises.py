from ..db_manager import get_connection

def add_workout_exercise(cur,exercise_id,session_id,order_in_session):
    cur.execute("INSERT INTO workout_exercises(exercise_id,session_id,order_in_session) VALUES(?,?,?)",
                (exercise_id,session_id,order_in_session))
    we_id=cur.lastrowid
    return we_id

def edit_workout_exercise(user_id,field_to_edit):
    from .workout_session import _print_session_details
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
            session_to_edit=input("Enter the session to edit: ")
            try:
                session_to_edit=int(session_to_edit)
                if session_to_edit in session_ids:
                    break
                else:
                    print("Invalid session ID")
            except ValueError:
                print("Enter a valid numeric value.")
    
        _print_session_details(cur,session_to_edit)

        if field_to_edit=="exercise_id":
            while True:
                select_exercise=input("Enter the order number of the exercise to replace: ")
                try:
                    select_exercise=int(select_exercise)
                    break
                except ValueError:
                    print("Enter a valid numeric value.")
            cur.execute("SELECT we_id FROM workout_exercises WHERE order_in_session=? AND session_id=?",(select_exercise,session_to_edit))
            exercise_row=cur.fetchone()
            if not exercise_row:
                print("No exercise found with that order number in this session.")
                return
            we_id=exercise_row[0]
            cur.execute("SELECT exercise_id,exercise_name FROM exercises")
            exercises=cur.fetchall()
            exercise_ids=[]
            for exercise in exercises:
                exercise_id,exercise_name=exercise
                print(f"ID:{exercise_id} - {exercise_name}")
                exercise_ids.append(exercise_id)
            
            while True:
                new_exercise=input("Enter the new exercise ID: ")
                try:
                    new_exercise=int(new_exercise)
                    if new_exercise in exercise_ids:
                        break
                    else:
                        print("Enter a valid exercise ID.")
                except ValueError:
                    print("Enter a valid numerical value.")
            
            cur.execute("UPDATE workout_exercises SET exercise_id=? WHERE we_id=?",(new_exercise,we_id))
            print("Exercise successfully edited.")
            _print_session_details(cur,session_to_edit)
        
        elif field_to_edit=="order_in_session":
            while True:
                try:
                    select_order=input("Enter the order number to change: ")
                    select_order=int(select_order)
                    
                    cur.execute("SELECT order_in_session,we_id FROM workout_exercises WHERE session_id=?",(session_to_edit,))
                    orders={order_num:we_id for order_num,we_id in cur.fetchall()}
                    
                    if select_order not in orders:
                        print("Invalid order number.Try again.")
                        continue
                    
                    new_order_number=int(input("Enter a new order number: "))
                    
                    if new_order_number==select_order:
                        print("New order number cannot be the same as the last order number.")
                    
                    if new_order_number in orders:
                        cur.execute("UPDATE workout_exercises SET order_in_session=? WHERE we_id=?",(select_order,orders[new_order_number]))
                        cur.execute("UPDATE workout_exercises SET order_in_session=? WHERE we_id=?",(new_order_number,orders[select_order]))
                        print(f"Swapped order {select_order} with {new_order_number}.")
                    
                    else:
                        cur.execute("UPDATE workout_exercises SET order_in_session=? WHERE we_id=?",(new_order_number,orders[select_order]))
                        print(f"Changed order {select_order} ---> {new_order_number}")
                    
                    _print_session_details(cur,session_to_edit)
                    break

                except ValueError:
                    print("Enter a valid numeric value.")
            
def add_exercise_to_session(user_id):
    from .workout_sets import add_workout_set
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
            try:
                session_to_add=input("Enter the session ID to add an exercise: ")
                session_to_add=int(session_to_add)
                if session_to_add in session_ids:
                    break
                else:
                    print("Invalid session ID")
            except ValueError:
                print("Enter a valid numeric value.")

        cur.execute("SELECT exercise_id,exercise_name,muscle_group FROM exercises")
        exercise=cur.fetchall()
        exercises=[]
        for row in exercise:
            exercise_id,exercise_name,muscle_group=row
            print(f"{exercise_id}. {exercise_name} ---- {muscle_group}")
            exercises.append(exercise_id)
        
        while True:
            try:
                selected_exercise=input("Enter an exercise to add: ").strip()
                order=int(input("Enter the order in session: ").strip())
                selected_exercise=int(selected_exercise)
                if selected_exercise in exercises:
                    break
                else:
                    print("Invalid exercise.")
            except ValueError:
                print("Enter a valid numeric value.")
        
        we_id=add_workout_exercise(cur,selected_exercise,session_to_add,order)
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
        print("Exercise logged successfully!")

def delete_exercise(user_id):
    from .workout_session import _print_session_details
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
            try:
                session_to_edit=input("Enter the session ID to delete an exercise: ")
                session_to_edit=int(session_to_edit)
                if session_to_edit in session_ids:
                    break
                else:
                    print("Invalid session ID")
            except ValueError:
                print("Enter a valid numeric value.")
        
        _print_session_details(cur,session_to_edit)

        cur.execute("SELECT order_in_session FROM workout_exercises WHERE session_id=?",(session_to_edit,))
        order=[row[0] for row in cur.fetchall()]
        while True:
            exercise_to_del=input("Enter the exercise order number to delete an exercise: ").strip()
            try:
                exercise_to_del=int(exercise_to_del)
                if exercise_to_del in order:
                    break
                else:
                    print("Enter a valid exercise order number.")
            except ValueError:
                print("Enter a valid numeric value.")
        
        cur.execute("DELETE FROM workout_exercises WHERE order_in_session=?",(exercise_to_del,))
        print("Exercise successfully deleted.")