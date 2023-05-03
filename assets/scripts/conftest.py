"""add fixtures for unittest here to follow the DRY principle"""
import pytest


@pytest.fixture(scope='session')
def init_values():
    """fixture to create random init values shared across tests"""
    random_name = 'Han Solo'
    random_email = "hansolo@fakemail.com"
    random_id = 42
    return random_name,  random_email, random_id
