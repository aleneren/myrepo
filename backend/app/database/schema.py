from app.database.connection import get_connection


def init_db() -> None:
    """
    Initialize the database schema.
    """
    try:
        with get_connection() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS transcriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL UNIQUE,
                    transcription TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );

                CREATE INDEX IF NOT EXISTS idx_transcription_filename
                ON transcriptions(filename);
                """
            )
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise
