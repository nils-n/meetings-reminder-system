"""class to describe a schedule of meetings"""
from dataclasses import dataclass, field
from typing import Union
from datetime import datetime
from reminding.meeting import Meeting

@dataclass
class Schedule ():
    """
    describes a schedule of meetings
    for table rows :how to load a mixed variables into dataclass variables from: 
    https://stackoverflow.com/questions/69915050/how-to-make-list-in-python-dataclass-that-can-accept-multiple-different-types
    """
    name: str
    meetings: list[Meeting] = field( default_factory=list)
    table_rows:  list[Union[str, int]] = field( default_factory=list)

    def __post_init__(self):
        self.load_meetings()
        self.convert_meetings_to_table()

    def load_meetings(self):
        """
        currently this loads a hard-coded list of mock meetings
        eventually this will be replaced by reading data from a google worksheet
        """
        self.meetings = []
        self.meetings.append( Meeting( 0, "Journal Club", datetime.now(), True, True, [], "" ))
        self.meetings.append( Meeting( 1, "Lab Meeting", datetime.now(), True, True, [], "" ))

    def convert_meetings_to_table(self):
        """
        convert the meetings object into a table format that the TUI can display and update
        """
        self.table_rows = []
        self.table_rows.append( ("ID", "Name", "Time", "invited", "confirmed" ))
        for meeting in self.meetings:
            self.table_rows.append( ( meeting.meeting_id, meeting.name, meeting.datetime, 42, 42))
