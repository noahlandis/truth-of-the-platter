"""
Utility class to handle string manipulation.
Author: Noah Landis
"""

import re
from fuzzywuzzy import fuzz

def remove_leading_number(yelp_name: str) -> str:
    """
    Removes the leading number from a Yelp name
    :param str yelp_name - the Yelp name (if it has a leading number)
    :return str - the Yelp name with the leading number removed
    """
    if bool(re.match(r'^\d+\.', yelp_name)):
        yelp_name = yelp_name[2::].lstrip()
    return yelp_name

def is_potential_match(name: str, yelp_name: str) -> bool:
    """
    Determines if the Yelp name is a fuzzy match for the user's inputted name
    :param str name - the user's inputted name
    :param str yelp_name - the name of the restaurant on Yelp
    :return bool - True if the Yelp name is a fuzzy match for the user's inputted name, False otherwise
    """
    name = remove_non_alphanumeric_chars(name)
    yelp_name = remove_non_alphanumeric_chars(yelp_name)
    match_ratio = fuzz.partial_token_set_ratio(name, yelp_name)
    return match_ratio > 70

def remove_non_alphanumeric_chars(a_string: str) -> str:
    """
    Removes all non-alphanumeric characters from a string to allow for error-tolerant string matching
    :param str a_string - the string to remove non-alphanumeric characters from
    :return str - the string with non-alphanumeric characters removed
    """
    return re.sub(r'\W+', '', a_string)

def extract_review_count(a_string: str) -> str:
    """
    Extracts the review count (numbers and commas) from a string
    :param str a_string - the string to extract the review count from
    :return str - the extracted review count
    """
    return re.findall(r'[0-9,]+', a_string)[0]