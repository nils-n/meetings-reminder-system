"""
These are unit tests for the schedule class. 

All unit tests are laid out in the form 

A rrange
A ct 
A ssert

"""
import pytest
from reminding.meeting import Meeting
from reminding.schedule import Schedule
from datetime import datetime


def test_can_create_new_schedule( create_random_meetings ) -> None:
    """Tests if a new Schedule can be instaniated """
    random_meetings = create_random_meetings
    random_name = "Random Schedule"

    model = Schedule(random_name, random_meetings )

    assert isinstance(model, Schedule)
    assert model.name == random_name

def test_can_create_empty_schedule() -> None:
    """Test if the Schedule class can create an empty schedule for displau the TUI"""
    random_name = "Random Schedule"

    model = Schedule(random_name, [], [])
    model.add_meeting( Meeting( 0, "Journal Club", datetime.now(), True, True, [], "" ))
    model.add_meeting( Meeting( 1, "Lab Meeting", datetime.now(), True, True, [], "" ))
  
    assert model.meetings[0].name == "Journal Club"
    assert model.meetings[0].meeting_id == 0
    assert model.meetings[1].name == "Lab Meeting"
    assert model.meetings[1].meeting_id == 1
    assert len(model.meetings) == 2


def test_table_rows_match_values_of_corresponding_meetings() -> None:
    """
    Test if meeting values are converted correctly to DataTable rows  
    """
    random_name = "Random Schedule"

    model = Schedule(random_name, [], [])
    model.add_meeting( Meeting( 0, "Journal Club", datetime.now(), True, True, [], "" ))

    assert model.table_rows[0][0] == "ID"
    assert model.table_rows[1][0] == model.meetings[0].meeting_id
    assert model.table_rows[0][1] == "Name"
    assert model.table_rows[1][1] == model.meetings[0].name