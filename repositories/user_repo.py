from db.db import get_connection

def create_user(email, password_hash, role):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)",
        (email, password_hash, role)
    )
    conn.commit()
    conn.close()

def get_user_by_email(email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cur.fetchone()
    conn.close()
    return user
