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
        self.validate_id(self.meeting_id)
        self.validate_notification_flag(self.send_notifications)

    def validate_name(self, new_name):
        """validate that the new name is a string type""" 
        if not isinstance(new_name, str):
            raise TypeError(f'The meeting name should be of type string \
                             ( {new_name} is not a string)')

    def validate_id( self, new_id):
        """validate that new id is a positive integer"""
        if not isinstance(new_id, int):
            raise TypeError(f"Meeting ID should be of type integer \
                            ( {new_id} is not and integer)")
        if isinstance(new_id, int) and (new_id < 0):
            raise ValueError( f"Meeting ID should be non-negative number\
                            ( {new_id} is not a positive number)")

    def validate_notification_flag(self, new_value):
        "validate that notification flag is bool type"
        if not isinstance(new_value, bool):
            raise TypeError(f"Notification flag should be a bool \
                            ( {new_value} is not a bool)")
