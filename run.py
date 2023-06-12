"""This is the entry point for the application"""
from itertools import cycle
from textual.app import App, ComposeResult
from textual.widgets import (
    Footer,
    Header,
    DataTable,
    Markdown,
)
from textual.reactive import reactive
from textual.containers import Horizontal
from textual import log
from gspread.exceptions import APIError
from reminding.schedule import Schedule
from reminding.meeting import Meeting
from reminding.worksheet import Worksheet
from screens import (
    NotificationScreen,
    WarningScreen,
    ModifyQuestionScreen,
    ModifyMeetingScreen,
    NewMeetingScreen,
)

GREETING_MARKDOWN = """\
# Meeting Manager

This Terminal Application helps you organize your upcoming meetings. 
- Press **'A'** to *add*, 'R' to *remove* or 'M' to *modify* a meeting 
- Press **'P'** to push your local changes 
- Press **'W'** to toggle display  between **Week**, **Month** and **All Meetings** 
"""


cursors = cycle(["column", "row", "cell"])


class MeetingsApp(App):
    """
    A Textual app to manage meetings.

    """

    BINDINGS = [
        ("d", "toggle_dark", "Dark mode"),
        ("a", "add_meeting", "Add"),
        ("r", "remove_meeting", "Remove"),
        ("m", "modify_meeting", "Modify"),
        ("p", "push_changes", "Push"),
        ("w", "toggle_time_range", "Toggle Time"),
    ]
    CSS_PATH = "./assets/css/meetings.css"

    schedule = reactive(
        Schedule(Worksheet("Schedule Sheet", None), "An example Schedule", [], [])
    )
    in_sync = reactive(True)

    def __init__(self):
        self.time_ranges = ["Week", "Month", "All Meetings"]
        self.current_time_range = "All Meetings"
        self.time_range_state = 2
        super().__init__()

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield Markdown(GREETING_MARKDOWN, id="entry-markdown")
        yield Horizontal(
            Markdown(
                f""" **Your Meetings:** [ {self.current_time_range} ]""",
                id="time-range-label",
            ),
            Markdown(
                f"""**In Sync:** [ { self.in_sync} ]""",
                id="sync-status",
            ),
            id="datatable-status",
        )
        yield DataTable(id="meetings-table", show_cursor=False)
        yield Footer()

    def on_mount(self) -> None:
        """called after mounting the screen"""
        self.schedule.load_meetings()
        self.schedule.load_participation_matrix()
        self.schedule.load_participants()
        self.load_meetings_table(self.app.current_time_range)
        sync_status = self.query_one("#sync-status")
        sync_status.add_class("in-sync")

    def action_toggle_time_range(self) -> None:
        """Toggles the view of the Meetings table
        States : 0=Week, 1=Month, 2=All Meetings
        """
        self.time_range_state = (
            self.time_range_state + 1 if self.time_range_state < 2 else 0
        )
        self.current_time_range = self.time_ranges[self.time_range_state]
        self.load_meetings_table(self.current_time_range)
        label_over_table = self.query_one("#time-range-label")
        label_over_table.update(
            f""" **Your Meetings:** [ {self.current_time_range} ]"""
        )

    def load_meetings_table(self, time_range) -> None:
        """updates the meeting table on the screen"""
        table = self.query_one("#meetings-table")
        table.zebra_stripes = True
        table.clear(columns=True)
        self.app.schedule.convert_meetings_to_table(time_range)
        rows = self.app.schedule.table_rows
        rows = iter(rows)
        column_labels = next(rows)
        for column in column_labels:
            table.add_column(column, key=column)
        table.add_rows(rows)
        table.sort("Time")

    def key_c(self):
        """called after key pressed"""
        table = self.query_one(DataTable)
        table.cursor_type = next(cursors)
        self.load_meetings_table(self.current_time_range)

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark

    def update_sync_status(self, new_status) -> None:
        """Updates a markdown that displayes on the Main Screen whether
        the current schedule is in sync with the remote repository"""
        self.in_sync = new_status
        new_text = f"""**In Sync:** [ { self.in_sync} ]"""
        sync_status = self.query_one("#sync-status")
        sync_status.update(new_text)
        if not self.in_sync:
            sync_status.add_class("not-in-sync")
            sync_status.remove_class("in-sync")
        else:
            sync_status.remove_class("not-in-sync")
            sync_status.add_class("in-sync")

    def action_push_changes(self) -> None:
        """An action to update worksheet with local changes"""
        try:
            if self.schedule.worksheet.is_modified:
                self.schedule.push_schedule_to_repository()
                self.schedule.calculate_participation_matrix()
                self.schedule.load_participants()
                self.schedule.push_participation_matrix_to_repository()
                self.load_meetings_table(self.current_time_range)
                self.schedule.worksheet.reset_modified_state()
                new_sync_status = not self.schedule.worksheet.is_modified
                self.update_sync_status(new_sync_status)
                self.app.push_screen(
                    NotificationScreen("Local Changes successful pushed!")
                )
            else:
                self.app.push_screen(
                    NotificationScreen(
                        "No Local Changes detected - \
Your schedule is identical with the schedule on the remote sheet."
                    )
                )

        except (ValueError, AttributeError, APIError):
            self.app.push_screen(
                WarningScreen(
                    "Could not connect to Google Sheet.\nLocal Changes are not saved!"
                )
            )

    def action_add_meeting(self) -> None:
        """an action to add a meeting"""
        self.push_screen(NewMeetingScreen(), self.check_input)

    def check_input(self, result: Meeting) -> None:
        """
        Callback to get return value (a meeting) from NewMeetingScreen Widget
        """
        if result is not False:
            self.schedule.add_meeting(result)
            self.update_sync_status(not isinstance(result, Meeting))
            self.load_meetings_table(self.current_time_range)

    def action_remove_meeting(self) -> None:
        """
        an action to remove a meeting
        """
        self.push_screen(
            ModifyQuestionScreen("Select Which Meeting to Remove (Use Meeting ID)"),
            self.check_which_meeting_to_remove,
        )

    def check_which_meeting_to_remove(self, result: int) -> None:
        """
        Callback to check which meeting the user wants to remove
        """
        if result is not False:
            try:
                self.schedule.validate_meeting_id(result)
                self.schedule.worksheet.remove_meeting_by_id(int(result))
                self.schedule.load_meetings()
                self.schedule.calculate_participation_matrix()
                self.schedule.load_participants()
                self.schedule.convert_meetings_to_table(self.current_time_range)
                self.update_sync_status(False)
                self.load_meetings_table(self.current_time_range)
            except (ValueError, TypeError):
                self.app.push_screen(
                    WarningScreen(f"Meeting ID does not exist ( ID : {result} )")
                )

    def action_modify_meeting(self) -> None:
        """an action to modify and exisisting meeting"""
        self.push_screen(ModifyQuestionScreen(), self.check_which_meeting_to_modify)

    def check_which_meeting_to_modify(self, result: int) -> None:
        """
        Callback to check which meeting the user wants to modify
        """
        if result is not False:
            try:
                log(f"--> checking if meeting with id {result} exists")
                self.schedule.validate_meeting_id(result)
                self.push_screen(ModifyMeetingScreen(result), self.check_meeting_update)
            except (ValueError, TypeError):
                self.app.push_screen(
                    WarningScreen(f"Meeting ID does not exist ( ID : {result} )")
                )

    def check_meeting_update(self, result: int) -> None:
        """
        Callback with modified meeting
        If meeting was updated, then update schedule and datatable
        """
        log("--> entering callback from  ModifyMeeting Screen")
        log(f"--> result was {result}")
        if result:
            self.app.schedule.worksheet.check_if_modified()
            self.update_sync_status(False)
            self.app.load_meetings_table(self.app.current_time_range)


if __name__ == "__main__":
    app = MeetingsApp()
    app.run()
