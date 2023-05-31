"""add fixtures for unittest here to follow the DRY principle"""
from typing import List
from datetime import datetime
from random import randint
from reminding.participant import Participant
from reminding.meeting import Meeting
from reminding.worksheet import Worksheet
import pytest


@pytest.fixture(scope="session")
def init_values():
    """fixture to create random init values shared across tests"""
    random_name = "Han Solo"
    random_email = "hansolo@fakemail.com"
    random_id = 42
    return random_name, random_email, random_id


@pytest.fixture(scope="session")
def init_participant() -> Participant:
    """initializes a random Participant"""
    random_name = "Han Solo"
    random_email = "hansolo@fakemail.com"
    random_id = 42
    return Participant(random_name, random_email, random_id, True)


@pytest.fixture(scope="session")
def create_random_participants() -> List[Participant]:
    """returns a list of participants"""
    random_names = ["Han Solo", "Darth Vader", "Chewbacca"]
    random_emails = [
        "hansolo@fakemail.com",
        "darthvader@fakemail.com",
        "chewbacca@fakemail.com",
    ]
    participants = []
    for i, (name, email) in enumerate(zip(random_names, random_emails)):
        participants.append(Participant(name, email, i, True))
    return participants


@pytest.fixture(scope="function")
def create_random_meetings() -> List[Meeting]:
    """initializes and returns a list of random meeting with random values"""
    random_meetings = []
    num_random_meetings = 2
    for meeting_id in range(num_random_meetings):
        # create random fake participants
        random_names = ["Han Solo", "Darth Vader", "Chewbacca"]
        random_emails = [
            "hansolo@fakemail.com",
            "darthvader@fakemail.com",
            "chewbacca@fakemail.com",
        ]
        random_participants = []
        for i, (name, email) in enumerate(zip(random_names, random_emails)):
            random_participants.append(Participant(name, email, i, True))
        # create random fake meeting with these participants
        random_meeting_id = meeting_id
        random_meeting_name = f"Random Meeting {meeting_id}"
        random_date_time = datetime.now()
        random_meeting_notes = "This is a random note for this meeting \
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
    random_names = ["Hans Gruber", "John McClane", "Tony", "Karl"]
    random_emails = [
        "hansgruber@nakatomiplaza.com",
        "johnmcclane@nakatomiplaza.com",
        "karl@nakatomiplaza.com",
        "tony@nakatomiplaza.com",
    ]
    random_participants = []
    for i, (name, email) in enumerate(zip(random_names, random_emails)):
        random_participants.append(Participant(name, email, i, True))
    random_name = "Christmas Party"
    random_meeting_id = 5
    random_datetime = datetime.strptime("24/12/88 21:00", "%d/%m/%y %H:%M")
    random_notes = "Now I have a machine gun"
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
