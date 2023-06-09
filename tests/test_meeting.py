"""
This is a unit test for the participant class.

All unit tests are laid out in the form

A rrange
A ct
A ssert

"""
from datetime import datetime
from contextlib import nullcontext as does_not_raise
import pytest
from reminding.meeting import Meeting, Participant


def test_can_create_new_meeting(create_random_participants) -> None:
    """Test if a meeting instance can be created"""
    participants = create_random_participants
    random_meeting_name = "Journal Club"
    random_meeting_id = 42
    random_date_time = datetime.now()
    random_meeting_notes = "This is a random note for this meeting \
        to be sent along with the reminder. "

    model = Meeting(
        random_meeting_id,
        random_meeting_name,
        random_date_time,
        True,
        True,
        participants,
        random_meeting_notes,
    )

    assert isinstance(model, Meeting)


@pytest.mark.parametrize(
    "fixture_name, new_name, expectation",
    [
        ("create_random_participants", "Test Meeting 1", does_not_raise()),
        ("create_random_participants", "Test Meeting 2", does_not_raise()),
        ("create_random_participants", 42, pytest.raises(TypeError)),
    ],
)
def test_invalid_name_raises_type_error(
    fixture_name, new_name, expectation, request
):
    """test various correct and incorrect meeting names"""
    participants = request.getfixturevalue(fixture_name)
    random_meeting_id = 42
    random_date_time = datetime.now()
    random_meeting_notes = "This is a random note for this meeting."

    with expectation:
        Meeting(
            random_meeting_id,
            new_name,
            random_date_time,
            True,
            True,
            participants,
            random_meeting_notes,
        )


@pytest.mark.parametrize(
    "fixture_name, new_id, expectation",
    [
        ("create_random_participants", 1, does_not_raise()),
        ("create_random_participants", 1044, does_not_raise()),
        ("create_random_participants", "42", pytest.raises(TypeError)),
        ("create_random_participants", None, pytest.raises(TypeError)),
        ("create_random_participants", -1, pytest.raises(ValueError)),
    ],
)
def test_invalid_id_raises_type_error(
    fixture_name, new_id, expectation, request
):
    """test various correct and incorrect meeting IDs"""
    participants = request.getfixturevalue(fixture_name)
    random_name = "R2D2"
    random_date_time = datetime.now()
    random_meeting_notes = "This is a random note for this meeting."

    with expectation:
        Meeting(
            new_id,
            random_name,
            random_date_time,
            True,
            True,
            participants,
            random_meeting_notes,
        )


@pytest.mark.parametrize(
    "fixture_name, notification_value, expectation",
    [
        ("create_random_participants", True, does_not_raise()),
        ("create_random_participants", "True", pytest.raises(TypeError)),
        (
            "create_random_participants",
            [
                True,
            ],
            pytest.raises(TypeError),
        ),
        ("create_random_participants", None, pytest.raises(TypeError)),
    ],
)
def test_invalid_notification_flag_raises_type_error(
    fixture_name, notification_value, expectation, request
):
    """ensure that notification flag is a bool type"""
    participants = request.getfixturevalue(fixture_name)
    random_name = "Random Name"
    random_meeting_id = 42
    random_date_time = datetime.now()
    random_meeting_notes = "This is a random note for this meeting."

    with expectation:
        Meeting(
            random_meeting_id,
            random_name,
            random_date_time,
            notification_value,
            True,
            participants,
            random_meeting_notes,
        )


@pytest.mark.parametrize(
    "fixture_name, new_time, expectation",
    [
        (
            "create_random_participants",
            datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M"),
            does_not_raise(),
        ),
        ("create_random_participants", datetime.now(), does_not_raise()),
        (
            "create_random_participants",
            "00/00/00 00:00",
            pytest.raises(TypeError),
        ),
    ],
)
def test_invalid_time_raises_type_error(
    fixture_name, new_time, expectation, request
):
    """ensure that meeting time is correct datetime type"""
    participants = request.getfixturevalue(fixture_name)
    random_name = "Random Name"
    random_meeting_id = 42
    random_meeting_notes = "This is a random note for this meeting."

    with expectation:
        Meeting(
            random_meeting_id,
            random_name,
            new_time,
            True,
            True,
            participants,
            random_meeting_notes,
        )


@pytest.mark.parametrize(
    "fixture_name, new_room_flag, expectation",
    [
        ("create_random_participants", True, does_not_raise()),
        ("create_random_participants", False, does_not_raise()),
        (
            "create_random_participants",
            [
                True,
            ],
            pytest.raises(TypeError),
        ),
        ("create_random_participants", None, pytest.raises(TypeError)),
        ("create_random_participants", 42, pytest.raises(TypeError)),
        (
            "create_random_participants",
            ["A", "List", "of", "strings"],
            pytest.raises(TypeError),
        ),
    ],
)
def test_invalid_room_flag_raises_type_error(
    fixture_name, new_room_flag, expectation, request
):
    """ensure that room flag is a bool type"""
    participants = request.getfixturevalue(fixture_name)
    random_name = "Random Name"
    random_meeting_id = 42
    random_time = datetime.now()
    random_meeting_notes = "This is a random note for this meeting."

    with expectation:
        Meeting(
            random_meeting_id,
            random_name,
            random_time,
            True,
            new_room_flag,
            participants,
            random_meeting_notes,
        )


@pytest.mark.parametrize(
    "fixture_name, new_notes, expectation",
    [
        ("create_random_participants", "", does_not_raise()),
        ("create_random_participants", "This is a note", does_not_raise()),
        (
            "create_random_participants",
            "This is also a note",
            does_not_raise(),
        ),
        ("create_random_participants", None, pytest.raises(TypeError)),
        ("create_random_participants", 1, pytest.raises(TypeError)),
    ],
)
def test_invalid_meeting_notes_raises_type_error(
    fixture_name, new_notes, expectation, request
):
    """test that invalid meeting notes raise type error"""
    participants = request.getfixturevalue(fixture_name)
    random_name = "Random Name"
    random_meeting_id = 42
    random_time = datetime.now()

    with expectation:
        Meeting(
            random_meeting_id,
            random_name,
            random_time,
            True,
            True,
            participants,
            new_notes,
        )


def test_meeting_values_convert_correctly_to_table_row(
    create_random_participants,
) -> None:
    """
    Test if meeting values are converted correctly to DataTable row
    """
    participants = create_random_participants
    random_name = "Random Name"
    random_meeting_id = 42
    random_time = datetime.now()
    random_notes = "This is a random note"

    model = Meeting(
        random_meeting_id,
        random_name,
        random_time,
        True,
        True,
        participants,
        random_notes,
    )

    assert model.table_row[0][0] == "ID"
    assert (
        0 < model.table_row[1][0] < 1000
    )  # ensure that model.meeting_id is between 0 and 1000
    assert model.table_row[0][1] == "Name"
    assert model.table_row[1][1] == model.name


@pytest.mark.parametrize(
    "fixture_name, input_time_str, expectation",
    [
        ("create_random_participants", "23/05/23 10:00", does_not_raise()),
        (
            "create_random_participants",
            "23/05/2023 10:00",
            pytest.raises(ValueError),
        ),
        (
            "create_random_participants",
            "23/05/2023",
            pytest.raises(ValueError),
        ),
        (
            "create_random_participants",
            "23.05.23 10:00",
            pytest.raises(ValueError),
        ),
        ("create_random_participants", "", pytest.raises(ValueError)),
        ("create_random_participants", -1, pytest.raises(TypeError)),
    ],
)
def test_user_input_for_meeting_time_can_be_converted_to_datetime(
    fixture_name, input_time_str, expectation, request
) -> None:
    """
    Test if wrong user input of meeting time raises correct errors
    """
    participants = request.getfixturevalue(fixture_name)
    random_name = "Random Name"
    random_meeting_id = 42
    random_time = datetime.now()
    random_notes = "This is a random note"
    model = Meeting(
        random_meeting_id,
        random_name,
        random_time,
        True,
        True,
        participants,
        random_notes,
    )

    with expectation:
        model.validate_meeting_time_string(input_time_str)


def test_add_participants_to_meeting(create_random_meeting) -> None:
    """Test if participants can be added to an existing meeting"""
    model = create_random_meeting
    num_added_participants = 10
    for i in range(num_added_participants):
        model.add_participant(
            Participant(
                f"Test Participant {i}",
                f"testemail-{i}@fakemail.com",
                i,
                True,
                [],
            )
        )

    assert model.num_participants == len(model.participants)
    for i, participant in enumerate(model.participants):
        assert participant.name == model.participants[i].name


def test_participant_table_rows_match_values_of_corresponding_participants(
    create_random_meeting,
) -> None:
    """
    Test if participant values are converted correctly to DataTable rows
    """
    model = create_random_meeting

    model.convert_participants_to_table()

    assert model.participant_table_rows[0][0] == "ID"
    assert model.participant_table_rows[0][1] == "Name"
    assert model.participant_table_rows[0][2] == "Email"
    assert model.participant_table_rows[0][3] == "confirmed"
    for i, participant in enumerate(model.participants):
        assert (
            model.participant_table_rows[i + 1][0] == participant.id_number
        )
        assert model.participant_table_rows[i + 1][1] == participant.name
        assert model.participant_table_rows[i + 1][2] == participant.email


def test_can_remove_participant_from_a_meeting_via_its_id(
    create_random_meeting,
) -> None:
    """
    Test if participant can be removed from a meeting
    """
    model = create_random_meeting
    random_participant = 1
    target_participant_id = model.participants[
        random_participant
    ].id_number

    model.remove_participant_by_id(target_participant_id)

    for participant in model.participants:
        assert participant.id_number != target_participant_id


@pytest.mark.parametrize(
    "fixture_name, input_id, expectation",
    [
        ("create_random_meeting", 1, does_not_raise()),
        ("create_random_meeting", 2, does_not_raise()),
        ("create_random_meeting", 500000, pytest.raises(ValueError)),
    ],
)
def test_removing_participant_with_wrong_id_raises_error(
    fixture_name, input_id, expectation, request
) -> None:
    """
    Test if trying to remove a participant from a meeting that it is not part
    of
    raises the correct exception (and warning to the user)
    """
    model = request.getfixturevalue(fixture_name)

    with expectation:
        model.remove_participant_by_id(input_id)


@pytest.mark.parametrize(
    "fixture_name, time_range, meeting_time, current_time, expectation",
    [
        (
            "create_random_meeting",
            "Week",
            datetime.strptime("10/01/01 00:00", "%d/%m/%y %H:%M"),
            datetime.strptime("01/01/01 00:00", "%d/%m/%y %H:%M"),
            False,
        ),
        (
            "create_random_meeting",
            "Month",
            datetime.strptime("10/01/01 00:00", "%d/%m/%y %H:%M"),
            datetime.strptime("01/01/01 00:00", "%d/%m/%y %H:%M"),
            True,
        ),
        (
            "create_random_meeting",
            "All Meetings",
            datetime.strptime("10/01/01 00:00", "%d/%m/%y %H:%M"),
            datetime.strptime("01/01/01 00:00", "%d/%m/%y %H:%M"),
            True,
        ),
        (
            "create_random_meeting",
            "Week",
            datetime.strptime("10/01/01 00:00", "%d/%m/%y %H:%M"),
            datetime.strptime("09/01/01 00:00", "%d/%m/%y %H:%M"),
            True,
        ),
        (
            "create_random_meeting",
            "Month",
            datetime.strptime("10/01/01 00:00", "%d/%m/%y %H:%M"),
            datetime.strptime("09/01/01 00:00", "%d/%m/%y %H:%M"),
            True,
        ),
        (
            "create_random_meeting",
            "All Meetings",
            datetime.strptime("10/01/01 00:00", "%d/%m/%y %H:%M"),
            datetime.strptime("09/01/01 00:00", "%d/%m/%y %H:%M"),
            True,
        ),
        (
            "create_random_meeting",
            "Week",
            datetime.strptime("10/01/01 00:00", "%d/%m/%y %H:%M"),
            datetime.strptime("11/01/85 00:00", "%d/%m/%y %H:%M"),
            False,
        ),
        (
            "create_random_meeting",
            "Month",
            datetime.strptime("10/01/01 00:00", "%d/%m/%y %H:%M"),
            datetime.strptime("11/01/85 00:00", "%d/%m/%y %H:%M"),
            False,
        ),
        (
            "create_random_meeting",
            "All Meetings",
            datetime.strptime("10/01/01 00:00", "%d/%m/%y %H:%M"),
            datetime.strptime("11/01/85 00:00", "%d/%m/%y %H:%M"),
            True,
        ),
    ],
)
def test_can_tell_if_meeting_is_within_time_range(
    fixture_name,
    time_range,
    meeting_time,
    current_time,
    expectation,
    request,
):
    """Tests whether a meeting correctly returns True if the meeting is
    within a given time range,
    and False when the meeting is not"""
    model = request.getfixturevalue(fixture_name)
    model.validate_meeting_time(meeting_time)

    result = model.is_within_time_range(current_time, time_range)

    assert result == expectation


@pytest.mark.parametrize(
    "fixture_name, new_participant, expectation",
    [
        (
            "create_random_meeting",
            Participant(
                "New Participant 1", "new-email+1@test.com", 42, True
            ),
            True,
        ),
        (
            "create_random_meeting",
            Participant(
                "New Participant 2", "new-email+2@test.com", 42, True
            ),
            True,
        ),
        (
            "create_random_meeting",
            Participant("Test User 1", "test.user+1@test.com", 1, True),
            False,
        ),
    ],
)
def test_adding_new_participant_changes_meeting_state_to_modified(
    fixture_name, new_participant, expectation, request
):
    """
    test whether adding a participant to a meeting changes it
      state to 'modified'
    """
    model = request.getfixturevalue(fixture_name)

    model.add_participant(new_participant)

    assert model.is_modified is expectation


@pytest.mark.parametrize(
    "fixture_name, target_id, expectation",
    [
        ("create_random_meeting", 1, True),
        ("create_random_meeting", 2, True),
    ],
)
def test_removing_valid_participant_changes_meeting_state_to_modified(
    fixture_name, target_id, expectation, request
):
    """
    test whether remove a participant with a valid ID changes meeting
    state to modified
    """
    model = request.getfixturevalue(fixture_name)

    model.remove_participant_by_id(target_id)

    assert model.is_modified is expectation


@pytest.mark.parametrize(
    "fixture_name, new_time, expectation",
    [
        (
            "create_random_meeting",
            datetime.strptime("21/11/06 16:30", "%d/%m/%y %H:%M"),
            True,
        ),
        (
            "create_random_meeting",
            datetime.strptime("01/01/01 00:00", "%d/%m/%y %H:%M"),
            False,
        ),
    ],
)
def test_changing_meeting_time_changes_state_to_modified(
    fixture_name, new_time, expectation, request
):
    """Test whether changing meeting time changes meeting state to
    'is_modified'"""
    model = request.getfixturevalue(fixture_name)

    model.validate_meeting_time(new_time)

    assert model.is_modified == expectation


@pytest.mark.parametrize(
    "fixture_name, new_name, expectation",
    [
        ("create_random_meeting", "New Meeting Name", True),
        ("create_random_meeting", "Test Meeting", False),
    ],
)
def test_changing_meeting_name_changes_state_to_modified(
    fixture_name, new_name, expectation, request
):
    """Test whether changing meeting name changes meeting state
    to 'is_modified'"""
    model = request.getfixturevalue(fixture_name)

    model.validate_name(new_name)

    assert model.is_modified == expectation
