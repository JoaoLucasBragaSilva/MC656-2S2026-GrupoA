def calc_abs_majority(vote_dict):
    """
    Determines the result of an absolute majority vote based on a dictionary.\n
    If a value is greater than floor(sum(values)), returns its key.\n
    If not, returns a tuple with all keys of greatest and 2nd greatest values.
    """

    vote_dict = validate_and_trim_dictionary(vote_dict)

    sorted_dict = sorted(vote_dict.items(), key=lambda item: item[1], reverse=True)
    most_voted_key = sorted_dict[0][0]
    sum_of_votes = sum(vote_dict.values())

    if vote_dict[most_voted_key] > sum_of_votes//2:
        return most_voted_key
    else:
        second_turn_keys = [most_voted_key, sorted_dict[1][0]]
        for i in range(2, len(sorted_dict)):
            if sorted_dict[i][1] == sorted_dict[1][1]:
                second_turn_keys.append(sorted_dict[i][0])
            else:
                break

        return tuple(sorted(second_turn_keys))

def calc_simple_majority(vote_dict):
    """
    Determines the result of a simple majority vote based on a dictionary.\n
    Returns the key of the greatest value.\n
    If both keys have the same value, returns a tuple containing both.
    """

    vote_dict = validate_and_trim_dictionary(vote_dict)
    if len(vote_dict) > 2:
        raise TypeError("Dictionary must contain exactly 2 non-required keys")

    sorted_dict = sorted(vote_dict.items(), key=lambda item: item[1], reverse=True)
    most_voted_key = sorted_dict[0][0]

    if vote_dict[most_voted_key] > sorted_dict[1][1]:
        return most_voted_key
    else:
        return most_voted_key, sorted_dict[1][0]

def validate_and_trim_dictionary(vote_dict):
    """
    Validates a dictionary according to the following criteria:\n
    - Must contain keys 0 and "B"
    - Must contain at least 2 keys aside from the above
    - Additional keys must be integers from 1 to 99
    - Values must be integers greater than or equal to 0
    """

    # Condition 4
    if (not all(isinstance(v, int) for v in vote_dict.values())) or (any(v < 0 for v in vote_dict.values())):
        raise ValueError("Dictionary values must contain only integers greater than or equal to than 0")

    # Condition 1
    if (0 not in vote_dict) or ("B" not in vote_dict):
        raise KeyError("Dictionary must contain both 0 and 'B' keys")
    trimmed = trim_dictionary(vote_dict)

    # Condition 3
    if (not all(isinstance(v, int) for v in trimmed)) or (not all(1 <= k <= 99 for k in trimmed)):
        raise ValueError("Non-required dictionary keys must contain only integers from 1 to 99")

    # Condition 2
    if len(trimmed) < 2:
        raise TypeError("Dictionary must contain at least 2 non-required keys")

    return trimmed

def trim_dictionary(vote_dict):
    return {
        k: v
        for k, v in vote_dict.items()
        if k not in (0, "B")
    }

d={"B":0,0:1,1:4,2:5,3:4}
print(calc_abs_majority(d))
