def calc_abs_majority(vote_dict):
    """
    Returns the result of an absolute majority vote based on a dictionary.
    If a value is greater than floor(sum(values)), returns its key.
    If not, returns a tuple with the two keys of greatest value.
    """

    sorted_dict = sorted(vote_dict.items(), key=lambda item: item[1], reverse=True)
    most_voted_key = sorted_dict[0][0]
    sum_of_votes = sum(vote_dict.values())

    if vote_dict[most_voted_key] > sum_of_votes//2:
        return most_voted_key
    else:
        return most_voted_key, sorted_dict[1][0]
    
def calc_simple_majority(vote_dict):
    """
    Returns the result of a simple majority vote based on a dictionary.
    Returns the key of the greatest value.
    If both keys have the same value, returns a tuple containing both.
    """

    sorted_dict = sorted(vote_dict.items(), key=lambda item: item[1], reverse=True)
    most_voted_key = sorted_dict[0][0]

    if vote_dict[most_voted_key] > sorted_dict[1][1]:
        return most_voted_key
    else:
        return most_voted_key, sorted_dict[1][0]