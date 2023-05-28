"""Class to describe details of a particular meeting """
from dataclasses import dataclass, field
from datetime import datetime
from typing import Union
from reminding.participant import Participant

@dataclass(frozen=False)
class Meeting :
    """Describes details of a meeting"""
    meeting_id : int
    name: str
    datetime: datetime
    send_notifications: bool = True
    room_confirmed: bool = False
    participants: list[Participant] = field( default_factory=list)
    meeting_notes : str = ""
    table_row: Union[str, int] = field( default_factory=list)

    def __post_init__(self):
        """validate that the attributes have correct form"""
        self.validate_name( self.name)
        self.validate_id(self.meeting_id)
        self.validate_notification_flag(self.send_notifications)
        self.validate_meeting_time( self.datetime)
        self.validate_meeting_room_flag( self.room_confirmed)
        self.validate_meeting_note(self.meeting_notes)
        self.convert_to_table_row()

    def validate_name(self, new_name):
        """validate that the new name is a string type""" 
        if not isinstance(new_name, str):
            raise TypeError(f'The meeting name should be of type string \
                             ( {new_name} is not a string)')
        self.name = new_name

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

    def validate_meeting_time(self, new_time):
        """validate that meeting time is of datetime data type"""
        if not isinstance( new_time, datetime):
            raise TypeError( f"Meeting time should be a built-in datetime type\
                            ( {new_time} is not of type datetime)")
        self.datetime = new_time

    def validate_meeting_room_flag( self, new_room_flag):
        """validate that flag for meeting room is bool type"""
        if not isinstance( new_room_flag, bool):
            raise TypeError( f"Meeting room flag should be a boolean\
                            ( {new_room_flag} is not a boolean)")

    def validate_meeting_note( self, new_note):
        """validate that meeting not is a string type"""
        if not isinstance( new_note, str):
            raise TypeError( f"Meeting notes should be a str type \
                            ( {new_note} is not a string)")

    def convert_to_table_row(self):
        """
        convert the meetings details into a table format that the TUI can display
        """
        self.table_row = []
        self.table_row.append( ("ID", "Name", "Time", "invited", "confirmed" ))
        self.table_row.append( ( self.meeting_id, self.name, self.datetime, 84, 84))