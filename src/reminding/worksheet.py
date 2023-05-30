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
        self.meetings = self.load_meetings("schedule")
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

    def load_meetings(self, worksheet_name) -> list[Meeting]:
        """Load meetings from the worksheet and transfer into a list of Meetings"""
        sheet = SHEET.worksheet(worksheet_name)
        row_list = sheet.get_all_values()
        return [
            Meeting(int(row[0]), row[1], datetime.strptime(row[2], "%d/%m/%y %H:%M"))
            for i, row in enumerate(row_list)
            if i > 0
        ]

    def push_meetings(self, meetings, worksheet_name) -> None:
        """this function replaces all rows on the worksheet with the current meetings"""
        sheet = SHEET.worksheet(worksheet_name)
        sheet.clear()
        header_row = [
            "Meeting ID",
            "Name",
            "Time",
            "Place",
            "Invited",
            "reminder sent?",
        ]
        sheet.append_row(header_row)
        new_rows = [
            [
                str(meeting.meeting_id),
                str(meeting.name),
                meeting.datetime.strftime("%d/%m/%y %H:%M"),
                "",
                str(len(meeting.participants)),
                "no",
            ]
            for meeting in meetings
        ]
        sheet.append_rows(new_rows)

    def add_meeting(self, new_meeting, worksheet_name) -> None:
        """add a meeting to the worksheet"""
        sheet = SHEET.worksheet(worksheet_name)
        meetings = self.load_meetings(worksheet_name)
        if new_meeting not in meetings:
            new_row = [
                str(new_meeting.meeting_id),
                str(new_meeting.name),
                new_meeting.datetime.strftime("%d/%m/%y %H:%M"),
                "",
                str(len(new_meeting.participants)),
                "no",
            ]
            sheet.append_row(new_row)

    def remove_meeting_by_id(self, target_id, worksheet_name) -> None:
        """remove meeting with given ID from worksheet"""
        sheet = SHEET.worksheet(worksheet_name)
        row_list = sheet.get_all_values()
        for i, row in enumerate(row_list):
            if row[0] == str(target_id):
                sheet.delete_rows(i + 1)


def main() -> None:
    data = Worksheet("Test Data", [])
    sheet = data.unittest_sheet
    row_list = sheet.get_all_values()
    print(row_list)
    print(row_list[0])
    print(row_list[1])


if __name__ == "__main__":
    main()
