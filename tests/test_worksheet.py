"""
This is a unit test for the worksheet class. 

All unit tests are laid out in the form 

A rrange
A ct 
A ssert

"""
from reminding.worksheet import Worksheet
from reminding.participant import Participant
import pytest
from contextlib import nullcontext as does_not_raise


def test_can_create_new_worksheet() -> None:
    """test if a new worksheet can be created"""

    model = Worksheet("Test Sheet", None)

    assert isinstance(model, Worksheet)


def test_can_read_values_from_worksheet(load_worksheet) -> None:
    """test if the class can read values from worksheet"""
    data = load_worksheet
    model = data.schedule_sheet.get_all_values()

    assert model[1][1] == "Christmas Party"
    assert model[1][2] == "24/12/23 21:00"
    assert model[1][3] == "Nakatomi Plaza"


def test_can_read_all_valid_participants_from_worksheet(load_worksheet) -> None:
    """test if the class can read all valid particpants from the worksheet"""
    valid_participants = [
        Participant("Mock Participant 1", "mockemail-1@fakemail.com", 1, True, []),
        Participant("Mock Participant 2", "mockemail-2@fakemail.com", 2, True, []),
    ]

    model = load_worksheet
    model.load_valid_participants()

    assert model.valid_participants[0] == valid_participants[0]
    assert model.valid_participants[1] == valid_participants[1]


@pytest.mark.parametrize(
    "fixture_name, participant, expectation",
    [
        (
            "load_worksheet",
            Participant("Mock Participant 1", "mockemail-1@fakemail.com", 1, True, []),
            does_not_raise(),
        ),
        (
            "load_worksheet",
            Participant("Mock Participant 2", "mockemail-2@fakemail.com", 2, True, []),
            does_not_raise(),
        ),
        (
            "load_worksheet",
            Participant("Elsa", "elsa@snowmail.com", 42, True, []),
            pytest.raises(ValueError),
        ),
        (
            "load_worksheet",
            Participant("Olaf", "olaf@snowmail.com", 100, True, []),
            pytest.raises(ValueError),
        ),
    ],
)
def test_invalid_participant_should_raise_ValueError(
    fixture_name, participant, expectation, request
) -> None:
    """Test wheter an participant that is not on the list of allowed /
    validated participants raises a ValueError"""
    model = request.getfixturevalue(fixture_name)
    model.load_valid_participants()

    with expectation:
        model.is_valid_participant(participant)
