"""add fixtures for unittest here to follow the DRY principle"""
from typing import List
from datetime import datetime
import pytest
from reminding.participant import Participant
from reminding.meeting import Meeting
from reminding.worksheet import Worksheet


@pytest.fixture(scope="session")
def init_values():
    """fixture to create random init values shared across tests"""
    random_name = "Test User 1"
    random_email = "test.user+1@test.com"
    random_id = 1
    return random_name, random_email, random_id


@pytest.fixture(scope="session")
def init_participant() -> Participant:
    """initializes a random Participant"""
    random_name = "Test User 1"
    random_email = "test.user+1@test.com"
    random_id = 1
    return Participant(random_name, random_email, random_id, True)


@pytest.fixture(scope="session")
def create_random_participants() -> List[Participant]:
    """returns a list of participants"""
    number_of_random_participants = 2
    random_names = [f"Test User {i}" for i in range(number_of_random_participants)]
    random_emails = [
        f"test.user+{i}@test.com" for i in range(number_of_random_participants)
    ]
    participants = []
    for i, (name, email) in enumerate(zip(random_names, random_emails)):
        participants.append(Participant(name, email, i, True))
    return participants


@pytest.fixture(scope="function")
def create_random_meetings() -> List[Meeting]:
    """initializes and returns a list of random meeting with random values"""
    random_meetings = []
    number_of_random_meetings = 2
    number_of_random_participants = 4
    for meeting_id in range(number_of_random_meetings):
        # create random fake participants
        random_names = [f"Test User {i}" for i in range(number_of_random_participants)]
        random_emails = [
            f"test.user+{i}@test.com" for i in range(number_of_random_participants)
        ]
        random_participants = []
        for i, (name, email) in enumerate(zip(random_names, random_emails)):
            random_participants.append(Participant(name, email, i, True))
        # create random fake meeting with these participants
        random_meeting_id = meeting_id
        random_meeting_name = f"Test Meeting {meeting_id}"
        random_date_time = datetime.now()
        random_meeting_notes = "This is a test note for this meeting \
            to be sent along with the reminder. "
        random_meetings.append(
            Meeting(
                random_meeting_id,
                random_meeting_name,
                random_date_time,
                True,
                True,
                random_participants,
                random_meeting_notes,
            )
        )
    return random_meetings


@pytest.fixture(scope="function")
def create_random_meeting() -> Meeting:
    """initialize a random meeting with a few random participants"""
    random_number_of_participants = 4
    random_names = [f"Test User {i}" for i in range(random_number_of_participants)]
    random_emails = [
        f"test.user+{i}@test.com" for i in range(random_number_of_participants)
    ]
    random_participants = []
    for i, (name, email) in enumerate(zip(random_names, random_emails)):
        random_participants.append(Participant(name, email, i, True))
    random_name = "Test Meeting"
    random_meeting_id = 5
    random_datetime = datetime.strptime("01/01/01 00:00", "%d/%m/%y %H:%M")
    random_notes = "This is just a Test"
    random_meeting = Meeting(
        random_meeting_id, random_name, random_datetime, True, True, [], random_notes
    )
    for participant in random_participants:
        random_meeting.add_participant(participant)

    return random_meeting


@pytest.fixture(scope="session")
def load_worksheet() -> Worksheet:
    """initialize and load the spreadsheet from the cloud once for all tests"""
    return Worksheet("Test Sheet", None)


@pytest.fixture(scope="session")
def load_mock_worksheet() -> Worksheet:
    """
    initialize a spreadsheet that does not depend on values from the cloud
    to reduce API requests per minutes
    """
    return Worksheet("Mock Sheet", None)
