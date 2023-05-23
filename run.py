from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Button, Footer, Header, Static, Label
from textual.widget import Widget
from textual.reactive import reactive
from textual.widgets import Input
from itertools import cycle
from textual.app import App, ComposeResult
from textual.widgets import DataTable


# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

# this is just the test how to work with Data tables in textualize - and how they would look like on heroku
ROWS = [
    ("lane", "swimmer", "country", "time"),
    (4, "Joseph Schooling", "Singapore", 50.39),
    (2, "Michael Phelps", "United States", 51.14),
    (5, "Chad le Clos", "South Africa", 51.14),
    (6, "László Cseh", "Hungary", 51.14),
    (3, "Li Zhuhao", "China", 51.26),
    (8, "Mehdy Metella", "France", 51.58),
    (7, "Tom Shields", "United States", 51.73),
    (1, "Aleksandr Sadovnikov", "Russia", 51.84),
    (10, "Darren Burns", "Scotland", 51.84),
]

cursors = cycle(["column", "row", "cell"])

class MockMeeting():
    """
    mocks a Meeting class 
    eventually this class will be imported. For now, this is just a placeholder
    """
    def __init__(self, name, ) -> None:
        self.name = name
        self.num_participants = 0
        self.participants = []


class MockSchedule():
    """
    mocks a Schedule class 
    eventually this class will be imported. For now, this is just a placeholder
    """

    def __init__(self, name, ) -> None:
        self.name = name
        self.num_meetings = 0
        self.meetings = []
        self.load_meetings()

    def change_name(self, new_name):
        """ just to test if this method can be called from the main App """
        self.name = new_name

    def load_meetings(self):
        """ create mock list of meetings just for testing of the display """
        self.meetings.append(MockMeeting('Journal Club'))

class Name(Widget):
    """Generates a greeting."""

    who = reactive("name", layout=True)  

    def render(self) -> str:
        return self.app.schedule.meetings[0].name
    

class MeetingDisplay(Static):
    """A widget to display a scheduled meeting"""

    def compose(self) -> ComposeResult:
        """Items of a meeting"""
        yield Input(placeholder="Enter your name")
        yield Name()
        yield Button('Update', id='update', variant='primary')
    
    def on_input_changed(self, event: Input.Changed) -> None:
        self.query_one(Name).who = event.value
        self.app.schedule.meetings[0].name = "Lab Meeting"
        

class MeetingsApp(App):
    """
    A Textual app to manage meetings.
    """

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    CSS_PATH = "./assets/css/meetings.css"

    schedule = reactive( MockSchedule("A Mock Schedule"))

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()
        yield MeetingDisplay()
        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = next(cursors)
        table.zebra_stripes = True
        table.add_columns(*ROWS[0])
        table.add_rows(ROWS[1:])

    def key_c(self):
        table = self.query_one(DataTable)
        table.cursor_type = next(cursors)

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark


if __name__ == "__main__":
    app = MeetingsApp()
    app.run()
