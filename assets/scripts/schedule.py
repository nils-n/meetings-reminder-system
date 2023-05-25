"""class to describe a schedule of meetings"""
from dataclasses import dataclass, field
from typing import Union
from meeting import Meeting

@dataclass
class Schedule ():
    """
    describes a schedule of meetings
    for table rows :how to load a mixed variables into dataclass variables from: 
    https://stackoverflow.com/questions/69915050/how-to-make-list-in-python-dataclass-that-can-accept-multiple-different-types
    """
    name: str
    num_meetings: int
    meetings: list[Meeting] = field( default_factory=list)
    table_rows:  list[Union[str, int]] = field( default_factory=list)

    def load_meetings(self):
        """
        currently this loads a hard-coded list of mock meetings
        eventually this will be replaced by reading data from a google worksheet
        """
        pass

    def convert_meetings_to_table(self):
        """
        convert the meetings object into a table format that the TUI can display and update
        """
        pass
