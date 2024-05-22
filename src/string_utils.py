import re
from fuzzywuzzy import fuzz


def remove_non_alphanumeric_chars(a_string):
    return re.sub(r'\W+', '', a_string)

def is_fuzzy_match(user_input, search_result):
    user_input = remove_non_alphanumeric_chars(user_input)
    search_result = remove_non_alphanumeric_chars(search_result)
    match_ratio = fuzz.partial_token_set_ratio(user_input, search_result)
    return match_ratio > 70

def is_sponsored(buisness_name):
    return re.match(r'^\d\.', buisness_name)

def is_potential_match(name, buisness_name):
    return is_sponsored(buisness_name) and is_fuzzy_match(name, buisness_name)

def extract_review_count(text):
    return re.findall(r'[0-9,]+', text)[0]