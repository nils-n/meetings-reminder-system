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
    meeting_notes : str = ""

    def __post_init__(self):
        """validate that the attributes have correct form"""
        self.validate_name( self.name)

    def validate_name(self, new_name):
        """validate that the new name is a string type""" 
        if not isinstance(new_name, str):
            raise TypeError(f'The meeting name should be of type string \
                             ( {new_name} is not a string)')
        