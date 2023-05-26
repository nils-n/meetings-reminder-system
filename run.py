from textual.app import App, ComposeResult
from textual.widgets import  Footer, Header, Input, DataTable, Markdown
from textual.reactive import reactive
from textual.app import App, ComposeResult
from itertools import cycle

# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

EXAMPLE_MARKDOWN = """\
# Meeting Reminders

This Terminal Application helps you organize your upcoming meetings. (Press 'L' to load your meetings)

"""

cursors = cycle(["column", "row", "cell"])

class MockMeeting():
    """
    mocks a Meeting class 
    eventually this class will be imported. For now, this is just a placeholder
    """
    def __init__(self, meeting_id, name, time, invited, confirmed ) -> None:
        self.meeting_id = meeting_id
        self.name = name
        self.time = time
        self.num_invited = invited
        self.num_confirmed = confirmed
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
        self.table_rows = []
        self.load_meetings()
        self.convert_meetings_to_table()

    def change_name(self, new_name):
        """ just to test if this method can be called from the main App """
        self.name = new_name

    def load_meetings(self):
        """ create mock list of meetings just for testing of the display """
        self.meetings.append(MockMeeting(1, 'Journal Club', "Thu 10:00 - 11:00", 5, 5))
        self.meetings.append(MockMeeting(2, 'Lab Meeting', "Fri 12:00 - 14:00", 42, 5))

    def convert_meetings_to_table(self):
        """converts the meeting array into an array that can be displayed in a table"""
        self.table_rows = []
        self.table_rows.append( ("ID", "Name", "Time", "invited", "confirmed" ))
        for meeting in self.meetings:
            self.table_rows.append( ( meeting.meeting_id, meeting.name, meeting.time, meeting.num_invited, 
                             meeting.num_confirmed))

    def convert_table_to_meeting(self):
        """
        converts the table from TUI into into meeting array that can be pushed to google sheets
        since this is just mock, it is not implemeneted.
        """
        pass


class MeetingsApp(App):
    """
    A Textual app to manage meetings.
    """

    BINDINGS = [ ("d", "toggle_dark", "Toggle dark mode"), 
                ("l" , "load_meetings" , "Load Meetings")]
    CSS_PATH = "./src/reminding/css/meetings.css"

    schedule = reactive( MockSchedule("A Mock Schedule"))

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
