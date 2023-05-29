"""This is the entry point for the application"""
from textual.app import App, ComposeResult
from textual.widgets import  Footer, Header, Input, DataTable, Markdown, Input, Button,Label
from textual.widgets import Placeholder
from textual.reactive import reactive, var
from textual.screen import ModalScreen 
from textual.containers import Grid, Horizontal, Vertical
from reminding.schedule import Schedule, Meeting
from itertools import cycle
from datetime import datetime
from dataclasses import replace

# terminal : 80 characters wide and 24 rows high

GREETING_MARKDOWN = """\
# Meeting Reminders

This Terminal Application helps you organize your upcoming meetings. 
- Press 'L' to load your meetings
- Press 'A' to add a meeting
- Press 'M' to modify a meeting (including to invite and remove participants)
 
"""

INPUT_MARKDOWN = """\
# Meeting Reminders

Enter Details for New Meeting. Note:
- Date Format DD/MM/YY
- Time Format HH:MM

"""

cursors = cycle(["column", "row", "cell"])

class WarningScreen(ModalScreen[None]):
    """Warning Widget that pops up when user input is invalid"""

    def __init__(self,  message: str="Input is invalid") -> None:
        self.error_message = message
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Label(f"{self.error_message}", id="invalid-input-msg")
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
            Input( "Test", placeholder="Name",id="input-name", classes="columns"),              # just adding a placeholder Meeting 11/11/11 - at 11:11 for faster debugging)
            Input( "11/11/11", placeholder="DD/MM/YY", id="input-date", classes="columns"),     # just adding a placeholder Meeting 11/11/11 - at 11:11 for faster debugging)
            Input( "11:11", placeholder="HH:MM", id="input-time", classes="columns"),           # just adding a placeholder Meeting 11/11/11 - at 11:11 for faster debugging)
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

        except (ValueError, TypeError):
            self.app.push_screen( WarningScreen( f"Meeting Time invalid ( {new_datetime} is not DD/MM/YY HH:MM )") )

class NewMeetingScreen(ModalScreen[Meeting]):
    """Screen with a dialog to enter details of new meeting"""

    new_meeting = var ( Meeting( 0,  "New Meeting", datetime.now() , True, False, [], "") )

    def compose(self) -> ComposeResult:
            yield Label("Do you want to add this meeting?", id="question")
            yield DataTable(id='new-meeting')
            yield Grid(
                Button("No", variant="error", id="no",  classes="column"),
                Button("Yes", variant="success", id="yes",  classes="column"),   
                Button("Reset", variant="primary", id="input-data",  classes="column"),
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
        table.clear(columns=True)
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
        temp = result
        self.new_meeting = result
        self.new_meeting.name = result.name
        self.new_meeting.datetime = result.datetime
        self.new_meeting.convert_to_table_row()
        self.update_table()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "input-data":
            self.app.push_screen(InputMeeting(), self.check_input)
        elif event.button.id == "yes":
            self.dismiss(self.new_meeting)
        else: 
            self.app.pop_screen()

class ModifyQuestionScreen(ModalScreen[int]):
    """ 
    Screen to question the user which meeting he or she wants to modify
    """
    def compose(self) -> ComposeResult:
        yield Label("Which meeting do you want to modify? (Use Meeting ID)", id="which-meeting")
        yield Grid(
                Input( "0", placeholder="Meeting ID",id="input-which-meeting", classes="columns"),      
                Button("Modify Meeting", variant="primary", id="which-meeting"),
                Button("Go Back", variant="error", id="never-mind"),
                classes="dialog"
            )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """return to previous input screen """
        if event.button.id == "which-meeting":
            target_meeting_id = self.query_one("#input-which-meeting").value
            self.dismiss(target_meeting_id)
        else:
            self.dismiss(False)

class MeetingsApp(App):
    """
    A Textual app to manage meetings.
    
    """

    BINDINGS = [ ("d", "toggle_dark", "Toggle dark mode"), 
                ("l" , "load_meetings" , "Load Meetings"), 
                ("a" , "add_meeting" , "Add Meeting"),
                ("m" , "modify_meeting" , "Modify Meeting")]
    CSS_PATH = "./assets/css/meetings.css"

    schedule = reactive( Schedule("An example Schedule", [], []))

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Markdown(GREETING_MARKDOWN)
        yield DataTable(id='meetings-table')
        yield Footer()

    def on_mount(self) -> None: 
        self.load_meetings_table()

    def action_load_meetings(self) -> None:
        self.load_meetings_table()

    def load_meetings_table(self) -> None: 
        table = self.query_one('#meetings-table')
        table.cursor_type = next(cursors)
        table.zebra_stripes = True
        ROWS = self.app.schedule.table_rows
        table.clear(columns=True)
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
        self.push_screen(NewMeetingScreen(), self.check_input)
    
    def check_input(self, result: Meeting) ->None:
        """
        Callback to get return value (a meeting) from NewMeetingScreen Widget
        """
        self.schedule.add_meeting(result)
        self.load_meetings_table()

    def action_modify_meeting(self) -> None:
        """an action to modify and exisisting meeting """
        self.push_screen( ModifyQuestionScreen(), self.check_which_meeting_to_modify )

    def check_which_meeting_to_modify(self, result: int) -> None:
        """
        Callback to check which meeting the user wants to modify
        """
        if result is not False :
            try:
                self.schedule.validate_meeting_id( result)
            except (ValueError, TypeError):
                self.app.push_screen( WarningScreen( f"Meeting ID does not exist ( ID : {result} )" ) )

if __name__ == "__main__":
    app = MeetingsApp()
    app.run()
