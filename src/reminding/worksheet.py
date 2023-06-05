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
    schedule_sheet_values: list[list[str]] = field(default_factory=list)
    unittest_sheet_values: list[list[str]] = field(default_factory=list)
    participation_matrix_sheet_values: list[list[str]] = field(default_factory=list)
    is_modified: bool = False

    def __post_init__(self) -> None:
        """
        read all values from the google API once and store the data in a local copy.
        This has two advantages :
        -  the API is queried less often
        -  It is also easier to keep track of changes
        """
        try:
            self.load_valid_participants()
            self.meetings = self.load_meetings()
            if self.name == "Test Sheet":
                self.unittest_sheet_values = SHEET.worksheet(
                    "unit-test"
                ).get_all_values()
                return
            self.schedule_sheet_values = SHEET.worksheet("schedule").get_all_values()
            self.participation_matrix_sheet_values = SHEET.worksheet(
                "valid-participants"
            ).get_all_values()
            self.meetings = self.load_meetings()
        except gspread.exceptions.APIError:
            self.valid_participants = []
            self.load_mock_participants()
            self.load_mock_meetings()

    def load_mock_participants(self):
        """load mock participants
        either for faster unit tests or in case of an APIError
        """
        self.valid_participants = [
            Participant(f"Mock Participant {i}", f"mockemail-{i}@testmail.com", i, True)
            for i in range(1, 5)
        ]

    def load_mock_meetings(self):
        """
        load mock meetings
        either for faster unit tests or in case of an APIError
        """
        self.meetings = []
        self.load_mock_participants()

        mock_datetime = datetime.strptime("01/01/01 00:00", "%d/%m/%y %H:%M")
        mock_participants = self.valid_participants

        self.meetings = [
            Meeting(
                i + 1,
                f"Mock Meeting {i+1}",
                mock_datetime,
                True,
                True,
                mock_participants,
                "",
            )
            for i in range(2)
        ]

    def load_valid_participants(self) -> None:
        """loads data of valid Participants from google sheet into a list of Participants
        assumes that data are stored in sheet as [ Participant ID - Name - Email ]
        """
        row_list = self.participation_matrix_sheet_values
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
        Load meetings from the worksheet and transfer into a list of Meetings
        - During the App, load  data from schedule sheet
        - During Unit Test without Mocking, load data from unit-test sheet
        - During Unit Tests with Mocking, create mock data
        """
        if self.name == "Mock Sheet":
            self.load_mock_meetings()
            return self.meetings

        if self.name == "Test Sheet":
            row_list = self.unittest_sheet_values
        else:
            row_list = self.schedule_sheet_values

        return [
            Meeting(int(row[0]), row[1], datetime.strptime(row[2], "%d/%m/%y %H:%M"))
            for i, row in enumerate(row_list)
            if i > 0
        ]

    def load_participation_matrix(self, worksheet_name, offline_mode):
        """loads the participation matrix from the worksheet"""
        if not offline_mode:
            row_list = self.participation_matrix_sheet_values
            return row_list[0], row_list[1:]
        else:
            row_header = [f"{i}" for i in range(len(self.valid_participants))]
            row_entries = []
            for meeting in self.meetings:
                row_entries.append(
                    [
                        "TRUE" if participant in meeting.participants else "FALSE"
                        for participant in self.valid_participants
                    ]
                )
            return row_header, row_entries

    def push_meetings(self, meetings, worksheet_name) -> None:
        """
        this function replaces all rows on the worksheet with the current meetings

        push changes only if your sheet was actually modified (to reduce unnecessary API calls )
        """
        if self.is_modified:
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

    def add_meeting(self, new_meeting) -> None:
        """
        adds a meeting to the local copy of the worksheet

        Note for later -> this should not work on the online values but rather on the
        local copy and the is_modified flag to True. (to reduce API calls)
        in a later version :
         - use sheet.append_row(new_row) to push those changes
         - creates method to push local changes to google sheet
        """
        meetings = self.load_meetings()
        if new_meeting not in meetings:
            new_row = [
                str(new_meeting.meeting_id),
                str(new_meeting.name),
                new_meeting.datetime.strftime("%d/%m/%y %H:%M"),
                "",
                str(len(new_meeting.participants)),
                "no",
            ]
            if self.name == "Test Sheet":
                self.unittest_sheet_values.append(new_row)
            else:
                self.schedule_sheet_values.append(new_row)
            # inform the main app that the local copy now differs from the cloud
            self.is_modified = True

    def remove_meeting_by_id(self, target_id) -> None:
        """remove meeting with given ID from local copy of worksheet
        Note for later -> this should not work on the online values but rather on the
        local copy and the is_modified flag to True. (to reduce API calls)

        in a different function: remove the row on the sheet using
        sheet.delete_rows(i + 1)
        """
        if self.name == "Test Sheet":
            row_list = self.unittest_sheet_values
        else:
            row_list = self.schedule_sheet_values
        modified_row_list = []
        for row in row_list:
            if row[0] != str(target_id):
                modified_row_list.append(row)
            else:
                self.is_modified = True

    def push_participation_matrix(self, row_header, new_rows, worksheet_name) -> None:
        """
        pushes the current participation matrix to to the worksheet
        Note for later -> this should not work on the online values but rather on the
        local copy and the is_modified flag to True. (to reduce API calls)
        """
        sheet = SHEET.worksheet(worksheet_name)
        sheet.clear()
        sheet.append_row(row_header)
        sheet.append_rows(new_rows)

def main() -> None:
    """Just a function for manual Testing"""
    # data = Worksheet("Test Sheet", None)
    # row_list = data.unittest_sheet_values
    data = Worksheet("Schedule Sheet", None)
    row_list = data.schedule_sheet_values
    print(type(row_list))
    print(row_list)
    print(row_list[0])
    print(row_list[1])
    print(f" Meetings in meetings array : {data.meetings}")


if __name__ == "__main__":
    main()
