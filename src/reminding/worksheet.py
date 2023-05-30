from dataclasses import dataclass
import gspread
from google.oauth2.service_account import Credentials
from reminding.schedule import Schedule

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("Meeting-Reminders")


@dataclass
class Worksheet:
    """
    This class handles the read and write access to google sheet
    so that changes after closing the program are permanent
    """

    name: str
    schedule_sheet: gspread.Worksheet

    def __post_init__(self) -> None:
        self.schedule_sheet = SHEET.worksheet("schedule")
