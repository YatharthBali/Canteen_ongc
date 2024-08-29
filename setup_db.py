import sqlite3

def setup_database():
    # Create user database
    conn = sqlite3.connect('user_db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            floor INTEGER NOT NULL,
            seat_no INTEGER NOT NULL,
            contact_no TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

    conn = sqlite3.connect('canteen_orders_db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS canteen_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            item TEXT,
            quantity INTEGER,
            price REAL,
            total_cost REAL,
            timestamp TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

    # Create canteen login database
    conn = sqlite3.connect('canteen_login_db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS canteen_login (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

    # Create canteen side database (if needed)
    conn = sqlite3.connect('canteen_side_db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS canteen_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            item TEXT,
            quantity INTEGER,
            price REAL,
            total_cost REAL,
            timestamp TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

    conn = sqlite3.connect('user_db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            floor INTEGER NOT NULL,
            seat_no INTEGER NOT NULL,
            contact_no TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

    # Create canteen orders database
    conn = sqlite3.connect('canteen_orders_db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS canteen_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            item TEXT,
            quantity INTEGER,
            price REAL,
            total_cost REAL,
            timestamp TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

    # Create canteen login database
    conn = sqlite3.connect('canteen_login_db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS canteen_login (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

    # Create canteen side database (if needed)
    conn = sqlite3.connect('canteen_side_db.sqlite')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS canteen_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            item TEXT,
            quantity INTEGER,
            price REAL,
            total_cost REAL,
            timestamp TEXT,
            status TEXT
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()
