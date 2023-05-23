from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Button, Footer, Header, Static, Label
from textual.widget import Widget
from textual.reactive import reactive
from textual.widgets import Input

# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high


class Schedule():
    """eventually this class will be imported. For now, this is just a placeholder"""

    def __init__(self, name, ) -> None:
        self.name = name
        self.num_meetings = 0

    def change_name(self, new_name):
        """ just to test if this method can be called from the main App """
        self.name = new_name

class Name(Widget):
    """Generates a greeting."""

    who = reactive("name", layout=True)  

    def render(self) -> str:
        return self.app.schedule.name
    


class MeetingDisplay(Static):
    """A widget to display a scheduled meeting"""

    def compose(self) -> ComposeResult:
        """Items of a meeting"""
        yield Label('Name')
        yield Label('Time')
        yield Label('Info')
        yield Input(placeholder="Enter your name")
        yield Name()
        yield Button('Update', id='update', variant='primary')
        yield Button('Add Participants', id='add', variant='primary')
    
    def on_input_changed(self, event: Input.Changed) -> None:
        self.query_one(Name).who = event.value
        self.app.schedule.name = "My new Meetings"
        

class MeetingsApp(App):
    """
    A Textual app to manage meetings.
    """

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    CSS_PATH = "./assets/css/meetings.css"

    schedule = reactive( Schedule("My Meetings"))

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield ScrollableContainer(MeetingDisplay(), MeetingDisplay(), MeetingDisplay())


    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark


if __name__ == "__main__":
    app = MeetingsApp()
    app.run()
