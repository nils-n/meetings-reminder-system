"""This is the entry point for the application"""
from textual import events
from textual.app import App, ComposeResult
from textual.widgets import  Footer, Header, Input, DataTable, Markdown, Input, Button,Label
from textual.widgets import Placeholder, ListView, ListItem
from textual.reactive import reactive, var
from textual.screen import ModalScreen 
from textual.containers import Grid, Horizontal, Vertical
from reminding.schedule import Schedule, Meeting, Participant
from itertools import cycle
from datetime import datetime

# terminal : 80 characters wide and 24 rows high

GREETING_MARKDOWN = """\
# Meeting Reminders

This Terminal Application helps you organize your upcoming meetings. 
- Press 'L' to load your meetings from Google Sheets (not implemented currently)
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

class ModifyQuestionScreen(ModalScreen[str]):
    """ 
    Screen to question the user which meeting he or she wants to modify
    """
    def __init__(self,  message: str="Which meeting do you want to modify? (Use Meeting ID)") -> None:
        self.question_message = message
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Label(self.question_message, id="which-meeting")
        yield Grid(
                Input( "1", placeholder="Input here",id="input-which-meeting", classes="columns"),      
                Button("Confirm", variant="primary", id="which-meeting"),
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

class ModifyMeetingScreen( ModalScreen[int]):
    """Screen with a dialog to update details of a selected meeting"""

    def __init__(self,  meeting_id: int) -> None:
        self.target_meeting_id = meeting_id
        self.meeting_to_modify =  self.app.schedule.get_meeting_by_id( int(meeting_id))
        super().__init__()

    def compose(self) -> ComposeResult: 
        yield Label("What you want to modify of this meeting?", id="question")
        #yield Placeholder( id="question")
        yield DataTable(id='update-meeting')
        yield DataTable(id='update-participants')
        yield Grid(
            Button("Name", variant="default", id="update-name",  classes="column"),
            Button("Time", variant="default", id="update-time",  classes="column"),   
            Button("Add Participant", variant="default", id="add-participant",  classes="column"),
            Button("Remove Participant", variant="default", id="remove-participant",  classes="column"),
            Button("Save Changes", variant="primary", id="update-now",  classes="column"),
            Button("Go Back", variant="error", id="not-update-now",  classes="column"),
            classes="update-dialog"
        )
    
    def update_meeting_table(self, table_id) -> None:
        """ updates the displayed table in the TUI with the current values of the Meeting"""
        table = self.query_one(table_id)
        table.clear(columns=True)
        table.cursor_type = next(cursors)
        table.zebra_stripes = True
        ROWS = self.meeting_to_modify.table_row
        table.add_columns(*ROWS[0])
        table.add_rows(ROWS[1:])

    def update_participants_table(self, table_id) -> None:
        """ updates the displayed table in the TUI with the current values of the Meeting"""
        table = self.query_one(table_id)
        table.clear(columns=True)
        table.cursor_type = next(cursors)
        table.zebra_stripes = True
        self.meeting_to_modify.convert_participants_to_table()
        ROWS = self.meeting_to_modify.participant_table_rows
        table.add_columns(*ROWS[0])
        table.add_rows(ROWS[1:])

    def on_mount(self) -> None:
        self.update_meeting_table( '#update-meeting')
        self.update_participants_table( '#update-participants')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "update-name":
            self.app.push_screen( ModifyQuestionScreen('Enter New Meeting Name for the Meeting:   '), self.check_update_meeting_name )
        elif event.button.id == "update-time":
            self.app.push_screen( ModifyQuestionScreen('Enter New Meeting Time for the Meeting: (Format DD/MM/YY HH:MM)   '), self.check_update_meeting_time )
        elif event.button.id == "remove-participant": 
            self.app.push_screen( ModifyQuestionScreen('Select Which Participant to Remove (Use Participant ID)   '), self.check_remove_participant_from_meeting )
        elif event.button.id == "add-participant": 
            self.app.push_screen( AddParticipantScreen('Select Which Participant to Add (from the List)   '), self.check_add_participant_to_meeting )
        else:
            self.app.pop_screen()

    def check_update_meeting_name(self, result: str):
        """
        Callback to update meeting name
        """
        if result is not False :
            try:
                self.meeting_to_modify.validate_name(result)
                self.meeting_to_modify.convert_to_table_row()
                self.update_meeting_table('#update-meeting')
            except (ValueError, TypeError):
                self.app.push_screen( WarningScreen( f"Name is not a string ( Name : {result} )" ) )

    def check_update_meeting_time(self, result: str):
        """
        Callback to update meeting time
        """
        if result is not False :
            try:
                self.meeting_to_modify.validate_meeting_time_string(result)
                self.meeting_to_modify.convert_to_table_row()
                self.update_meeting_table('#update-meeting')
            except (ValueError, TypeError):
                self.app.push_screen( WarningScreen( f"Time is not in the right format \n - Input   : {result} \n - Expected: DD/MM/YY HH:MM " ) )

    def check_remove_participant_from_meeting(self, result: str):
        """
        Callback to remove a participant from a meeting
        """
        if result is not False :
            try:
                self.meeting_to_modify.validate_id(int(result))
                self.meeting_to_modify.remove_participant_by_id( int(result) )
                self.meeting_to_modify.convert_to_table_row()
                self.update_participants_table( '#update-participants')
            except (ValueError, TypeError):
                self.app.push_screen( WarningScreen( f"Participant with that ID does not exist \n - Input was  : {result} " ) )

    def check_add_participant_to_meeting(self, result: Participant):
        """
        Callback to enter a participant to a meeting
        """
        if result is not False :
            try:
                self.meeting_to_modify.add_participant_to_meeting( result ) 
                self.meeting_to_modify.convert_to_table_row()
                self.update_participants_table( '#update-participants')
            except (ValueError, TypeError):
                self.app.push_screen( WarningScreen( f"Could not add Participant to meeting\
                                                     \n - Participant : {result.__repr__} " ) )

class AddParticipantScreen( ModalScreen[Participant]):
    """
    Screen with Dialog to select a Participant to be added to a meeting
    """
    def compose(self) -> ComposeResult:
        yield Label("Add a Participant from this list to be added to the Meeting:", id="which-participant-to-add")
        yield Grid(
            ListView(
                ListItem(Label("One")),
                ListItem(Label("Two")),
                ListItem(Label("Three")),
                ListItem(Label("Four")),
                ListItem(Label("Five")),
                ListItem(Label("Six")),
            ),
                Button("Confirm", variant="primary", id="aye-participant"),
                Button("Go Back", variant="error", id="nay-participant"),
                classes="add-dialog"
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
                self.push_screen( ModifyMeetingScreen(result), self.check_meeting_update)
            except (ValueError, TypeError):
                self.app.push_screen( WarningScreen( f"Meeting ID does not exist ( ID : {result} )" ) )

    def check_meeting_update(self, result: Meeting) -> None:
        """
        Callback with modified meeting
        If meeting was updated, then update schedule and datatable
        To be implmemented 
        """
        pass 

if __name__ == "__main__":
    app = MeetingsApp()
    app.run()
