from ..db_manager import get_connection
import bcrypt

def add_user(name,username,password,role,height,weight,age):
    conn=get_connection()
    cur=conn.cursor()

    plain_password = password.encode('utf-8')
    hashed_password=bcrypt.hashpw(plain_password,bcrypt.gensalt())

    cur.execute("INSERT INTO users(name,username,password_hash,role,height,weight,age) VALUES(?,?,?,?,?,?,?)",(name,username,hashed_password.decode("utf-8"),role,height,weight,age))
    conn.commit()
    conn.close()

def del_user(user_id):
    with get_connection() as conn:
        cur=conn.cursor()

        cur.execute("SELECT name,user_id,role FROM users WHERE user_id=?",(user_id,))
        user=cur.fetchone()
        if not user:
            print(f"User with id: {user_id} was not found.")
            return
        if user[2]=="admin":
            sure=input("Do you really want to delete an admin?(y/n) :").lower().strip()
            if sure=="y":
                cur.execute("DELETE FROM users WHERE user_id=?",(user_id,))
                print("Admin successfully deleted.")
                return
            else:
                print("Admin was not deleted.")
                return
        confirmation=input("Are you sure you want to delete this user? (y/n): ").lower().strip()
        if confirmation=="y":
            cur.execute("DELETE FROM users WHERE user_id=?",(user_id,))
            print("User successfully deleted.")
        else:
            print("User was not deleted.")

def edit_user_info(user_id,logged_role=None):
    with get_connection() as conn:
        cur=conn.cursor()
        cur.execute("SELECT name,username,password_hash,role,height,weight,age FROM users WHERE user_id=?",(user_id,))
        user_info=cur.fetchone()
        fields = ["name", "username", "password_hash", "role", "height", "weight", "age"]
        if not user_info:
            print("User not found.")
            return
            
        for x,user in enumerate(fields,start=1):
            print(f"{x}.{user} : {user_info[x-1]}")
            
        while True:
            try:
                edit=int(input("Enter the number you want to edit(1-7): ").strip())
                if edit<1 or edit>len(fields):
                    print("Invalid choice.Try again.")
                    continue
                elif edit>0 and edit<=len(fields):
                    break
            except ValueError :
                print("Enter a valid number")

        field_to_edit=fields[edit-1]
        
        if field_to_edit=='role' and logged_role!="admin":
            print("A user cannot change the role.")
            return
        
        if field_to_edit!="password_hash":
            while True:
                new=input(f"Enter the new value for {field_to_edit}: ")
                if field_to_edit=="role":
                    if new not in('admin','user'):
                        print("Invalid role.Enter 'admin' or 'user'.")
                        continue
                if field_to_edit=="username":
                    cur.execute("SELECT username FROM users WHERE username=?",(new,))
                    result=cur.fetchone()
                    if result:
                        print("Username already taken.Try again.")
                        continue
                    else:
                        cur.execute("UPDATE users SET username=? WHERE user_id=?",(new,user_id))
                        conn.commit()
                        break
                else:
                    query=f"UPDATE users SET {field_to_edit}=? WHERE user_id=?"
                    cur.execute(query,(new,user_id))
                    print(f"New {field_to_edit} saved.")
                    conn.commit()
                    break
        else:
            while True:
                new_pass=input("Enter the new password: ")
                confirmation=input("Are you sure? (y/n): ").lower().strip()
                if bcrypt.checkpw(new_pass.encode("utf-8"), user_info[2].encode("utf-8")):
                    print("New password cannot be the same as the old password. Try again.")
                    continue
                
                new_hashed_pass=bcrypt.hashpw(new_pass.encode('utf-8'),bcrypt.gensalt())
                if confirmation!="y":
                    return
                else:
                    cur.execute("UPDATE users SET password_hash=? WHERE user_id=?",(new_hashed_pass.decode('utf-8'),user_id))
                    break
    

