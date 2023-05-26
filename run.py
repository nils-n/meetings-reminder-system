from textual.app import App, ComposeResult
from textual.widgets import  Footer, Header, Input, DataTable, Markdown
from textual.reactive import reactive
from itertools import cycle
from reminding.schedule import Schedule

# terminal : 80 characters wide and 24 rows high

EXAMPLE_MARKDOWN = """\
# Meeting Reminders

This Terminal Application helps you organize your upcoming meetings. (Press 'L' to load your meetings)

"""

cursors = cycle(["column", "row", "cell"])

class MeetingsApp(App):
    """
    A Textual app to manage meetings.
    
    """

    BINDINGS = [ ("d", "toggle_dark", "Toggle dark mode"), 
                ("l" , "load_meetings" , "Load Meetings")]
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

if __name__ == "__main__":
    app = MeetingsApp()
    app.run()
