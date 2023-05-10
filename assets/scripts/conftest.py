"""add fixtures for unittest here to follow the DRY principle"""
from typing import List
from participant import Participant
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
