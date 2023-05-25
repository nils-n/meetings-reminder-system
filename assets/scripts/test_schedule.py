"""
These are unit tests for the schedule class. 

All unit tests are laid out in the form 

A rrange
A ct 
A ssert

"""
import pytest
from meeting import Meeting
from schedule import Schedule


def test_can_create_new_schedule( create_random_meetings ) -> None:
    """Tests if a new Schedule can be instaniated """
    random_meetings = create_random_meetings
    random_name = "Random Schedule"

    model = Schedule(random_name, 1, random_meetings )

    assert isinstance(model, Schedule)
    assert model.name == random_name
