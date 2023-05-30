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


def test_can_read_values_from_worksheet() -> None:
    """test if the class can read values from worksheet"""
    data = Worksheet("Test Sheet", None)
    model = data.schedule_sheet.get_all_values()

    assert model[1][1] == "Christmas Party"
    assert model[1][2] == "24/12/23 21:00"
    assert model[1][3] == "Nakatomi Plaza"
