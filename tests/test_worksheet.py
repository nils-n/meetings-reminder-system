"""
This is a unit test for the worksheet class. 

All unit tests are laid out in the form 

A rrange
A ct 
A ssert

"""
from reminding.worksheet import Worksheet


def test_can_create_new_worksheet() -> None:
    """test if a new worksheet can be created"""

    model = Worksheet("Test Sheet", None)

    assert isinstance(model, Worksheet)
