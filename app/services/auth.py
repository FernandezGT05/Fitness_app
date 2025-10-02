import bcrypt
from app.db_manager import get_connection

def login_user():
    conn = get_connection()
    cur = conn.cursor()

    while True:
        print("----Personal Fitness Tracker----\n")
        username = input("Enter the username: ")
        cur.execute("SELECT username,user_id,password_hash,role,name FROM users WHERE username=?",(username,))
        user_data = cur.fetchone()

        if not user_data:
            print("Invalid username")
            continue

        # Username exists, now check password
        while True:
            password = input("Enter the password: ")
            stored_hash = user_data[2]
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                print(f"Successfully logged in {user_data[4]} ({user_data[3]})")
                conn.close()
                return user_data  # <-- return the logged-in user data
            else:
                print("Invalid password")
