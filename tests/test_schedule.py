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
from contextlib import nullcontext as does_not_raise


def test_can_create_new_schedule( create_random_meetings ) -> None:
    """Tests if a new Schedule can be instaniated """
    random_meetings = create_random_meetings
    random_name = "Random Schedule"

    model = Schedule(random_name, random_meetings )

    assert isinstance(model, Schedule)
    assert model.name == random_name

def xtest_can_create_empty_schedule() -> None:
    """
    Test if the Schedule class can create an empty schedule for displau the TUI
    Test disabled to allow for Mock meetings (for faster debugging of the TUI).
       -> Once the Mock Classes are removed, the test should pass 
    """
    random_name = "Random Schedule"

    model = Schedule(random_name, [], [])
    model.add_meeting( Meeting( 0, "Journal Club", datetime.now(), True, True, [], "" ))
    model.add_meeting( Meeting( 1, "Lab Meeting", datetime.now(), True, True, [], "" ))
  
    assert model.meetings[0].name == "Journal Club"
    assert model.meetings[1].name == "Lab Meeting"
    assert 0 < model.meetings[0].meeting_id < 1000  # ensure that model.meeting_id is between 0 and 1000
    assert 0 < model.meetings[1].meeting_id < 1000  # ensure that model.meeting_id is between 0 and 1000

def test_table_rows_match_values_of_corresponding_meetings() -> None:
    """
    Test if meeting values are converted correctly to DataTable rows  
    """
    random_name = "Random Schedule"

    model = Schedule(random_name, [], [])
    model.add_meeting( Meeting( 0, "Journal Club", datetime.now(), True, True, [], "" ))

    assert model.table_rows[0][0] == "ID"
    assert 0 < model.table_rows[1][0] < 1000  # ensure that model.meeting_id is between 0 and 1000
    assert model.table_rows[0][1] == "Name"
    assert model.table_rows[1][1] == model.meetings[0].name


@pytest.mark.parametrize(
    "meeting_id_input, expectation", 
    [
        (1, does_not_raise()),
        (2, does_not_raise()),
        (3, pytest.raises(ValueError)),
        (444, pytest.raises(ValueError)),
        ("1", does_not_raise()),
        ("You shall not pass", pytest.raises(ValueError)),
        (None, pytest.raises(TypeError)),
    ]
)
def test_raises_error_when_meeting_id_does_not_exist( meeting_id_input, expectation) -> None:
    """
    Test that schedule throws an expecption when 
    the user tries to modify a meeting wit an invalid meeting ID
    """
    random_name = "Random Schedule"
    random_datetime =  datetime.strptime( "01/01/71 00:00", "%d/%m/%y %H:%M")

    model = Schedule(random_name, [], [])
    model.add_meeting(  Meeting( 1, "Mock Meeting 1 ",random_datetime, True, True, [], "" ) )
    model.add_meeting(  Meeting( 2, "Mock Meeting 2 ",random_datetime, True, True, [], "" ) )

    with expectation: 
        model.validate_meeting_id( meeting_id_input) 

@pytest.mark.parametrize(
    "target_id, expectation", 
    [
        (1, does_not_raise()),
        (2, does_not_raise()),
        (3, pytest.raises(ValueError)),
        (444, pytest.raises(ValueError)),
        ("1", does_not_raise()),
        ("You shall not pass", pytest.raises(ValueError)),
        (None, pytest.raises(TypeError)),
    ]
)
def test_incorrect_input_of_meeting_id_raises_error( target_id, expectation) -> None:
    """
    Test if function raises correct error when supplied with
    invalid meeting ID 
    """

    random_name = "Random Schedule"
    random_datetime =  datetime.strptime( "01/01/71 00:00", "%d/%m/%y %H:%M")

    model = Schedule(random_name, [], [])
    model.add_meeting(  Meeting( 1, "Mock Meeting 1 ",random_datetime, True, True, [], "" ) )
    model.add_meeting(  Meeting( 2, "Mock Meeting 2 ",random_datetime, True, True, [], "" ) )
                      
    with expectation: 
        model.get_meeting_by_id( target_id) 

@pytest.mark.parametrize(
    "target_id, expectation", 
    [
        (1, "Mock Meeting 1"),
        (2, "Mock Meeting 2"),
    ]
)
def test_correct_input_of_meeting_id_returns_correct_meeting( target_id, expectation) -> None: 
    """
    Test if meeting is returns correct meeting after
    asking the schedule for it via its ID 
    """

    random_name = "Random Schedule"
    random_datetime =  datetime.strptime( "01/01/71 00:00", "%d/%m/%y %H:%M")
    random_schedule = Schedule(random_name, [], [])
    random_schedule.add_meeting(  Meeting( 1, "Mock Meeting 1 ",random_datetime, True, True, [], "" ) )
    random_schedule.add_meeting(  Meeting( 2, "Mock Meeting 2 ",random_datetime, True, True, [], "" ) )
    
    model =  random_schedule.get_meeting_by_id( target_id ) 
    
    assert model.name == expectation
       