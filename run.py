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

EXAMPLE_MARKDOWN = """\
# Meeting Reminders

This Terminal Application helps you organize your upcoming meetings. (Press 'L' to load your meetings)

"""

cursors = cycle(["column", "row", "cell"])

class InputName(ModalScreen):
    """Screen with Input Dialog to enter a Name"""

    def compose(self) -> ComposeResult:
        yield Label("Enter an Name for the Meeting.")
        yield Input(
            placeholder="Enter a name...",
        )

    def on_input_submitted(self) -> None:
        """
        This needs an implmentation
        To retrieve and then validate input
        --> For now, just display the screen
        """
        self.app.pop_screen()


class UpdateScreen(ModalScreen):
    """Screen with a dialog to enter meeting details."""

    new_meeting = reactive ( Meeting( 42,  "New Meeting", datetime.now() , True, False, [], "") )

    def compose(self) -> ComposeResult:
       
            yield Label("Do you want to add this meeting?", id="question")
            #yield Label(f"Name: {self.new_meeting.name}\n \
            #            Time: {self.new_meeting.datetime}", id="new-meeting")
            yield DataTable(id='new-meeting')
            yield Grid(
                Button("No", variant="error", id="no",  classes="column"),
                Button("Yes", variant="success", id="yes",  classes="column"),   
                Button("Update", variant="primary", id="input-data",  classes="column"),
                id="dialog"
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

    def on_mount(self) -> None: 
        table = self.query_one('#new-meeting')
        table.cursor_type = next(cursors)
        table.zebra_stripes = True
        ROWS = self.new_meeting.table_row
        table.add_columns(*ROWS[0])
        table.add_rows(ROWS[1:])

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "input-data":
            self.app.push_screen(InputName())

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
        yield Markdown(EXAMPLE_MARKDOWN)
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
