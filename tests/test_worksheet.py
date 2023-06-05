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


def test_can_create_new_worksheet(load_mock_worksheet) -> None:
    """test if a new worksheet can be created"""
    model = load_mock_worksheet

    assert isinstance(model, Worksheet)


def test_can_read_values_from_worksheet(load_mock_worksheet) -> None:
    """test if the class can read values from worksheet"""
    data = load_mock_worksheet
    model = data.schedule_sheet_values

    assert model[1][1] == "Unit Test Meeting 1"
    assert model[1][2] == "11/11/11 11:11"


def test_can_read_all_valid_participants_from_worksheet(load_mock_worksheet) -> None:
    """test if the class can read all valid particpants from the worksheet"""

    valid_participants = [
        Participant(
            f"Test User {i}", f"student.reminder.test.user+{i}@gmail.com", i, True, []
        )
        for i in range(1, 5)
    ]

    model = load_mock_worksheet
    model.load_valid_participants()

    assert model.valid_participants[0] == valid_participants[0]
    assert model.valid_participants[1] == valid_participants[1]


@pytest.mark.parametrize(
    "fixture_name, participant, expectation",
    [
        (
            "load_mock_worksheet",
            Participant(
                "Test User 1", "student.reminder.test.user+1@gmail.com", 1, True, []
            ),
            does_not_raise(),
        ),
        (
            "load_mock_worksheet",
            Participant(
                "Test User 2", "student.reminder.test.user+2@gmail.com", 2, True, []
            ),
            does_not_raise(),
        ),
        (
            "load_mock_worksheet",
            Participant(
                "Test User 42", "student.reminder.test.user+42@gmail.com", 42, True, []
            ),
            pytest.raises(ValueError),
        ),
    ],
)
def test_invalid_participant_should_raise_value_error(
    fixture_name, participant, expectation, request
) -> None:
    """Test wheter an participant that is not on the list of allowed /
    validated participants raises a ValueError"""
    model = request.getfixturevalue(fixture_name)
    model.load_valid_participants()

    with expectation:
        model.is_valid_participant(participant)


def test_can_read_meetings_from_worksheet(load_mock_worksheet) -> None:
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

    Update (5 june 2023): While the idea above was not bad per se, it lead to a violation of Googles Terms and
    Serives by using the API for spam-like usage, see  https://developers.google.com/terms
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

    model = load_mock_worksheet
    meetings = model.load_meetings()

    assert meetings[0] == unit_test_meetings[0]
    assert meetings[1] == unit_test_meetings[1]


def test_can_add_meeting_to_worksheet(load_mock_worksheet) -> None:
    """
    this is a test if the unit test can write a meeting to the worksheet.

    We use the tested reading method (see previous test) to confirm the writing method

    """
    model = load_mock_worksheet
    new_meeting = Meeting(
        42,
        "UT Write Method Test",
        datetime.strptime("24/12/00 10:00", "%d/%m/%y %H:%M"),
    )

    model.add_meeting(new_meeting)
    meetings = model.load_meetings()

    assert new_meeting in meetings


def test_can_delete_meeting_by_id_from_worksheet(load_mock_worksheet) -> None:
    """
    this is a test if the unit test can delete a meeting to the worksheet.

    We use the tested methods for reading and writing to test the delete method
    """
    model = load_mock_worksheet
    new_meeting = Meeting(
        42,
        "UT Write Method Test",
        datetime.strptime("24/12/00 10:00", "%d/%m/%y %H:%M"),
    )
    model.add_meeting(new_meeting)
    model.remove_meeting_by_id(42)
    meetings = model.load_meetings()

    assert new_meeting not in meetings


def xtest_can_push_all_local_meetings_to_worksheet(load_mock_sworksheet) -> None:
    """
    This is a test if one can push all local meetings to a worksheet to replace its content

    (note:  this test is disabled because of a design descision to purge all API calls from the unit test)
    """
    model = load_mock_sworksheet
    old_meetings = model.load_meetings()
    new_unit_test_meetings = [
        Meeting(
            44,
            "Modified Meeting 1",
            datetime.strptime("01/01/01 01:00", "%d/%m/%y %H:%M"),
        ),
        Meeting(
            22,
            "Modified Meeting 1",
            datetime.strptime("02/02/02 02:00", "%d/%m/%y %H:%M"),
        ),
    ]

    model.push_meetings(new_unit_test_meetings, "unit-test")
    updated_meetings = model.load_meetings()

    assert updated_meetings == new_unit_test_meetings

    # push back the old meetings
    model.push_meetings(old_meetings, "unit-test")


@pytest.mark.parametrize(
    "fixture_name, participant",
    [
        (
            "load_mock_worksheet",
            Participant(
                "Test User 1", "student.reminder.test.user+1@gmail.com", 1, True
            ),
        ),
        (
            "load_mock_worksheet",
            Participant(
                "Test User 2", "student.reminder.test.user+2@gmail.com", 2, True
            ),
        ),
    ],
)
def test_can_load_mock_participants(fixture_name, participant, request) -> None:
    """
    Test to load mock participants
    """
    model = request.getfixturevalue(fixture_name)
    model.load_valid_participants()

    assert participant in model.valid_participants


@pytest.mark.parametrize(
    "fixture_name, meeting, expected_index",
    [
        (
            "load_mock_worksheet",
            Meeting(
                1,
                "Unit Test Meeting 1",
                datetime.strptime("11/11/11 11:11", "%d/%m/%y %H:%M"),
                True,
                True,
                [],
                "",
            ),
            0,
        ),
        (
            "load_mock_worksheet",
            Meeting(
                2,
                "Unit Test Meeting 2",
                datetime.strptime("30/05/23 14:00", "%d/%m/%y %H:%M"),
                True,
                True,
                [],
                "",
            ),
            1,
        ),
    ],
)
def test_can_load_mock_meetings(fixture_name, meeting, expected_index, request) -> None:
    """
    Test to load mock meetings
    """
    model = request.getfixturevalue(fixture_name)
    model.schedule_sheet_values = model.load_mock_unittest_sheet()

    model.load_meetings()

    assert model.meetings[expected_index].name == meeting.name
