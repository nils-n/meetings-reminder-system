"""This is the entry point for the application"""
from textual.app import App, ComposeResult
from textual.widgets import  Footer, Header, Input, DataTable, Markdown, Input, Button,Label
from textual.widgets import Placeholder
from textual.reactive import reactive
from textual.screen import ModalScreen 
from textual.containers import Grid, Horizontal, Vertical
from reminding.schedule import Schedule, Meeting
from itertools import cycle
from datetime import datetime

# terminal : 80 characters wide and 24 rows high

GREETING_MARKDOWN = """\
# Meeting Reminders

This Terminal Application helps you organize your upcoming meetings. 
- Press 'L' to load your meetings
- Press 'A' to add a meeting
 
"""


INPUT_MARKDOWN = """\
# Meeting Reminders

Enter Details for New Meeting:

"""


cursors = cycle(["column", "row", "cell"])


class WarningScreen(ModalScreen):
    """Warning Widget that pops up when user input is invalid"""

    def compose(self) -> ComposeResult:
        yield Label("Input is invalid", id="invalid-input-msg")
        yield Grid(
                Button("Try again", variant="error", id="return-to-previous"),
                classes="dialog"
            )

    def on_button_pressed(self) -> None:
        """return to previous input screen """
        self.app.pop_screen()


class InputMeeting(ModalScreen[Meeting]):
    """Screen with Input Dialog to enter details of a new Meeting"""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Markdown(INPUT_MARKDOWN)
        yield Vertical(
            Input( placeholder="Name",id="input-name", classes="columns"),
            Input( placeholder="DD/MM/YY", id="input-date", classes="columns"),
            Input( placeholder="HH:MM", id="input-time", classes="columns"),
            id="meeting-inputs",
        )
  
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
        new_meeting.validate_name( new_name)
        try: 
            new_meeting.validate_meeting_time_string( new_datetime)
            self.dismiss( new_meeting )

        except ValueError:
            self.app.push_screen( WarningScreen() )
            # add here a widget that pops up and informs about error message.
            # for now it is just silently not updating if the format is wrong
            print('something went wrong')


class UpdateScreen(ModalScreen):
    """Screen with a dialog to enter meeting details."""

    new_meeting = reactive ( Meeting( 0,  "New Meeting", datetime.now() , True, False, [], "") )

    def compose(self) -> ComposeResult:
            yield Label("Do you want to add this meeting?", id="question")
            yield DataTable(id='new-meeting')
            yield Grid(
                Button("No", variant="error", id="no",  classes="column"),
                Button("Yes", variant="success", id="yes",  classes="column"),   
                Button("Update", variant="primary", id="input-data",  classes="column"),
                classes="dialog"
            )
            # Button("Update", variant="primary", id="input-data"),
            # yield Placeholder(id="question")
            # yield Placeholder(id="new-meeting")
            # yield Grid(
            #     Placeholder(id="no", classes="column"),
            #     Placeholder(id="yes", classes="column"),
            #     Placeholder(id="input-data", classes="column"),
            #     id='dialog'
            # )

    def update_table(self) -> None:
        """ updates the displayed table in the TUI with the current values of the Meeting"""
        table = self.query_one('#new-meeting')
        table.clear()
        table.cursor_type = next(cursors)
        table.zebra_stripes = True
        ROWS = self.new_meeting.table_row
        table.add_columns(*ROWS[0])
        table.add_rows(ROWS[1:])

    def on_mount(self) -> None: 
        """Directly after mounting go to input screen"""
        self.app.push_screen(InputMeeting(), self.check_input)

    def check_input(self, result: Meeting) ->None:
        """
        Callback to get return value from Input Widget
        Called when InputName is popped
        Updates also the displayed Table in the Dialog
        """
        self.new_meeting.name = result.name
        self.new_meeting.datetime = result.datetime
        self.new_meeting.convert_to_table_row()
        self.update_table()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "input-data":
            self.app.push_screen(InputMeeting(), self.check_input)
        else:
            self.app.pop_screen()

class MeetingsApp(App):
    """
    A Textual app to manage meetings.
    
    """

    BINDINGS = [ ("d", "toggle_dark", "Toggle dark mode"), 
                ("l" , "load_meetings" , "Load Meetings"), 
                ("a" , "add_meeting" , "Add a Meeting"),]
    CSS_PATH = "./assets/css/meetings.css"

    schedule = reactive( Schedule("An example Schedule", [], []))

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Markdown(GREETING_MARKDOWN)
        yield DataTable(id='meetings-table')
        yield Footer()

    def action_load_meetings(self) -> None:
        table = self.query_one('#meetings-table')
        table.cursor_type = next(cursors)
        table.zebra_stripes = True
        ROWS = self.app.schedule.table_rows
        table.add_columns(*ROWS[0])
        table.add_rows(ROWS[1:])

    def key_c(self):
        table = self.query_one(DataTable)
        table.cursor_type = next(cursors)
        
    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark
    
    def action_add_meeting(self) -> None:
        """an action to add a meeting """
        self.push_screen(UpdateScreen())

if __name__ == "__main__":
    app = MeetingsApp()
    app.run()
