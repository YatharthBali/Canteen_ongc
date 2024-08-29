import sqlite3

def populate_users():
    # Connect to the user database
    conn = sqlite3.connect('user_db.sqlite')
    cursor = conn.cursor()
    
    # Insert user data
    users = [
        (101, 'Parvesh', 3, 21, '9860988854'),
        (102, 'Kartik', 1, 45, '9811066875'),
        (103, 'Sumit', 2, 1, '8805568756')
    ]
    
    cursor.executemany('''
        INSERT OR IGNORE INTO users (user_id, name, floor, seat_no, contact_no) 
        VALUES (?, ?, ?, ?, ?)
    ''', users)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    populate_users()
