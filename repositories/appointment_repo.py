from db.db import get_connection
from datetime import datetime, timedelta
import sqlite3


#пытаемся реализовать логику приёма врачей, конкретно эта функция предназначена для предотвращения записей на одно время, а также 30 мин за и после записи
def is_time_slot_available(doctor_id, appointment_time):
    conn = get_connection()
    cur = conn.cursor()

    # приводим формат: 2025-03-31T03:12 → 2025-03-31 03:12
    appointment_time = appointment_time.replace("T", " ")

    query = """
    SELECT 1
    FROM appointments
    WHERE doctor_id = ?
      AND datetime(visit_time) BETWEEN
          datetime(?, '-30 minutes')
          AND
          datetime(?, '+30 minutes')
    """

    cur.execute(query, (doctor_id, appointment_time, appointment_time))
    exists = cur.fetchone()

    conn.close()

    # если запись найдена — слот занят
    return exists is None

def find_nearest_available_time(doctor_id, requested_time):
    conn = get_connection()
    cur = conn.cursor()

    # строку → datetime
    base_time = datetime.strptime(
        requested_time.replace("T", " "),
        "%Y-%m-%d %H:%M"
    )

    # проверяем вперёд с шагом 30 минут (до 10 попыток = 5 часов)
    for i in range(1, 11):
        candidate = base_time + timedelta(minutes=30 * i)
        candidate_str = candidate.strftime("%Y-%m-%d %H:%M")

        cur.execute("""
            SELECT 1 FROM appointments
            WHERE doctor_id = ?
              AND datetime(visit_time) BETWEEN
                  datetime(?, '-30 minutes')
                  AND
                  datetime(?, '+30 minutes')
        """, (doctor_id, candidate_str, candidate_str))

        if cur.fetchone() is None:
            conn.close()
            return candidate_str

    conn.close()
    return None


def get_by_user(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.id, d.name, d.specialization, a.visit_time
        FROM appointments a
        JOIN doctors d ON d.id = a.doctor_id
        WHERE a.user_id = ?
    """, (user_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def create_appointment(user_id, doctor_id, time):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO appointments (user_id, doctor_id, visit_time) VALUES (?, ?, ?)",
        (user_id, doctor_id, time)
    )
    conn.commit()
    conn.close()


def get_by_doctor(doctor_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.id,
               u.email,
               a.visit_time
        FROM appointments a
        JOIN users u ON a.user_id = u.id
        WHERE a.doctor_id = ?
        ORDER BY a.visit_time
    """, (doctor_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


def delete_by_id(appointment_id, user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM appointments WHERE id = ? AND user_id = ?",
        (appointment_id, user_id)
    )
    conn.commit()
    conn.close()
