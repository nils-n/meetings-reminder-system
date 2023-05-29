"""
This is a unit test for the participant class. 

All unit tests are laid out in the form 

A rrange
A ct 
A ssert

"""
from contextlib import nullcontext as does_not_raise
from reminding.participant import Participant
from email_validator import EmailNotValidError
import pytest

def test_can_create_new_participant(init_values) -> None:
    """test if a new participant can be created"""
    random_name,  random_email, random_id = init_values

    model =  Participant(random_name, random_email, random_id, False)

    assert isinstance(model, Participant)

@pytest.mark.parametrize(
    "fixture_name, example_input,expectation",
    [
        ("init_values", 'Han Solo', does_not_raise()),
        ("init_values", 'Chewbakka', does_not_raise()),
        ("init_values", 'Darth Vader', does_not_raise()),
        ("init_values", 1, pytest.raises(TypeError)),
        ("init_values", None, pytest.raises(TypeError)),
        ("init_values",  ["A", "List", "of", "Strings"], pytest.raises(TypeError)),
    ],
)
def test_invalid_name_raises_error(fixture_name, example_input, expectation, request):
    """test various correct and incorrect participant names"""
    _ , random_email, random_id = request.getfixturevalue(fixture_name)

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
    random_name,  random_email, _ = request.getfixturevalue(fixture_name)

    with expectation:
        Participant(random_name, random_email, example_input, False)

@pytest.mark.parametrize(
        "new_name,expectation, fixture_name", 
        [
            ( "Sith Lord", "Sith Lord", "init_participant"),
            ( "Han Solo", "Han Solo", "init_participant")
        ]
)
def test_can_update_participant_name(new_name, expectation, fixture_name, request):
    """Test wheter participant name can be updated"""
    model = request.getfixturevalue(fixture_name)

    model.update_name(new_name)

    assert model.name == expectation

@pytest.mark.parametrize(
    "new_email, expectation, fixture_name",
    [
        ("sithlord@fakemail.com", "sithlord@fakemail.com",  "init_participant"),
        ("hansolo@fakemail.com", "hansolo@fakemail.com",  "init_participant"),
        ("chewbacca@fakemail.com", "chewbacca@fakemail.com",  "init_participant")
    ]
)
def test_can_update_participant_email( new_email, expectation, fixture_name, request):
    """Test whether participant email can be updated"""
    model = request.getfixturevalue( fixture_name)

    model.update_email(new_email)

    assert model.email == expectation

@pytest.mark.parametrize(
    "new_id, expectation, fixture_name", 
    [
        (42, 42, "init_participant"),
        (1, 1, "init_participant")
    ]
)
def test_can_update_participant_id( new_id, expectation, fixture_name, request):
    """Test wheter participant id can be updated """
    model = request.getfixturevalue( fixture_name)

    model.update_id( new_id)

    assert model.id_number == expectation

@pytest.mark.parametrize(
        "new_id, expectation, fixture_name",
        [
            ("42", pytest.raises(TypeError), "init_participant"),
            ([42], pytest.raises(TypeError), "init_participant"),
            ((42,), pytest.raises(TypeError), "init_participant"),
            (None, pytest.raises(TypeError), "init_participant"),

        ]
)
def test_wrong_participant_id_raises_type_error( new_id, expectation, fixture_name, request):
    """Test wheter wrong input of new meeting id raises exception"""
    model = request.getfixturevalue( fixture_name)

    with expectation:
        model.update_id( new_id)

@pytest.mark.parametrize(
    "new_email, expectation, fixture_name",
    [
        ("hansolo@fakemailcom", pytest.raises(EmailNotValidError), "init_participant"),
        ("hansolofakemail.com", pytest.raises(EmailNotValidError), "init_participant"),
        ("hansolo@@fakemail.com", pytest.raises(EmailNotValidError), "init_participant"),
        ( ["hansolo@fakemail.com"], pytest.raises(AttributeError), "init_participant"),
        ( None , pytest.raises(AttributeError), "init_participant")
    ]
)
def test_wrong_email_raises_type_error( new_email, expectation, fixture_name, request):
    """Test wheter wrong input of email raises exception"""
    model = request.getfixturevalue( fixture_name)

    with expectation:
        model.update_email( new_email)

@pytest.mark.parametrize(
    "new_name, expectation, fixture_name",
    [
        ( 42, pytest.raises(TypeError), "init_participant"),
        ( ["Han", "Solo"], pytest.raises(TypeError), "init_participant"),
        ( ("Han", "Solo"), pytest.raises(TypeError), "init_participant"),
        (  None, pytest.raises(TypeError), "init_participant")
    ]
)
def test_wrong_name_raises_type_error( new_name, expectation, fixture_name, request):
    """Test wheter wrong input of name raises exception"""
    model = request.getfixturevalue( fixture_name)

    with expectation:
        model.update_name( new_name)


@pytest.mark.parametrize(
        "participant_name, participant_email, fixture_name",
        [
            ( "Hans Gruber", "hansgruber@nakatomiplaza.com", "init_participant"  ),
            ( "Karl", "justkarl@nakatomiplaza.com", "init_participant"  ),
            ( "John McClane", "johnmcclane@nakatomiplaza.com", "init_participant"  )
        ]
)
def test_converts_details_correctly_into_table_row(participant_name, participant_email,\
                                                    fixture_name, request):
    """
    test if details of a participant are converted correctly into a table row format 
    """
    model = request.getfixturevalue( fixture_name)
    model.update_name(participant_name)
    model.update_email(participant_email)

    model.convert_to_table_row()

    assert model.table_row[0][1] == model.name
    assert model.table_row[0][2] == model.email
