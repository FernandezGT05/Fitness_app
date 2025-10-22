from ..db_manager import get_connection

def add_workout_set(cur,we_id,set_number,reps,weight=None):
    cur.execute("INSERT INTO workout_sets(we_id,set_number,reps,weight) VALUES(?,?,?,?)",
                (we_id,set_number,reps,weight,))

def edit_set_info(user_id,field_to_edit):
    from .workout_session import _print_session_details
    
    with get_connection() as conn:
        cur=conn.cursor()
        # Display the sessions and get the session to edit.
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
                session_to_edit=input("Enter the session to edit: ")
                session_to_edit=int(session_to_edit)
                if session_to_edit in session_ids:
                    break
                else:
                    print("Invalid session ID")
                    continue
            except ValueError:
                print("Enter a valid numeric value.")
                continue
        # print session details
        _print_session_details(cur,session_to_edit)

        while True:
            try:
                exercise_to_edit=int(input("Enter the order number which contains the set to edit: "))
                
                cur.execute("SELECT we_id,order_in_session FROM workout_exercises WHERE session_id=?",(session_to_edit,))
                orders={order_in_session:we_id for we_id,order_in_session in cur.fetchall()}

                if exercise_to_edit not in orders:
                    print("Enter an order number within the session.")
                    continue
                we_id=orders[exercise_to_edit]
                break
            except ValueError:
                print("Enter a valid numeric value.")
                continue
        # Display the selected exercise and its sets.
        cur.execute("SELECT exercise_id FROM workout_exercises WHERE order_in_session=?",(exercise_to_edit,))
        exercise_id=cur.fetchone()[0]
        cur.execute("SELECT exercise_name FROM exercises WHERE exercise_id=?",(exercise_id,))
        exercise_name=cur.fetchone()[0]
        print(f"         {exercise_to_edit}. |--- {exercise_name} ---|")
        
        cur.execute("SELECT set_number,reps,weight FROM workout_sets WHERE we_id=? ORDER BY set_number ASC",(we_id,))
        set_info=cur.fetchall()
        set_numbers=[]
        for set_row in set_info:
                set_number,reps,weight=set_row
                set_numbers.append(set_number)
                print(f"              - |Set {set_number}| - |{weight}kg| - |{reps} reps|")
        
        while True:
            try:
                set_to_edit=int(input("Enter the set number to edit: "))
                
                if set_to_edit not in set_numbers:
                    print("Set number not found.Enter a valid set number.")
                    continue
                break
            except ValueError:
                print("Enter a valid numeric value.")
                continue
        
        if field_to_edit=="weight":
            while True:
                try:    
                    new_weight=int(input("Enter the new weight (kg) : "))
                    if new_weight<0:
                        print("Weight cannot be negative.Try again.")
                        continue
                    cur.execute("UPDATE workout_sets SET weight=? WHERE we_id=? AND set_number=?",(new_weight,we_id,set_to_edit))
                    _print_session_details(cur,session_to_edit)
                    break
                except ValueError:
                    print("Enter a neumeric value.")
                    continue
        elif field_to_edit=="reps":
            while True:
                try:    
                    new_reps=int(input("Enter the new reps: "))
                    if new_reps<0:
                        print("Reps cannot be negative.Try again.")
                        continue
                    cur.execute("UPDATE workout_sets SET reps=? WHERE we_id=? AND set_number=?",(new_reps,we_id,set_to_edit))
                    _print_session_details(cur,session_to_edit)
                    break
                except ValueError:
                    print("Enter a neumeric value.")
                    continue

def add_set_to_exercise(user_id):
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
                session_to_add=input("Enter the session ID to add a set: ")
                session_to_add=int(session_to_add)
                if session_to_add in session_ids:
                    break
                else:
                    print("Invalid session ID")
            except ValueError:
                print("Enter a valid numeric value.")
        _print_session_details(cur,session_to_add)

        while True:
            exercise_to_add=input("enter the exercise number to add a set: ").strip()
            try:
                exercise_to_add=int(exercise_to_add)
                break
            except ValueError:
                print("Enter a valid numeric value.")
        cur.execute("SELECT we_id FROM workout_exercises WHERE order_in_session=? AND session_id=?",(exercise_to_add,session_to_add))
        exercise_row=cur.fetchone()
        if not exercise_row:
            print("No exercise found with that order number in this session.")
            return
        
        we_id=exercise_row[0]
        cur.execute("SELECT set_number FROM workout_sets WHERE we_id=?",(we_id,))
        sets=cur.fetchall()
        all_sets=[]
        for row in sets:
            set_num=row
            all_sets.append(set_num)

        set_number=len(all_sets)+1
        print("\n", end="")
        print(f"Set No.{set_number}")
        reps=input("Number of reps: ")
        weight=input("Weight used in kg (press enter to skip): ")
        add_workout_set(cur,we_id,set_number,reps,weight)
                    
def del_set(user_id):
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
                session_to_edit=input("Enter the session ID to delete a set: ")
                session_to_edit=int(session_to_edit)
                if session_to_edit in session_ids:
                    break
                else:
                    print("Invalid session ID")
            except ValueError:
                print("Enter a valid numeric value.")
        
        _print_session_details(cur,session_to_edit)

        while True:
            try:
                select_order=input("Enter the order number of the set to delete: ")
                select_order=int(select_order)
                
                cur.execute("SELECT order_in_session,we_id FROM workout_exercises WHERE session_id=?",(session_to_edit,))
                orders={order_num:we_id for order_num,we_id in cur.fetchall()}
                
                if select_order not in orders:
                    print("Invalid order number.Try again.")
                    continue
                break
            except ValueError:
                    print("Enter a valid numeric value.")

        cur.execute("SELECT we_id FROM workout_exercises WHERE order_in_session=? AND session_id=?",(select_order,session_to_edit))
        we_id=cur.fetchone()[0]
        cur.execute("SELECT set_number FROM workout_sets WHERE we_id=?",(we_id,))
        sets=[row[0] for row in cur.fetchall()]

        while True:
            set_to_del=input("Enter the set number to delete: ").strip()
            try:
                set_to_del=int(set_to_del)
                if set_to_del in sets:
                    break
                else:
                    print("Enter a valid set number.")
            except ValueError:
                print("Enter a valid numeric value.")
        
        cur.execute("DELETE FROM workout_sets WHERE set_number=? AND we_id=?",(set_to_del,we_id))
        print("Set successfully deleted.")
        # Re order set numbers after deletion
        cur.execute("SELECT set_number FROM workout_sets WHERE we_id=? ORDER BY set_number", (we_id,))
        remaining = [r[0] for r in cur.fetchall()]
        for i, old_num in enumerate(remaining, start=1):
            cur.execute("UPDATE workout_sets SET set_number=? WHERE we_id=? AND set_number=?", (i, we_id, old_num))

