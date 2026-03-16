from dataclasses import dataclass
from datetime import datetime


@dataclass
class Transcription:
    """
    Dataclass representing a transcription row.
    """

    id: str
    filename: str
    transcription: str
    created_at: datetime
