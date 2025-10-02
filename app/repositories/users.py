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
