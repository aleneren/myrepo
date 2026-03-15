import sqlite3
import os

DB_PATH: str = os.getenv("DB_PATH")

if not DB_PATH:
    raise ValueError("DB_PATH environment variable is not set.")

# Ensure the directory exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)


def get_connection() -> sqlite3.Connection:
    """
    Create and return a SQLite database connection.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        raise
