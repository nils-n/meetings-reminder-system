"""add fixtures for unittest here to follow the DRY principle"""
from typing import List
from datetime import datetime
from random import randint
from participant import Participant
from meeting import Meeting
import pytest

@pytest.fixture(scope='session')
def init_values():
    """fixture to create random init values shared across tests"""
    random_name = 'Han Solo'
    random_email = "hansolo@fakemail.com"
    random_id = 42
    return random_name,  random_email, random_id

@pytest.fixture(scope='session')
def init_participant() -> Participant:
    """initializes a random Participant"""
    random_name = "Han Solo"
    random_email = "hansolo@fakemail.com"
    random_id = 42
    return Participant( random_name, random_email, random_id, True)

@pytest.fixture(scope='session')
def create_random_participants( ) -> List[Participant]:
    """returns a list of participants"""
    random_names = [ "Han Solo", "Darth Vader" , "Chewbacca" ]
    random_emails = ["hansolo@fakemail.com", "darthvader@fakemail.com" , "chewbacca@fakemail.com" ]
    participants = []
    for i, (name, email) in enumerate(zip(random_names, random_emails)):
        participants.append( Participant( name, email, i, True))
    return participants


@pytest.fixture(scope='session')
def create_random_meetings( ) -> List[Meeting]:
    """initializes and returns a list of random meeting with random values"""
    random_meetings = []
    num_random_meetings = 2
    for meeting_id in range(num_random_meetings):
        # create random fake participants 
        random_names = [ "Han Solo", "Darth Vader" , "Chewbacca" ]
        random_emails = ["hansolo@fakemail.com", "darthvader@fakemail.com" , "chewbacca@fakemail.com" ]
        random_participants = []
        for i, (name, email) in enumerate(zip(random_names, random_emails)):
            random_participants.append( Participant( name, email, i, True))
        # create random fake meeting with these participants 
        random_meeting_id = meeting_id
        random_meeting_name = f"Random Meeting {meeting_id}"
        random_date_time = datetime.now()
        random_meeting_notes = 'This is a random note for this meeting \
            to be sent along with the reminder. '
        random_meetings.append( Meeting(random_meeting_id, random_meeting_name, \
                                        random_date_time, True, True, \
                                    random_participants, random_meeting_notes))
    return random_meetings
