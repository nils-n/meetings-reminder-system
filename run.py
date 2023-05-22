from textual.app import App, ComposeResult
from textual.containers import ScrollableContainer
from textual.widgets import Button, Footer, Header, Static, Label

# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high


# just a test to commit from code anywhere

# just a test to commit from vscode

class MeetingDisplay(Static):
    """A widget to display a scheduled meeting"""

    def compose(self) -> ComposeResult:
        """Items of a meeting"""
        yield Label('Name')
        yield Label('Time')
        yield Label('Info')
        yield Button('Update', id='update', variant='primary')
        yield Button('Add Participants', id='add', variant='primary')

class MeetingsApp(App):
    """
    A Textual app to manage meetings.
    """

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    CSS_PATH = "./assets/css/meetings.css"

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
