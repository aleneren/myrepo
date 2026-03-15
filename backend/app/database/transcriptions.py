import uuid
from typing import List

from app.database.connection import get_connection
from app.model.transcriptions import Transcription


def get_unique_filename(original_filename: str) -> str:
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            while True:
                unique_filename = f"{uuid.uuid4().hex}_{original_filename}"

                cursor.execute(
                    "SELECT 1 FROM transcriptions WHERE filename = ?",
                    (unique_filename,),
                )

                if cursor.fetchone() is None:
                    return unique_filename
    except Exception as e:
        print(f"Error generating unique filename: {e}")
        raise


def insert_transcription(filename: str, transcription: str) -> None:
    try:
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO transcriptions (filename, transcription)
                VALUES (?, ?)
                """,
                (filename, transcription),
            )
    except Exception as e:
        print(f"Error inserting transcription: {e}")
        raise


def get_transcriptions() -> List[Transcription]:
    try:
        with get_connection() as conn:
            rows = conn.execute(
                """
                SELECT id, filename, transcription, created_at
                FROM transcriptions
                ORDER BY created_at DESC
                """
            ).fetchall()

        return [Transcription(*row) for row in rows]
    except Exception as e:
        print(f"Error fetching transcriptions: {e}")
        raise


def search_transcriptions(query: str) -> List[Transcription]:
    try:
        search_term = f"%{query}%"

        with get_connection() as conn:
            rows = conn.execute(
                """
                SELECT id, filename, transcription, created_at
                FROM transcriptions
                WHERE filename LIKE ?
                OR transcription LIKE ?
                ORDER BY created_at DESC
                """,
                (search_term, search_term),
            ).fetchall()

        return [Transcription(*row) for row in rows]
    except Exception as e:
        print(f"Error searching transcriptions: {e}")
        raise
