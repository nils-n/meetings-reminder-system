"""
This is a unit test for the participant class. 

All unit tests are laid out in the form 

A rrange
A ct 
A ssert

"""
from datetime import datetime
from meeting import Meeting

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
