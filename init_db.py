import sqlite3
import os
#файл для инициализации бд, использует самописную sql схему в db/schema (файл без расширения по какой-то причине пчарм не хочет рефакторить его с расширением sql)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

with sqlite3.connect(DB_PATH) as conn:
    with open("db/schema", encoding="utf-8") as f:
        conn.executescript(f.read())

print("База данных и таблицы успешно созданы")
