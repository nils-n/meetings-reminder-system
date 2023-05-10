"""
This is a unit test for the participant class. 

All unit tests are laid out in the form 

A rrange
A ct 
A ssert

"""
from datetime import datetime
from participant import Participant
from meeting import Meeting

def test_can_create_new_meeting( init_values) -> None:
    """Test if a meeting instance can be created"""
    random_name,  random_email, random_id = init_values
    participants = []
    participants.append( Participant( random_name, random_email, random_id, True))
    random_meeting_name = "Journal Club"
    random_date_time = datetime.now()
    random_meeting_notes = 'This is a random note for this meeting \
        to be sent along with the reminder. '
    model = Meeting(random_id, random_meeting_name, random_date_time, True, True, \
                     participants, random_meeting_notes)

    assert isinstance( model, Meeting)
