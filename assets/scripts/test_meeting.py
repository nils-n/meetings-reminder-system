"""
This is a unit test for the participant class. 

All unit tests are laid out in the form 

A rrange
A ct 
A ssert

"""
from datetime import datetime
from contextlib import nullcontext as does_not_raise
from meeting import Meeting
import pytest

def test_can_create_new_meeting( create_random_participants) -> None:
    """Test if a meeting instance can be created"""
    participants = create_random_participants
    random_meeting_name = "Journal Club"
    random_meeting_id = 42
    random_date_time = datetime.now()
    random_meeting_notes = 'This is a random note for this meeting \
        to be sent along with the reminder. '

    model = Meeting(random_meeting_id, random_meeting_name, random_date_time, True, True, \
                     participants, random_meeting_notes)

    assert isinstance( model, Meeting)

@pytest.mark.parametrize (
        "fixture_name, new_name, expectation", 
        [
            ("create_random_participants", 'Death Star Staff Meeting', does_not_raise()),
            ("create_random_participants", 'Rebel Briefing', does_not_raise()),
            ("create_random_participants", 42,  pytest.raises(TypeError))
        ]
)
def test_invalid_name_raises_type_error(fixture_name, new_name, expectation, request):
    """test various correct and incorrect meeting names"""
    participants = request.getfixturevalue(fixture_name)
    random_meeting_id = 42
    random_date_time = datetime.now()
    random_meeting_notes = 'This is a random note for this meeting.'

    with expectation:
        Meeting(random_meeting_id, new_name, random_date_time, True, True, \
                     participants, random_meeting_notes)

@pytest.mark.parametrize(
    "fixture_name, new_id, expectation", 
    [
        ('create_random_participants', 1, does_not_raise()),
        ('create_random_participants', 1044, does_not_raise()),
        ('create_random_participants', "42", pytest.raises(TypeError)),
        ('create_random_participants', None, pytest.raises(TypeError)),
        ('create_random_participants', -1, pytest.raises(ValueError))
    ]
)
def test_invalid_id_raises_type_error( fixture_name, new_id, expectation, request):
    """test various correct and incorrect meeting IDs"""
    participants = request.getfixturevalue(fixture_name)
    random_name = "R2D2"
    random_date_time = datetime.now()
    random_meeting_notes = 'This is a random note for this meeting.'

    with expectation:
        Meeting( new_id, random_name, random_date_time, True, True, \
                participants, random_meeting_notes)

@pytest.mark.parametrize(
    "fixture_name, notification_value, expectation", 
    [
        ('create_random_participants', True, does_not_raise()),
        ('create_random_participants', "True", pytest.raises(TypeError)),
        ('create_random_participants', [True, ], pytest.raises(TypeError)),
        ('create_random_participants', None, pytest.raises(TypeError))
    ]
)
def test_invalid_notification_flag_raises_type_error( fixture_name, notification_value, \
                                                     expectation, request):
    """ensure that notification flag is a bool type"""
    participants = request.getfixturevalue(fixture_name)
    random_name = "R2D2"
    random_meeting_id = 42
    random_date_time = datetime.now()
    random_meeting_notes = 'This is a random note for this meeting.'

    with expectation:
        Meeting( random_meeting_id, random_name, random_date_time, notification_value, True, \
                participants, random_meeting_notes)

@pytest.mark.parametrize(
        "fixture_name, new_time, expectation",
        [
            ('create_random_participants', datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M") \
              , does_not_raise()),
            ('create_random_participants', datetime.now() , does_not_raise()),
            ('create_random_participants', "21/11/06 16:30" , pytest.raises(TypeError))
        ]
)
def test_invalid_time_raises_type_error( fixture_name, new_time, \
                                        expectation, request):
    """ensure that meeting time is correct datetime type"""
    participants = request.getfixturevalue(fixture_name)
    random_name = "R2D2"
    random_meeting_id = 42
    random_meeting_notes = 'This is a random note for this meeting.'

    with expectation:
        Meeting( random_meeting_id, random_name, new_time, True, True, \
                participants, random_meeting_notes)
