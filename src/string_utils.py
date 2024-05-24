import re
from fuzzywuzzy import fuzz


def remove_non_alphanumeric_chars(a_string):
    return re.sub(r'\W+', '', a_string)

def is_fuzzy_match(name, yelp_name):
    name = remove_non_alphanumeric_chars(name)
    yelp_name = remove_non_alphanumeric_chars(yelp_name)
    match_ratio = fuzz.partial_token_set_ratio(name, yelp_name)
    return match_ratio > 70

def is_sponsored(yelp_name):
    return re.match(r'^\d\.', yelp_name)

def is_potential_match(name, yelp_name):
    return is_sponsored(yelp_name) and is_fuzzy_match(name, yelp_name)

def extract_review_count(text):
    return re.findall(r'[0-9,]+', text)[0]