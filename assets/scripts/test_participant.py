"""
This is a unit test for the participant class. 

All unit tests are laid out in the form 

A rrange
A ct 
A ssert

"""
from contextlib import nullcontext as does_not_raise
from participant import Participant
from email_validator import EmailNotValidError
import pytest

def test_can_create_new_participant(init_values) -> None:
    """test if a new participant can be created"""
    random_name,  random_email, random_id = init_values

    model =  Participant(random_name, random_email, random_id, False)

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
def test_invalid_email_raises_error(example_input, expectation):
    """test various correct and incorrect participant email addresses"""
    random_name = 'Han Solo'
    random_id = 1

    with expectation:
        Participant(random_name, example_input, random_id, False)

@pytest.mark.parametrize(
    "example_input,expectation",
    [
        ('Han Solo', does_not_raise()),
        ('Chewbakka', does_not_raise()),
        ('Darth Vader', does_not_raise()),
        (1, pytest.raises(TypeError)),
        (None, pytest.raises(TypeError)),
        ( ["A", "List", "of", "Strings"], pytest.raises(TypeError)),
    ],
)
def test_invalid_name_raises_error(example_input, expectation):
    """test various correct and incorrect participant names"""
    random_email= "hansolo@fakemail.com"
    random_id = 1

    with expectation:
        Participant(example_input, random_email, random_id, False)

@pytest.mark.parametrize(
    "fixture_name,example_input,expectation",
    [
        ("init_values", 1, does_not_raise()),
        ("init_values", 2 , does_not_raise()),
        ("init_values", 42, does_not_raise()),
        ("init_values", "42", pytest.raises(TypeError)),
        ("init_values", -1, pytest.raises(ValueError)),
        ("init_values", None, pytest.raises(TypeError)),
        ("init_values", ["A", "List", "of", "Strings"], pytest.raises(TypeError)),
    ],
)
def test_invalid_meeting_id_raises_error(fixture_name, example_input, expectation, request):
    """test wether meeting id a positive integer"""
    init_values = request.getfixturevalue(fixture_name)
    random_name,  random_email, random_id = init_values
    
    with expectation:
        Participant(random_name, random_email, example_input, False)

def test_can_update_participant_name():
    random_name = 'Han Solo'
    random_email= "hansolo@fakemail.com"

