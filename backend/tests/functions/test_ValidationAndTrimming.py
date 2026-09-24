import pytest

from backend.functions.presElection.MajorityCalcs import trim_dictionary, validate_and_trim_dictionary


# Dictionary validation tests
# Tests invalid dictionary values
def test_invalid_values():
    with pytest.raises(ValueError, match="Dictionary values must contain only integers greater than or equal to than 0"):
        validate_and_trim_dictionary({"B": 0, 0: 0, 1: -1, 2: 4})
    with pytest.raises(ValueError, match="Dictionary values must contain only integers greater than or equal to than 0"):
        validate_and_trim_dictionary({"B": 0, 0: 0, 1: "a", 2: 4})

# Tests missing required 0 and "B" keys
def test_no_required_keys():
    with pytest.raises(KeyError, match="Dictionary must contain both 0 and 'B' keys"):
        validate_and_trim_dictionary({0: 0, 1: 0, 2: 4})
    with pytest.raises(KeyError, match="Dictionary must contain both 0 and 'B' keys"):
        validate_and_trim_dictionary({"B": 0, 1: 0, 2: 4})

# Tests invalid dictionary keys
def test_invalid_keys():
    with pytest.raises(ValueError, match="Non-required dictionary keys must contain only integers from 1 to 99"):
        validate_and_trim_dictionary({"B": 0, 0: 0, -1: 2, 2: 4})
    with pytest.raises(ValueError, match="Non-required dictionary keys must contain only integers from 1 to 99"):
        validate_and_trim_dictionary({"B": 0, 0: 0, "a": 2, 2: 4})

# Tests less than 2 keys after trimming
def test_not_enough_keys():
    with pytest.raises(TypeError, match="Dictionary must contain at least 2 non-required keys"):
        validate_and_trim_dictionary({"B": 0, 0: 0})
    with pytest.raises(TypeError, match="Dictionary must contain at least 2 non-required keys"):
        validate_and_trim_dictionary({"B": 0, 0: 0, 2: 4})


# Dictionary trimming test
def test_trimming():
    assert trim_dictionary({"B": 0, 0: 0}) == {}
    assert trim_dictionary({"B": 0, 0: 0, 1: 10, 2: 20}) == {1: 10, 2: 20}