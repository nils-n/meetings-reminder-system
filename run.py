from textual.app import App, ComposeResult
from textual.widgets import Header, Footer

# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high


# just a test to commit from code anywhere

# just a test to commit from vscode

class MeetingsApp(App):
    """
    A Textual app to manage meetings.
    """

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark


if __name__ == "__main__":
    app = MeetingsApp()
    app.run()
