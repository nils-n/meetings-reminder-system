""" 
The screens are moved into this sepearate file to keep main (run.py) better readable

The starting point for this app was the Stopwatch Example of the Textualize Tutorial:
https://textual.textualize.io/tutorial/

Explanation that helped me understand how to use screens with textualize: 
https://textual.textualize.io/guide/screens/

All Widgets (such as Checkbox, Grid, Input, DataTable or reactive attribues) were based on 
the Textualize documentation and then modified to fit the needs of this app. 
Starting point for widgets : 
https://textual.textualize.io/widget_gallery/

"""
from itertools import cycle
from datetime import datetime
from textual.app import ComposeResult
from textual.widgets import (
    Header,
    Input,
    DataTable,
    Markdown,
    Button,
    Label,
)
from textual.widgets import Checkbox
from textual.reactive import var
from textual.screen import ModalScreen
from textual.containers import Grid, VerticalScroll, Vertical, Horizontal
from reminding.meeting import Meeting

INPUT_MARKDOWN = """\
# Meeting Manager 

Enter Details for New Meeting. Use *TAB* key to focus input
- Date Format DD/MM/YY
- Time Format HH:MM

"""

cursors = cycle(["column", "row", "cell"])


class WarningScreen(ModalScreen[None]):
    """Warning Widget that pops up when user input is invalid"""

    def __init__(self, message: str = "Input is invalid") -> None:
        self.error_message = message
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Label(f"{self.error_message}", id="invalid-input-msg")
        yield Grid(
            Button("Try again", variant="error", id="return-to-previous"),
            classes="dialog",
        )

    def on_button_pressed(self) -> None:
        """return to previous input screen"""
        self.app.pop_screen()


class NotificationScreen(ModalScreen[None]):
    """Notification dialog that pops up on top of current screen"""

    def __init__(self, message: str = "Operation was successful.") -> None:
        self.notification_message = message
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Label(f"{self.notification_message}", id="valid-input-msg")
        yield Grid(
            Button("OK", variant="primary", id="return-to-previous"),
            classes="dialog",
        )

    def on_button_pressed(self) -> None:
        """return to previous input screen"""
        self.app.pop_screen()


class InputMeeting(ModalScreen[Meeting]):
    """Screen with Input Dialog to enter details of a new Meeting"""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Markdown(INPUT_MARKDOWN)
        yield Vertical(
            Input(
                placeholder="Enter Meeting Name",
                id="input-name",
                classes="columns",
            ),
            Input(placeholder="DD/MM/YY", id="input-date", classes="columns"),
            Input(placeholder="HH:MM", id="input-time", classes="columns"),
            Horizontal(
                Button("Submit", id="submit-input", variant="primary"),
                Button("Go Back", id="not-submit-input", variant="default"),
            ),
            id="meeting-inputs",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """handles button press event on the Input screen"""
        if event.button.id == "submit-input":
            self.on_input_submitted()
        else:
            self.dismiss(False)

    def on_input_submitted(self) -> None:
        """
        retrieve and validate values from input
        --> For now, just display the screen
        """
        new_name = self.query_one("#input-name").value
        new_date = self.query_one("#input-date").value
        new_time = self.query_one("#input-time").value
        new_datetime = f"{new_date} {new_time}"
        new_meeting = Meeting(0, "New Meeting", datetime.now(), True, False, [], "")
        new_meeting.validate_name(new_name)
        try:
            new_meeting.validate_meeting_time_string(new_datetime)
            self.dismiss(new_meeting)

        except (ValueError, TypeError):
            self.app.push_screen(
                WarningScreen(
                    f"Meeting Time invalid ( {new_datetime} is not DD/MM/YY HH:MM )"
                )
            )


class NewMeetingScreen(ModalScreen[Meeting]):
    """Screen with a dialog to enter details of new meeting"""

    new_meeting = var(Meeting(0, "New Meeting", datetime.now(), True, False, [], ""))

    def compose(self) -> ComposeResult:
        yield Label("Do you want to add this meeting?", id="question")
        yield DataTable(id="new-meeting", show_cursor=False)
        yield Grid(
            Button("No", variant="error", id="no", classes="column"),
            Button("Yes", variant="success", id="yes", classes="column"),
            Button("Reset", variant="primary", id="input-data", classes="column"),
            classes="dialog",
        )

    def update_table(self) -> None:
        """updates the displayed table in the TUI with the current values of the Meeting"""
        table = self.query_one("#new-meeting")
        table.clear(columns=True)
        table.cursor_type = next(cursors)
        table.zebra_stripes = True
        rows = self.new_meeting.table_row
        table.add_columns(*rows[0])
        table.add_rows(rows[1:])

    def on_mount(self) -> None:
        """called after mounting to input screen"""
        self.app.push_screen(InputMeeting(), self.check_input)

    def check_input(self, result: Meeting) -> None:
        """
        Callback to get return value from Input Widget
        Called when InputName is popped
        Updates also the displayed Table in the Dialog
        """
        if result is not False:
            self.new_meeting = result
            self.new_meeting.name = result.name
            self.new_meeting.datetime = result.datetime
            self.new_meeting.convert_to_table_row()
            self.update_table()
        else:
            self.app.pop_screen()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """handles button press event"""
        if event.button.id == "input-data":
            self.app.push_screen(InputMeeting(), self.check_input)
        elif event.button.id == "yes":
            self.dismiss(self.new_meeting)
        else:
            self.app.pop_screen()


class ModifyQuestionScreen(ModalScreen[str]):
    """
    Screen to question the user which meeting he or she wants to modify
    """

    def __init__(
        self, message: str = "Which meeting do you want to modify? (Use Meeting ID)"
    ) -> None:
        self.question_message = message
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Label(self.question_message, id="which-meeting")
        yield Grid(
            Input(
                "1",
                placeholder="Input here",
                id="input-which-meeting",
                classes="columns",
            ),
            Button("Confirm", variant="primary", id="which-meeting"),
            Button("Go Back", variant="error", id="never-mind"),
            classes="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """return to previous input screen"""
        if event.button.id == "which-meeting":
            target_meeting_id = self.query_one("#input-which-meeting").value
            self.dismiss(target_meeting_id)
        else:
            self.dismiss(False)


class ModifyMeetingScreen(ModalScreen[int]):
    """Screen with a dialog to update details of a selected meeting"""

    def __init__(self, meeting_id: int) -> None:
        self.target_meeting_id = meeting_id
        self.meeting_to_modify = self.app.schedule.get_meeting_by_id(int(meeting_id))
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Label("What you want to modify of this meeting?", id="question")
        yield DataTable(id="update-meeting", show_cursor=False)
        yield DataTable(id="update-participants", show_cursor=False)
        yield Grid(
            Button("Name", variant="default", id="update-name", classes="column"),
            Button("Time", variant="default", id="update-time", classes="column"),
            Button(
                "Add Participant",
                variant="default",
                id="add-participant",
                classes="column",
            ),
            Button(
                "Remove Participant",
                variant="default",
                id="remove-participant",
                classes="column",
            ),
            Button(
                "Save Changes", variant="primary", id="update-now", classes="column"
            ),
            Button("Go Back", variant="error", id="not-update-now", classes="column"),
            classes="update-dialog",
        )

    def update_meeting_table(self, table_id) -> None:
        """updates the displayed table in the TUI with the current values of the Meeting"""
        table = self.query_one(table_id)
        table.clear(columns=True)
        table.cursor_type = next(cursors)
        table.zebra_stripes = True
        rows = self.meeting_to_modify.table_row
        table.add_columns(*rows[0])
        table.add_rows(rows[1:])

    def update_participants_table(self, table_id) -> None:
        """updates the displayed table in the TUI with the current values of the Meeting"""
        table = self.query_one(table_id)
        table.clear(columns=True)
        table.cursor_type = next(cursors)
        table.zebra_stripes = True
        self.meeting_to_modify.convert_participants_to_table()
        rows = self.meeting_to_modify.participant_table_rows
        table.add_columns(*rows[0])
        table.add_rows(rows[1:])

    def on_mount(self) -> None:
        """called once after mounting the screen"""
        self.update_meeting_table("#update-meeting")
        self.update_participants_table("#update-participants")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """handles button press event"""
        if event.button.id == "update-name":
            self.app.push_screen(
                ModifyQuestionScreen("Enter New Meeting Name for the Meeting:   "),
                self.check_update_meeting_name,
            )
        elif event.button.id == "update-time":
            self.app.push_screen(
                ModifyQuestionScreen(
                    "Enter New Meeting Time for the Meeting: (Format DD/MM/YY HH:MM)   "
                ),
                self.check_update_meeting_time,
            )
        elif event.button.id == "remove-participant":
            self.app.push_screen(
                ModifyQuestionScreen(
                    "Select Which Participant to Remove (Use Participant ID)   "
                ),
                self.check_remove_participant_from_meeting,
            )
        elif event.button.id == "add-participant":
            self.app.push_screen(
                AddParticipantScreen(
                    "Select Which Participant to Add (from the List)   "
                ),
                self.check_add_participant_to_meeting,
            )
        elif event.button.id == "update-now":
            self.dismiss(1)
        else:
            self.dismiss(0)
            # self.app.pop_screen()

    def check_update_meeting_name(self, result: str):
        """
        Callback to update meeting name
        """
        if result is not False:
            try:
                self.meeting_to_modify.validate_name(result)
                self.meeting_to_modify.convert_to_table_row()
                self.update_meeting_table("#update-meeting")
            except (ValueError, TypeError):
                self.app.push_screen(
                    WarningScreen(f"Name is not a string ( Name : {result} )")
                )

    def check_update_meeting_time(self, result: str):
        """
        Callback to update meeting time
        """
        if result is not False:
            try:
                self.meeting_to_modify.validate_meeting_time_string(result)
                self.meeting_to_modify.convert_to_table_row()
                self.update_meeting_table("#update-meeting")
            except (ValueError, TypeError):
                self.app.push_screen(
                    WarningScreen(
                        f"Time is not in the right format \n - Input \
                                : {result} \n - Expected: DD/MM/YY HH:MM "
                    )
                )

    def check_remove_participant_from_meeting(self, result: str):
        """
        Callback to remove a participant from a meeting
        """
        if result is not False:
            try:
                self.meeting_to_modify.validate_id(int(result))
                self.meeting_to_modify.remove_participant_by_id(int(result))
                self.meeting_to_modify.convert_to_table_row()
                self.update_participants_table("#update-participants")
            except (ValueError, TypeError):
                self.app.push_screen(
                    WarningScreen(
                        f"Participant with that ID does not exist \n - Input was  : {result} "
                    )
                )

    def check_add_participant_to_meeting(self, result: list[int]):
        """
        Callback to enter a participant to a meeting
        """
        if result is not False:
            try:
                new_participants = self.app.schedule.get_allowed_participants_by_id(
                    result
                )
                for participant in new_participants:
                    self.meeting_to_modify.add_participant(participant)
                self.meeting_to_modify.convert_to_table_row()
                self.update_participants_table("#update-participants")
            except (ValueError, TypeError):
                self.app.push_screen(
                    WarningScreen(
                        f"Could not add Participant to meeting\
                                                     \n - Participant : {result.__repr__} "
                    )
                )


class AddParticipantScreen(ModalScreen[list[int]]):
    """
    Screen with Dialog to select a Participant to be added to a meeting
    """

    def compose(self) -> ComposeResult:
        yield Label(
            "Add a Participant from this list to be added to the Meeting:",
            id="which-participant-to-add",
        )
        with VerticalScroll():
            for participant in self.app.schedule.worksheet.valid_participants:
                yield Checkbox(
                    label=f"{participant.name} :sweat:", name=f"{participant.id_number}"
                )

        yield Grid(
            Button("Confirm", variant="primary", id="aye-participant"),
            Button("Go Back", variant="error", id="nay-participant"),
            classes="add-dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        return a list of IDs with selected participants to previous input screen
        """
        if event.button.id == "aye-participant":
            selected = []
            for checkbox in self.query("Checkbox").results(Checkbox):
                if checkbox.value:
                    selected.append(int(checkbox.name))
            self.dismiss(selected)
        else:
            self.dismiss(False)
