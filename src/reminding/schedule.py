"""class to describe a schedule of meetings"""
from dataclasses import dataclass, field
from typing import Union
from datetime import datetime
from reminding.worksheet import Worksheet


@dataclass
class Schedule:
    """
    describes a schedule of meetings
    for table rows :how to load a mixed variables into dataclass
      variables from:
    https://stackoverflow.com/questions/69915050/how-to-make-list-in-python-dataclass-that-can-accept-multiple-different-types
    """

    worksheet: Worksheet
    name: str
    table_rows: list[Union[str, int]] = field(default_factory=list)
    participation_matrix_row_header: list[str] = field(
        default_factory=list
    )
    participation_matrix_rows: list[str] = field(default_factory=list)

    def __post_init__(self):
        self.load_meetings()
        self.load_allowed_participants()
        self.calculate_participation_matrix()
        self.load_participants()
        self.convert_meetings_to_table("All Meetings")

    def load_participants(self):
        """loads all participants stored in the participation matrix"""
        for i, meeting in enumerate(self.worksheet.meetings):
            for j, participant in enumerate(
                self.worksheet.valid_participants
            ):
                if self.participation_matrix_rows[i][j + 1] in [
                    "TRUE",
                    True,
                    1,
                ]:
                    self.worksheet.meetings[i].add_participant(participant)

    def load_meetings(self):
        """
        loads all meetings form the local copy of the google worksheet
        """
        self.worksheet.load_meetings()

    def push_schedule_to_repository(self):
        """pushes all meetings (including all local modifications) to the
        worksheet"""
        self.worksheet.push_schedule_to_repository()

    def push_participation_matrix_to_repository(self):
        """pushes the participation matrix of all meetings of this schedule"""
        self.worksheet.push_participation_matrix(
            self.participation_matrix_row_header,
            self.participation_matrix_rows,
        )

    def load_participation_matrix(self):
        """loads the participation matrix as stored in the API"""
        (
            self.participation_matrix_row_header,
            self.participation_matrix_rows,
        ) = self.worksheet.load_participation_matrix()

    def load_allowed_participants(self):
        """
        loads all valid participants form the local copy of the
          google worksheet
        """
        self.worksheet.load_valid_participants()

    def validate_participant(self, potential_participant):
        """
        checks whether a supplied participant is in the list
          of allowed participants
        more of a security check to prevent sending emails
          to arbitrary locations
        """
        if potential_participant not in self.worksheet.valid_participants:
            raise ValueError("This is not an allowed participant!")

    def get_allowed_participants_by_id(self, id_numbers):
        """
        returns a list of participants that match one of the id numbers
        """
        return [
            participant
            for participant in self.worksheet.valid_participants
            if participant.id_number in id_numbers
        ]

    def add_meeting(self, new_meeting):
        """
        function to add a new meeting to the current schedule
        also updates the table rows for the User Interface
        """
        self.worksheet.add_meeting(new_meeting)
        self.calculate_participation_matrix()

    def remove_meeting(self, target_id):
        """
        removes a meeting from the schedule via its ID
        """
        self.worksheet.remove_meeting_by_id(target_id)
        self.calculate_participation_matrix()

    def convert_meetings_to_table(self, time_range):
        """
        convert the meetings object into a table format that
          the TUI can display and update
        """
        self.table_rows = []
        self.table_rows.append(
            ("ID", "Name", "Time", "invited", "confirmed")
        )
        for meeting in self.worksheet.meetings:
            if meeting.is_within_time_range(datetime.now(), time_range):
                self.table_rows.append(
                    (
                        str(meeting.meeting_id),
                        meeting.name,
                        str(meeting.datetime),
                        str(len(meeting.participants)),
                        str(meeting.num_participants),
                    )
                )

    def validate_meeting_id(self, target_id) -> None:
        """
        raises a ValueError if the supplied integer cannot be converted to int
        or if it does not match any of the meetings IDs in the schedule
        """
        target_id = int(target_id)
        valid_ids = []
        for meeting in self.worksheet.meetings:
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
        for meeting in self.worksheet.meetings:
            if meeting.meeting_id == target_id:
                return meeting

    def calculate_participation_matrix(self) -> None:
        """
        calculates the participation matrix that maps the allowed participants
        to the current meetings in the schedule

        - the first row contains all allowed participant IDs
        - the first column contains all current meeting IDs
        - if  element (i,j) is True  --> participant i is in meeting j
        - if  element (i,j) is False --> participant i is not in meeting j
        """

        self.participation_matrix_row_header = [
            "Meeting ID / Participant ID"
        ] + [
            participant.id_number
            for participant in self.worksheet.valid_participants
        ]
        self.participation_matrix_rows = []
        for meeting in self.worksheet.meetings:
            self.participation_matrix_rows.append(
                [str(meeting.meeting_id)]
                + [
                    True
                    if (participant in meeting.participants)
                    else False
                    for participant in self.worksheet.valid_participants
                ]
            )
