"""
This is a unit test for the worksheet class. 

All unit tests are laid out in the form 

A rrange
A ct 
A ssert

"""
from reminding.worksheet import Worksheet
from reminding.participant import Participant
from reminding.meeting import Meeting
import pytest
from contextlib import nullcontext as does_not_raise
from datetime import datetime


def xtest_can_create_new_worksheet() -> None:
    """test if a new worksheet can be created"""

    model = Worksheet("Test Sheet", None)

    assert isinstance(model, Worksheet)


def xtest_can_read_values_from_worksheet(load_worksheet) -> None:
    """test if the class can read values from worksheet"""
    data = load_worksheet
    model = data.schedule_sheet.get_all_values()

    assert model[1][1] == "Christmas Party"
    assert model[1][2] == "24/12/23 21:00"
    assert model[1][3] == "Nakatomi Plaza"


def xtest_can_read_all_valid_participants_from_worksheet(load_worksheet) -> None:
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
def xtest_invalid_participant_should_raise_ValueError(
    fixture_name, participant, expectation, request
) -> None:
    """Test wheter an participant that is not on the list of allowed /
    validated participants raises a ValueError"""
    model = request.getfixturevalue(fixture_name)
    model.load_valid_participants()

    with expectation:
        model.is_valid_participant(participant)


def xtest_can_read_meetings_from_worksheet(load_worksheet) -> None:
    """
    this is a bit tricky: what to test first, reading or writing a meeting?
    If we test read first -> How do we know during unit test what to expect on the editable sheet?
    If we test write first -> How do we know during unit test that we actually edited the sheet correctly?

    This could be done by mocking a database and i will explore that option in future.

    Another option is to connect to a known database and test the code with those sheets:
    https://stackoverflow.com/questions/1217736/how-to-write-unit-tests-for-database-calls

    I modify this idea by adding a fourth sheet 'unit-test' to our google sheet that is not used by the app,
    just for the unit test, using same columns as the first (schedule) sheet. then i would assume:
    if i can read/write to the fourth sheet, it should work for the first and second as well.
    """
    unit_test_meetings = [
        Meeting(
            1,
            "Unit Test Meeting 1",
            datetime.strptime("11/11/11 11:11", "%d/%m/%y %H:%M"),
        ),
        Meeting(
            2,
            "Unit Test Meeting 2",
            datetime.strptime("30/05/23 14:00", "%d/%m/%y %H:%M"),
        ),
    ]

    model = load_worksheet
    model.load_meetings("unit-test")

    assert model.meetings[0] == unit_test_meetings[0]
    assert model.meetings[1] == unit_test_meetings[1]


def test_can_add_meeting_to_worksheet(load_worksheet) -> None:
    """
    this is a test if the unit test can write a meeting to the worksheet.

    We use the tested reading method (see previous test) to confirm the writing method

    (note: I disabled the other tests to make testing faster)
    """
    model = load_worksheet
    new_meeting = (
        Meeting(
            42,
            "UT Write Method Test",
            datetime.strptime("24/12/00 10:00", "%d/%m/%y %H:%M"),
        ),
    )

    model.add_meeting(new_meeting, "unit-test")
    model.load_meetings("unit-test")

    assert new_meeting in model.meetings
