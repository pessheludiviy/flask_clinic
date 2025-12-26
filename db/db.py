import sqlite3

def get_connection():
    return sqlite3.connect("C:/Users/netrunner/Desktop/prfiles/sem2/database.db")
