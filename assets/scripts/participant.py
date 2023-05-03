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
        """validate that the email is has correct form"""
        validate_email( self.email )



def main() -> None :
    """test if a participant can be created"""
    participant = Participant('Han Solo', 'hansolo@fakemail.com', 1, True)
    print(participant)
    print(astuple(participant))
    print(asdict(participant))

if __name__ == '__main__' :
    main()
