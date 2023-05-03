"""
This is a unit test for the participant class. 

All unit tests are laid out in the form 

A rrange
A ct 
A ssert

"""
from participant import Participant

def test_can_create_new_participant():
    """"""
    random_name = 'Han Solo'
    random_email = 'hansolo@fakemail.com'
    random_id = 1

    model =  Participant(random_name, random_email, random_id)

    assert isinstance(model, Participant)