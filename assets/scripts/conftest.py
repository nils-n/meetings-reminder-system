"""add fixtures for unittest here to follow the DRY principle"""
import pytest
from participant import Participant


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