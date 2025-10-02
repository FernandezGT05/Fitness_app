from app.db_manager import get_connection
from app.repositories.users import add_user
from app.repositories.exercises import add_exercise
from app.repositories.workout_session import add_workout_session
from app.services.auth import login_user

user_data=login_user()

while True:
    if user_data[3] == "admin":
        print(f"----Admin: {user_data[4]}----")
        print("1.Add new user\n")
        print("2.Add new exercise\n")
        print("3.Exit")

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
    
    elif user_data[3]=="user":
        print(f"----User {user_data[4]}----")
        print("1.Log workout")
        print("2.Exit")

        choice=input("Enter your choice: ")
        if choice=="1":
            split=input("Enter the split(eg: arms/chest&triceps): ")
            add_workout_session(user_data[1],split)
        elif choice=="2":
            break

        
            
