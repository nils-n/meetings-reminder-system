"""class to describe a schedule of meetings"""
from dataclasses import dataclass, field
from typing import Union
from datetime import datetime
import gspread
from reminding.meeting import Meeting, Participant
from reminding.worksheet import Worksheet


@dataclass
class Schedule:
    """
    describes a schedule of meetings
    for table rows :how to load a mixed variables into dataclass variables from:
    https://stackoverflow.com/questions/69915050/how-to-make-list-in-python-dataclass-that-can-accept-multiple-different-types
    """

    worksheet: Worksheet
    name: str
    meetings: list[Meeting] = field(default_factory=list)
    table_rows: list[Union[str, int]] = field(default_factory=list)
    allowed_participants: list[Participant] = field(default_factory=list)
    participation_matrix_row_header: list[str] = field(default_factory=list)
    participation_matrix_rows: list[str] = field(default_factory=list)
    offline_mode: bool = False

    def __post_init__(self):
        self.load_allowed_participants()
        self.load_meetings("schedule")
        self.load_participants()
        self.convert_meetings_to_table("All Meetings")

    def load_participants(self):
        """loads all participants stored in the participation matrix"""
        try:
            self.load_participation_matrix()
            for i, meeting in enumerate(self.meetings):
                for j, participant in enumerate(self.allowed_participants):
                    if self.participation_matrix_rows[i][j + 1] in ["TRUE", True, 1]:
                        meeting.participants.append(participant)
        except (gspread.exceptions.APIError, IndexError) as error:
            print(
                f"Could not read data from API (error : {error})\n Loading Mock Meetings instead..."
            )

    def load_meetings(self, worksheet_name):
        """
        currently this loads a hard-coded list of mock meetings
        eventually this will be replaced by reading data from a google worksheet

        how to catch gpsread APIError
        https://stackoverflow.com/questions/66091272/how-to-implement-try-catch-and-get-the-name-and-code-of-the-gspread-error

        """
        if worksheet_name == "Mock Sheet":
            self.load_mock_meetings()
            self.offline_mode = True
            return
        try:
            self.worksheet.load_meetings(worksheet_name)
            self.meetings = self.worksheet.meetings
            self.offline_mode = False
        except gspread.exceptions.APIError as error:
            print(
                f"Could not read data from API (error : {error})\n Loading Mock Meetings instead..."
            )
            self.load_mock_meetings()

    def load_mock_meetings(self):
        """
        load mock meetings
        either for faster unit test or in case of an APIError
        """
        self.meetings = []
        mock_datetime = datetime.strptime("01/01/01 00:00", "%d/%m/%y %H:%M")
        mock_participants = []
        mock_participants.append(self.allowed_participants[0])
        mock_participants.append(self.allowed_participants[1])
        mock_participants.append(self.allowed_participants[2])
        mock_participants.append(self.allowed_participants[3])

        self.add_meeting(
            Meeting(
                1,
                "Mock Meeting 1 ",
                mock_datetime,
                True,
                True,
                mock_participants,
                "",
            )
        )
        self.add_meeting(
            Meeting(
                2,
                "Mock Meeting 2 ",
                mock_datetime,
                True,
                True,
                mock_participants,
                "",
            )
        )

    def push_meetings(self, worksheet_name):
        """pushes all meetings (including all local modifications) to the worksheet"""
        self.worksheet.push_meetings(self.meetings, worksheet_name)

    def push_participation_matrix(self):
        """pushes the participation matrix of all meetings of this schedule"""
        self.worksheet.push_participation_matrix(
            self.participation_matrix_row_header,
            self.participation_matrix_rows,
            "participation-matrix",
        )

    def load_participation_matrix(self):
        """loads the participation matrix as stored in the API"""

        (
            self.participation_matrix_row_header,
            self.participation_matrix_rows,
        ) = self.worksheet.load_participation_matrix(
            "participation-matrix", self.offline_mode
        )

    def load_allowed_participants(self):
        """
        loads all available participants that can be added to a meeting
        eventually this be a google sheet - for now just mock the pool of participants.

        Background: I do not want this application to send Emails to arbitrary locations
        which is potentially a security risk. So, instead, only participants in
        a dedicated Google sheet can be selected, and the Email addresses cannot be modified.
        This could be done with a separete web application, or the user can change it manually.

        Note that this is not an unreasonable assumption: The type of meetings where it makes sense
        to add some automation are anyway repetitive meetings with the same participants.

        It also makes sense to load this on the schedule level - it only needs to load once to
        avoid unnecessary traffic.
        """
        if not self.offline_mode:
            self.allowed_participants = self.worksheet.valid_participants
        else:
            self.allowed_participants = []
            self.allowed_participants.append(
                Participant("Mock Participant 1", "mockemail-1@fakemail.com", 1, True)
            )
            self.allowed_participants.append(
                Participant("Mock Participant 2", "mockemail-2@fakemail.com", 2, True)
            )
            self.allowed_participants.append(
                Participant("Mock Participant 3", "mockemail-3@fakemail.com", 3, True)
            )
            self.allowed_participants.append(
                Participant("Mock Participant 4", "mockemail-4@fakemail.com", 4, True)
            )

    def validate_participant(self, potential_participant):
        """
        checks whether a supplied participant is in the list of allowed participants
        more of a security check to prevent sending emails to arbitrary locations
        """
        if potential_participant not in self.allowed_participants:
            raise ValueError("This is not an allowed participant!")

    def get_allowed_participants_by_id(self, id_numbers):
        """
        returns a list of participants that match one of the id numbers
        """
        return [
            participant
            for participant in self.allowed_participants
            if participant.id_number in id_numbers
        ]

    def add_meeting(self, new_meeting):
        """
        function to add a new meeting to the current schedule
        also updates the table rows for the User Interface
        """
        self.meetings.append(new_meeting)

    def remove_meeting(self, target_id):
        """
        removes a meeting from the schedule via its ID
        """
        self.meetings = [
            meeting for meeting in self.meetings if meeting.meeting_id != int(target_id)
        ]

    def convert_meetings_to_table(self, time_range):
        """
        convert the meetings object into a table format that the TUI can display and update
        """
        self.table_rows = []
        self.table_rows.append(("ID", "Name", "Time", "invited", "confirmed"))
        for meeting in self.meetings:
            if meeting.is_within_time_range(datetime.now(), time_range):
                self.table_rows.append(
                    (
                        meeting.meeting_id,
                        meeting.name,
                        meeting.datetime,
                        len(meeting.participants),
                        meeting.num_participants,
                    )
                )

    def validate_meeting_id(self, target_id) -> None:
        """
        raises a ValueError if the supplied integer cannot be converted to int
        or if it does not match any of the meetings IDs in the schedule
        """
        target_id = int(target_id)
        valid_ids = []
        for meeting in self.meetings:
            valid_ids.append(meeting.meeting_id)
        if target_id not in valid_ids:
            raise ValueError(
                f"The meeting ID should match an existing meeting \
                             ( {target_id} does not match any meeting )"
            )

    def get_meeting_by_id(self, target_id) -> int:
        """
        returns a meeting of a schedule by asking of its ID
        At the time when this function is called it is already checked that a
        meeting with this ID exists - so i am not going to test it again.
        """
        self.validate_meeting_id(target_id)
        for meeting in self.meetings:
            if meeting.meeting_id == target_id:
                return meeting

    def calculate_participation_matrix(self) -> None:
        """
        calculates the participation matrix that maps the allowed participants
        to the current meetings in the schedule

        - the first row contains all allowed participant IDs
        - the first column contains all current meeting IDs
        - if  element (i,j) is True   -->  participant i is participating in meeting j
        - if  element (i,j) is False  -->  participant i is not participating in meeting j
        """

        self.participation_matrix_row_header = ["Meeting ID / Participant ID"] + [
            participant.id_number for participant in self.allowed_participants
        ]
        self.participation_matrix_rows = []
        for meeting in self.meetings:
            self.participation_matrix_rows.append(
                [str(meeting.meeting_id)]
                + [
                    True if (participant in meeting.participants) else False
                    for participant in self.allowed_participants
                ]
            )


def main() -> None:
    """Just a function for manual Testing"""
    model = Schedule(Worksheet("Test Sheet", None), "An example Schedule", [], [])

    print(type(model.meetings))


if __name__ == "__main__":
    main()
