import sqlite3

DB_PATH = 'users.db'

def add_user(user_id, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (user_id, password) VALUES (?, ?)', (user_id, password))
        conn.commit()
        print(f"User '{user_id}' added successfully.")
    except sqlite3.IntegrityError:
        print(f"User '{user_id}' already exists.")
    finally:
        conn.close()

if __name__ == '__main__':
    user_id = input('Enter new username: ')
    password = input('Enter password: ')
    add_user(user_id, password) 