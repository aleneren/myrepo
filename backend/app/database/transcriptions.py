from typing import List

from app.database.connection import get_connection
from app.model.transcriptions import Transcription


def insert_transcription(uuid: str, filename: str, transcription: str) -> None:
    """
    Inserts a transcription record into the database.

    Args:
        uuid (str): The unique identifier for the transcription.
        filename (str): The unique filename for the audio file.
        original_filename (str): The original filename of the audio file.
        transcription (str): The transcription text.
    """
    try:
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO transcriptions (id, filename, transcription)
                VALUES (?, ?, ?)
                """,
                (uuid, filename, transcription),
            )
    except Exception as e:
        print(f"Error inserting transcription: {e}")
        raise


def get_transcriptions() -> List[Transcription]:
    """
    Fetches all transcription records from the database.

    Returns:
        List[Transcription]: A list of transcription records.
    """
    try:
        with get_connection() as conn:
            rows = conn.execute("""
                SELECT id, filename, transcription, created_at
                FROM transcriptions
                ORDER BY i DESC
                """).fetchall()

        return [Transcription(*row) for row in rows]
    except Exception as e:
        print(f"Error fetching transcriptions: {e}")
        raise


def search_transcriptions(query: str) -> List[Transcription]:
    """
    Searches for transcription records based on audio filename (case-insensitive, partial match).

    Args:
        query (str): The search query for the audio filename.

    Returns:
        List[Transcription]: A list of transcription records matching the search query.
    """
    try:
        search_term = f"%{query}%"

        with get_connection() as conn:
            rows = conn.execute(
                """
                SELECT id, filename, transcription, created_at
                FROM transcriptions
                WHERE filename LIKE ? COLLATE NOCASE
                ORDER BY i DESC
                """,
                (search_term,),
            ).fetchall()

        return [Transcription(*row) for row in rows]
    except Exception as e:
        print(f"Error searching transcriptions: {e}")
        raise
