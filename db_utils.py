import sqlite3
import datetime

def connect_to_db(db_name):
    return sqlite3.connect(db_name)

def user_login(user_id):
    conn = connect_to_db('user_db.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def setup_user_db():
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

def place_order(user_id, order_details):
    conn = connect_to_db('canteen_orders_db.sqlite')
    cursor = conn.cursor()

    for detail in order_details:
        item = detail['item']
        quantity = detail['quantity']
        price = detail['price']
        total_cost = quantity * price
        timestamp = datetime.datetime.now().isoformat()

        cursor.execute(
            "INSERT INTO canteen_orders (user_id, item, quantity, price, total_cost, timestamp, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, item, quantity, price, total_cost, timestamp, 'Pending')
        )
    conn.commit()
    conn.close()

def canteen_login(username, password):
    conn = connect_to_db('canteen_login_db.sqlite')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM canteen_login WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def get_orders():
    conn = connect_to_db('canteen_orders_db.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM canteen_orders ORDER BY timestamp DESC')
    orders = cursor.fetchall()
    conn.close()
    return orders

def mark_order_as_delivered(order_id):
    conn = connect_to_db('canteen_orders_db.sqlite')
    cursor = conn.cursor()
    cursor.execute("UPDATE canteen_orders SET status='Delivered' WHERE id=?", (order_id,))
    conn.commit()
    conn.close()

def create_tables():
    conn = connect_to_db('canteen_orders_db.sqlite')
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
