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
        self.validate_name(  self.name )


    def validate_name(self, name):
        """validate that name is a string"""
        if not type(name) is str:
            raise(TypeError(f"Participant Name should be a string ( {name} is not a string)")) 

def main() -> None :
    """test if a participant can be created"""
    participant = Participant('Han Solo', 'hansolo@fakemail.com', 1, True)
    print(participant)
    print(astuple(participant))
    print(asdict(participant))

if __name__ == '__main__' :
    main()
