import sqlite3

def get_connection():
    try:
        conn = sqlite3.connect('src/database/api.db')
        return conn
    except Exception as e:
        raise e