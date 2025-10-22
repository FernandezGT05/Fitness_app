from ..db_manager import get_connection

def add_exercise(exercise_name, muscle_group, description=None):
    with get_connection() as conn:
        cur=conn.cursor()

        cur.execute("INSERT INTO exercises(exercise_name,muscle_group,description) VALUES(?,?,?)",(exercise_name,muscle_group,description))
    
def edit_exercise(exercise_id):
    with get_connection() as conn:
        cur=conn.cursor()

        exercises=['exercise_name','description','muscle_group']
        cur.execute("SELECT exercise_name,description,muscle_group FROM exercises WHERE exercise_id=?",(exercise_id,))

        for x,exercises in enumerate(exercises,start=1):
            print(f"{x}.{exercises[x-1]}")
        
        while True:
            try:
                choice=int(input("Enter the field you want to edit(1-3): "))
                if choice<1 and choice>3:
                    print("Invalid choice.Enter a number between 1-3.")
                    continue
                elif choice>=1 and choice<=3:
                    break
            except ValueError:
                print(f"Invalid input. Enter a number(1-3)")
        
        field_to_edit=exercises[choice-1]
        edit=input(f"Enter the new {field_to_edit} :")
        
        query=f"UPDATE exercises SET {field_to_edit}=? WHERE exercise_id=?"
        cur.execute(query,(edit,exercise_id))
        print("Exercise successfully edited.")

def del_exercise(exercises_id):
    with get_connection() as conn:
        cur=conn.cursor()

        confirmation=input("Are you sure?(y/n): ").lower().strip()
        if confirmation=="y":
            cur.execute("DELETE FROM exercises WHERE exercise_id=?",(exercises_id,))
            print("Exercise deleted successfully.")
        else:
            print("Exercise was not deleted.")
            return
