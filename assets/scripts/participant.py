"""Class to describe a participant of a meeting"""
from dataclasses import dataclass, astuple, asdict

@dataclass
class Participant :
    """Describes a person that participates in a meeting"""
    name: str
    email: str
    id_number: int


def main() -> None :
    """test if a participant can be created"""
    participant = Participant('Han Solo', 'hansolo@fakemail.com', 1)
    print(participant)
    print(astuple(participant))
    print(asdict(participant))

if __name__ == '__main__' :
    main()
