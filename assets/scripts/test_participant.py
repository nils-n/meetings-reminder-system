"""
This is a unit test for the participant class. 

All unit tests are laid out in the form 

A rrange
A ct 
A ssert

"""
from contextlib import nullcontext as does_not_raise
from participant import Participant
from email_validator import validate_email, EmailNotValidError
import pytest

def test_can_create_new_participant():
    """test if a new participant can be created"""
    random_name = 'Han Solo'
    random_email = 'hansolo@fakemail.com'
    random_id = 1

    model =  Participant(random_name, random_email, random_id)

    assert isinstance(model, Participant)

@pytest.mark.parametrize(
    "example_input,expectation",
    [
        ('hansolo@fakemail.com', does_not_raise()),
        ('chewbacca@fakemail.com', does_not_raise()),
        ('darthvadser@fakemail.com', does_not_raise()),
        ('hansolo@fakemailcom', pytest.raises(EmailNotValidError)),
    ],
)
def test_invalid_emails_raise_error(example_input, expectation):
    """test various correct and incorrect participant email addresses"""
    random_name = 'Han Solo'
    random_id = 1
    with expectation:
        model =  Participant(random_name, example_input, random_id)
        validate_email( model.email)
