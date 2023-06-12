"""Class to describe a participant of a meeting"""
from dataclasses import dataclass, astuple, asdict, field
from random import randint
from typing import Union
from email_validator import validate_email


@dataclass
class Participant:
    """Describes a person that participates in a meeting"""

    name: str
    email: str
    id_number: int
    has_valid_email: bool
    table_row: Union[str, int] = field(default_factory=list)

    def __post_init__(self):
        """validate that the attributes have correct form"""
        validate_email(self.email)
        self.validate_name(self.name)
        self.validate_meeting_id(self.id_number)
        if not isinstance(self.id_number, int):
            self.id_number = randint(0, 1000)

    def validate_name(self, name):
        """validate that name is a string"""
        if not isinstance(name, str):
            raise TypeError(
                f"Participant Name should be a string ( {name} \
                is not a string)"
            )

    def validate_meeting_id(self, id_number):
        """validate that meeting id is an positive integer"""
        if not isinstance(id_number, int):
            raise TypeError(
                f"Participant Name should be an integer \
                             ( {self.validate_meeting_id} is not an integer)"
            )
        if isinstance(id_number, int) and (id_number < 0):
            raise ValueError(
                f"Meeting ID should be non-negative \
                             ( {self.validate_meeting_id} is not a positive \
                                integer)"
            )

    def update_name(self, new_name):
        """updates particpant name"""
        self.validate_name(new_name)
        self.name = new_name

    def update_email(self, new_email):
        """updates participant email address"""
        validate_email(new_email)
        self.email = new_email

    def update_id(self, new_id):
        """updates participant id"""
        self.validate_meeting_id(new_id)
        self.id_number = new_id

    def convert_to_table_row(self):
        """
        convert the participant details into a table format that the TUI can
        display. currently a table row is defined as :
        ID -  Name - Email - has confirmed - has been notified
        """
        self.table_row = []
        self.table_row.append((self.id_number, self.name, self.email, True, True))


def main() -> None:
    """test if a participant can be created"""
    participant = Participant("Han Solo", "hansolo@fakemail.com", 1, True)
    print(participant)
    print(astuple(participant))
    print(asdict(participant))


if __name__ == "__main__":
    main()
