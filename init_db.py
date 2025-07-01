import sqlite3
import os


SCHEMA_FILE = 'schema.sql'

DB_PATH = os.path.join('data', 'bakery.db')

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    with open(SCHEMA_FILE, 'r') as f:
        sql_script = f.read()

    conn.executescript(sql_script)
    conn.commit()
    conn.close()
    
    print("Database Initialized successfully!")

if __name__ == '__main__':
    init_db()