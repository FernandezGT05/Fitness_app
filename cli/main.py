from app.db_manager import get_connection
from app.repositories.users import add_user,del_user,edit_user_info
from app.repositories.exercises import add_exercise,edit_exercise,del_exercise
from app.repositories.workout_session import add_workout_session,list_sessions,edit_workout_session
from app.repositories.workout_exercises import edit_workout_exercise
from app.repositories.workout_sets import edit_set_info
from app.services.auth import login_user

user_data=login_user()

while True:
    if user_data[3] == "admin":
        print(f"----Admin: {user_data[4]}----")
        print("1.Add new user")
        print("2.Add new exercise")
        print("3.Exit")
        print("4.Delete a user")
        print("5.Edit user information")
        print("6.Delete an exercise")
        print("7.Edit an exercise")
        print("8.List sessions")

        choice=input("Enter your choice: ")
        if choice=="1":
            name=input("Enter the name:")
            while True:
                username=input("Enter the username: ")
                conn=get_connection()
                try:
                    cur=conn.cursor()
                    cur.execute("SELECT username FROM users WHERE username=?",(username,))
                    check=cur.fetchone()
                    if not check:
                        break
                    else:
                        print("username already taken.")
                finally:
                    conn.close()
            new_password=input("Enter the password: ")
            while True:
                role=input("Enter the role (admin/user): ").lower().strip()
                if role=="admin" or role=="user":
                    break
                else:
                    print("Invalid role.Try again.")
            height=int(input("Enter the height(in cm): "))
            weight=float(input("Enter the weight(in kg): "))
            age=int(input("Enter the age: "))
            add_user(name,username,new_password,role,height,weight,age)
            print(f"User '{name}' added successfully.")
        
        elif choice=="2":
            exercise_name=input("Exercise name: ")
            muscle_group=input("Muscle group: ")
            description=input("Description(press enter if none): ")
            add_exercise(exercise_name,muscle_group,description)
            print(f"Exercise '{exercise_name}' added successfully.")

        elif choice=="3":
            break
        elif choice=="4":
            try:
                user_id=int(input("Enter the user ID to delete: "))
                del_user(user_id)
            except ValueError:
                print("Invalid Input. Enter a numeric ID.")
        
        elif choice=="5":
            change_info=input("Whose information do you need to change?(user ID) :")
            edit_user_info(change_info,logged_role="admin")

        elif choice=="6":
            exercise=input("Enter the exercise ID to delete: ")
            del_exercise(exercise)

        elif choice=="7":
            exercise=input("Enter the exercise ID to edit: ")
            edit_exercise(exercise)
        
        elif choice=="8":
            list_sessions(user_data[1])


    elif user_data[3]=="user":
        print(f"----User: {user_data[4]}, ID: {user_data[1]}----")
        print("1.Log workout")
        print("2.Exit")
        print("3.Edit your info")
        print("4.List sessions")
        print("5.Edit workout")

        choice=input("Enter your choice: ")
        if choice=="1":
            split=input("Enter the split(eg: arms/chest&triceps): ")
            add_workout_session(user_data[1],split)
        elif choice=="2":
            break
        elif choice=="3":
            edit_user_info(user_data[1])
        elif choice=="4":
            list_sessions(user_data[1])
        elif choice=="5":
            print("\n---Fields---",end="")
            print("1.Date")
            print("2.Notes")
            print("3.Split name")
            print("4.Exercise")
            print("5.Exercise order")
            print("6.Reps")
            print("7.Weight")
            while True:
                field_to_edit=input("Enter the field to edit: ")
                
                try:
                    field_to_edit=int(field_to_edit)
                    break
                except ValueError:
                    print("Enter a valid numeric value.")
            if field_to_edit<1 or field_to_edit>8:
                    print("Enter a valid number.")
                    
            if field_to_edit==1 :
                edit_workout_session(user_data[1],"date")
            elif field_to_edit==2:
                edit_workout_session(user_data[1],"notes")
            elif field_to_edit==3:
                edit_workout_session(user_data[1],"split_name")
            elif field_to_edit==4:
                edit_workout_exercise(user_data[1],"exercise_id")
            elif field_to_edit==5:
                edit_workout_exercise(user_data[1],"order_in_session")
            elif field_to_edit==6:
                edit_set_info(user_data[1],"reps")
            elif field_to_edit==7:
                edit_set_info(user_data[1],"weight")
                


        
            
