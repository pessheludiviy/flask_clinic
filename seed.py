import sqlite3
import random
import uuid
from services.auth_service import hash_password
#Это файл для тестирования, чтобы добавлять докторов, пароль ко всем аккаунтам врачей - 1234, мыло в database.db
DB_NAME = "database.db"

NAMES = [
    "Иванов Иван Иванович",
    "Петров Пётр Петрович",
    "Сидоров Алексей Сергеевич",
    "Смирнова Анна Викторовна",
    "Кузнецов Дмитрий Олегович"
]

SPECIALIZATIONS = [
    "Терапевт",
    "Хирург",
    "Невролог",
    "Кардиолог",
    "Педиатр"
]

def random_email():
    return f"doctor_{uuid.uuid4().hex[:8]}@clinic.ru"

def main():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    name = random.choice(NAMES)
    specialization = random.choice(SPECIALIZATIONS)
    email = random_email()
    password = hash_password("1234")

    # 1️⃣ создаём пользователя-врача
    cur.execute(
        "INSERT INTO users (email, password_hash, role) VALUES (?, ?, ?)",
        (email, password, "doctor")
    )
    user_id = cur.lastrowid

    # 2️⃣ профиль
    cur.execute(
        "INSERT INTO profiles (user_id, full_name) VALUES (?, ?)",
        (user_id, name)
    )

    # 3️⃣ доктор
    cur.execute(
        "INSERT INTO doctors (user_id, name, specialization) VALUES (?, ?, ?)",
        (user_id, name, specialization)
    )

    conn.commit()
    conn.close()

    print("✅ Врач создан")
    print(f"Email: {email}")
    print("Пароль: 1234")
    print(f"Имя: {name}")
    print(f"Специализация: {specialization}")

if __name__ == "__main__":
    main()
