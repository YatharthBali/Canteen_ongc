import sqlite3

def check_tables():
    conn = sqlite3.connect('user_db.sqlite')  # or the relevant database file
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables:", tables)
    conn.close()

check_tables()

def inspect_table():
    conn = sqlite3.connect('user_db.sqlite')  # or the relevant database file
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(users);")
    columns = cursor.fetchall()
    print("Users Table Columns:", columns)
    conn.close()

inspect_table()