from db.db import get_connection


#получить список всех докторов кортежем
def get_all_doctors():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctors")
    doctors = cur.fetchall()
    conn.close()
    return doctors

#получаем айдишник доктора из таблицы докторы, используя айди пользователя, привязанный к доктору
def get_doctor_by_user_id(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM doctors WHERE user_id = ?",
        (user_id,)
    )
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


