"""Class to describe a participant of a meeting"""
from dataclasses import dataclass, astuple, asdict
from email_validator import validate_email

@dataclass
class Participant :
    """Describes a person that participates in a meeting"""
    name: str
    email: str
    id_number: int
    has_valid_email: bool

    def __post_init__(self):
        """validate that the attributes have correct form"""
        validate_email( self.email )
        self.validate_name()
        self.validate_meeting_id()

    def validate_name(self):
        """validate that name is a string"""
        if not isinstance( self.name, str):
            raise TypeError(f"Participant Name should be a string ( {self.name} is not a string)")

    def validate_meeting_id(self):
        """validate that meeting id is an positive integer"""
        if not isinstance( self.id_number, int):
            raise TypeError(f"Participant Name should be an integer ( {self.validate_meeting_id} is not an integer)")
        if isinstance( self.id_number, int) and (self.id_number < 0):
            raise ValueError(f"Meeting ID should be non-negative ( {self.validate_meeting_id} is not a positive integer)")

        


def main() -> None :
    """test if a participant can be created"""
    participant = Participant('Han Solo', 'hansolo@fakemail.com', 1, True)
    print(participant)
    print(astuple(participant))
    print(asdict(participant))

if __name__ == '__main__' :
    main()
