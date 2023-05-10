"""Class to describe details of a particular meeting """
from dataclasses import dataclass, field
from datetime import datetime
from participant import Participant

@dataclass(frozen=True)
class Meeting :
    """Describes details of a meeting"""
    meeting_id : int
    name: str
    datetime: datetime
    send_notifications: bool = True
    room_confirmed: bool = False
    participants: list[Participant] = field( default_factory=list)
    meeting_notes : str
