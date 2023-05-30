from dataclasses import dataclass, field
from reminding.participant import Participant
from reminding.meeting import Meeting
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("Meeting-Reminders")


@dataclass
class Worksheet:
    """
    This class handles the read and write access to google sheet
    so that changes after closing the program are permanent
    """

    name: str
    schedule_sheet: gspread.Worksheet
    valid_participants: list[Participant] = field(default_factory=list)
    meetings: list[Meeting] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.schedule_sheet = SHEET.worksheet("schedule")
        self.valid_participants_sheet = SHEET.worksheet("valid-participants")
        self.load_valid_participants()
        self.unittest_sheet = SHEET.worksheet("unit-test")

    def load_valid_participants(self) -> None:
        """loads data of valid Participants from google sheet into a list of Participants
        assumes that data are stored in sheet as [ Participant ID - Name - Email ]
        """
        row_list = self.valid_participants_sheet.get_all_values()
        self.valid_participants = [
            Participant(row[1], row[2], int(row[0]), True, [])
            for i, row in enumerate(row_list)
            if i > 0
        ]

    def is_valid_participant(self, participant) -> None:
        """raises a ValueError if the participant is not on the sheet of valid participants"""
        if participant not in self.valid_participants:
            raise ValueError

    def load_meetings(self, worksheet_name) -> None:
        """Load meetings from the worksheet and transfer into a list of Meetings"""
        row_list = self.unittest_sheet.get_all_values()
        self.meetings = [
            Meeting(int(row[0]), row[1], datetime.strptime(row[2], "%d/%m/%y %H:%M"))
            for i, row in enumerate(row_list)
            if i > 0
        ]

    def add_meeting(self, new_meeting, worksheet_name) -> None:
        """add a meeting to the worksheet"""
        pass


def main() -> None:
    data = Worksheet("Test Data", [])
    print(data.valid_participants)


if __name__ == "__main__":
    main()
