import pytest

from functions.presElection.MajorityCalcs import (
    calc_abs_majority,
    calc_simple_majority,
)


# Absolute majority tests
def test_single_winner():
    assert calc_abs_majority({"B": 40, 0: 40, 83: 13, 57: 5, 26: 5, 39: 50, 1: 0, 99: 80}) == 99

def test_two_winners():
    assert calc_abs_majority({"B": 40, 0: 40, 83: 13, 57: 5, 26: 5, 39: 60, 1: 0, 99: 80}) == (39, 99)

def test_multiple_winners():
    assert calc_abs_majority({"B": 40, 0: 40, 83: 13, 57: 60, 26: 5, 39: 60, 1: 60, 99: 80}) == (1, 39, 57, 99)

# Test ignoring blank and null votes
def test_ignore_non_valid_votes():
    assert calc_abs_majority({"B": 400, 0: 400, 1: 50, 99: 100}) == 99

# Test edge of absolute majority win condition
def test_edge_of_abs_majority():
    assert calc_abs_majority({"B": 0, 0: 0, 1: 500000, 99: 500000}) == (1, 99)
    assert calc_abs_majority({"B": 0, 0: 0, 1: 500000, 99: 500001}) == 99

# Test draw with zero votes
def test_max_zeroes():
    assert calc_abs_majority({"B": 10, 0: 10, 1: 0, 99: 0}) == (1, 99)


# Simple majority tests
def test_simple_majority():
    assert calc_simple_majority({"B": 100, 0: 100, 1: 51, 99: 50}) == 1
    assert calc_simple_majority({"B": 100, 0: 100, 1: 50, 99: 50}) == (1, 99)
    assert calc_simple_majority({"B": 100, 0: 100, 1: 50, 99: 51}) == 99

# Test too many keys
    with pytest.raises(TypeError, match="Dictionary must contain exactly 2 non-required keys"):
        calc_simple_majority({"B": 100, 0: 100, 1: 50, 2: 45, 99: 51})
