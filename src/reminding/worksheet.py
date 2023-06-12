"""class to describe I/O to a remote worksheet """
from dataclasses import dataclass, field
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from reminding.participant import Participant
from reminding.meeting import Meeting

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]


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
    schedule_sheet_values: list[list[str]] = field(default_factory=list)
    participation_matrix_sheet_values: list[list[str]] = field(default_factory=list)
    valid_participant_sheet_values: list[list[str]] = field(default_factory=list)
    is_modified: bool = False

    def __post_init__(self) -> None:
        """
        read all values from the google API once and store the data in a local copy.

        Note: during unit test, replace values from schedule sheet with mock data
        """
        self.valid_participants = []

        # this part should be exectuted during a unit test
        if any(
            [
                "Mock" in self.name,
                "mock" in self.name,
                "test" in self.name,
                "Test" in self.name,
            ]
        ):
            self.schedule_sheet_values = self.load_mock_unittest_sheet()
            self.participation_matrix_sheet_values = (
                self.load_mock_participation_matrix_values()
            )
            self.valid_participant_sheet_values = (
                self.load_mock_valid_participant_values()
            )

        else:
            # this part should be exectured during runtime of the app with actual API calls
            # first try to connect to the API
            try:
                self.CREDS = Credentials.from_service_account_file("creds.json")
                self.SCOPED_CREDS = self.CREDS.with_scopes(SCOPE)
                self.GSPREAD_CLIENT = gspread.authorize(self.SCOPED_CREDS)
                self.SHEET = self.GSPREAD_CLIENT.open("Meeting-Reminders")
                self.schedule_sheet_values = self.SHEET.worksheet(
                    "schedule"
                ).get_all_values()
                self.participation_matrix_sheet_values = self.SHEET.worksheet(
                    "participation-matrix"
                ).get_all_values()
                self.valid_participant_sheet_values = self.SHEET.worksheet(
                    "valid-participants"
                ).get_all_values()

            except (FileNotFoundError, gspread.exceptions.APIError):
                # if there is no creds file, use mock data (demo mode)
                self.schedule_sheet_values = self.load_mock_unittest_sheet()
                self.participation_matrix_sheet_values = (
                    self.load_mock_participation_matrix_values()
                )
                self.valid_participant_sheet_values = (
                    self.load_mock_valid_participant_values()
                )

                print(
                    f"Loading Test Data...\
                      \nName of your Sheet   : {self.name}  "
                )
        # fill datastructures used during the App
        self.load_valid_participants()
        self.meetings = self.load_meetings()

    def load_mock_valid_participant_values(self):
        """
        load a set of mock valid participants as if it were read from a worksheet
        Reason for this : to run unit tests without actually calling values from API
        """
        return [
            ["Participant ID", "Name", "Email"],
            ["1", "Test User 1", "student.reminder.test.user+1@gmail.com"],
            ["2", "Test User 2", "student.reminder.test.user+2@gmail.com"],
            ["3", "Test User 3", "student.reminder.test.user+3@gmail.com"],
            ["4", "Test User 4", "student.reminder.test.user+4@gmail.com"],
            ["5", "Test User 5", "student.reminder.test.user+5@gmail.com"],
        ]

    def load_mock_participation_matrix_values(self):
        """
        load how the mock participants participants in the mock meetings
        Reason for this : to run unit tests without actually calling values from API
        """
        return [
            ["Meeting ID / Participant ID", "1", "2", "3", "4", "5"],
            ["1", "TRUE", "TRUE", "TRUE", "TRUE", "TRUE"],
            ["2", "FALSE", "FALSE", "FALSE", "FALSE", "FALSE"],
        ]

    def load_mock_unittest_sheet(self):
        """
        load a set of mock meetings as if they were read from a worksheet
        Reason for this : to run unit tests without actually calling values from APIr
        """
        return [
            ["Meeting ID", "Name", "Time", "Place", "Invited", "reminder sent?"],
            ["1", "Unit Test Meeting 1", "11/11/11 11:11", "", "0", "no"],
            ["2", "Unit Test Meeting 2", "30/05/23 14:00", "", "0", "no"],
        ]

    def load_valid_participants(self) -> None:
        """loads data of valid Participants from google sheet into a list of Participants
        assumes that data are stored in sheet as [ Participant ID - Name - Email ]
        """
        row_list = self.valid_participant_sheet_values
        self.valid_participants = [
            Participant(row[1], row[2], int(row[0]), True, [])
            for i, row in enumerate(row_list)
            if i > 0
        ]

    def is_valid_participant(self, participant) -> None:
        """raises a ValueError if the participant is not on the sheet of valid participants"""
        if participant not in self.valid_participants:
            raise ValueError

    def load_meetings(self) -> list[Meeting]:
        """
        Load meetings from a worksheet and transfer into a list of Meetings
        """
        row_list = self.schedule_sheet_values

        return [
            Meeting(int(row[0]), row[1], datetime.strptime(row[2], "%d/%m/%y %H:%M"))
            for i, row in enumerate(row_list)
            if i > 0
        ]

    def load_participation_matrix(self):
        """loads the participation matrix from the local copy of the worksheet"""
        row_list = self.participation_matrix_sheet_values
        return row_list[0], row_list[1:]

    def push_schedule_to_repository(self) -> None:
        """
        this function uploads the local copy of the worksheet if is has been modified
        """
        if self.is_modified:
            sheet = self.SHEET.worksheet("schedule")
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
                for meeting in self.meetings
            ]
            sheet.append_rows(new_rows)

    def add_meeting(self, new_meeting) -> None:
        """
        adds a meeting to the local copy of the worksheet
        """
        if new_meeting not in self.meetings:
            new_row = [
                str(new_meeting.meeting_id),
                str(new_meeting.name),
                new_meeting.datetime.strftime("%d/%m/%y %H:%M"),
                "",
                str(len(new_meeting.participants)),
                "no",
            ]
            self.schedule_sheet_values.append(new_row)
            self.meetings.append(new_meeting)
            self.is_modified = True

    def remove_meeting_by_id(self, target_id) -> None:
        """remove meeting with given ID from local copy of a worksheet"""
        row_list = self.schedule_sheet_values
        modified_row_list = []
        for row in row_list:
            if row[0] != str(target_id):
                modified_row_list.append(row)
            else:
                self.is_modified = True
        if self.is_modified:
            self.schedule_sheet_values = modified_row_list
            self.meetings = self.load_meetings()

    def push_participation_matrix(self, row_header, new_rows) -> None:
        """
        pushes the current participation matrix to to the worksheet
        Note for later -> this should not work on the online values but rather on the
        local copy and the is_modified flag to True. (to reduce API calls)
        """
        sheet = self.SHEET.worksheet("participation-matrix")
        sheet.clear()
        sheet.append_row(row_header)
        sheet.append_rows(new_rows)

    def check_if_modified(self) -> None:
        """
        Checks if one of the meeting in the sheet is modified. If yes, set state
        of the sheet to modified
        """
        for meeting in self.meetings:
            if meeting.is_modified:
                self.is_modified = True

    def reset_modified_state(self) -> None:
        """
        sets status of worksheet and its meeting to 'not modified'
        this would be called when syncning with repository was successfull
        """
        self.is_modified = False
        for meeting in self.meetings:
            meeting.is_modified = False


def main() -> None:
    """Just a function for manual Testing"""
    data = Worksheet("Mock Sheet", None)
    row_list = data.participation_matrix_sheet_values
    print(row_list)


if __name__ == "__main__":
    main()
