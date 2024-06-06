"""
This module contains utility functions for string manipulation.
Author: Noah Landis
"""

import re
from fuzzywuzzy import fuzz

def is_potential_match(name: str, yelp_name: str) -> bool:
    """
    Determines if the Yelp name is a potential match for the user's inputted name, based on the following criteria:
    - The Yelp name is not a sponsored result
    - The Yelp name is a fuzzy match for the user's inputted name
    :param str name - the user's inputted name
    :param str yelp_name - the name of the restaurant on Yelp
    :return bool - True if the Yelp name is a potential match for the user's inputted name, False otherwise
    """
    return (not is_sponsored(yelp_name)) and is_fuzzy_match(name, yelp_name)

def is_sponsored(yelp_name: str) -> bool:
    """
    Determines if the Yelp name is a sponsored result
    :param str yelp_name - the name of the restaurant on Yelp
    :return bool - True if the Yelp name is a sponsored result, False otherwise
    """

    # On Yelp, only non-sponsored results have a number followed by a period at the beginning of the name
    return not bool(re.match(r'^\d+\.', yelp_name))

def is_fuzzy_match(name: str, yelp_name: str) -> bool:
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