import pytest
from src import string_utils

@pytest.mark.parametrize("name, yelp_name, expected", [
    ("Home Slice Pizza", "1. Home Slice Pizza", True), # fuzzy match and non-sponsored result
    ("Home Slice Pizza", "Home Slice Pizza", False), # fuzzy match with sponsored result
    ("Luigi's Pizza from Home", "1. Home Slice Pizza", False), # no fuzzy match with non-sponsored result
    ("Luigi's Pizza from Home", "Home Slice Pizza", False) # no fuzzy match with sponsored result
])
def test_is_potential_match(name, yelp_name, expected):
    actual = string_utils.is_potential_match(name, yelp_name)
    assert actual == expected

@pytest.mark.parametrize("yelp_name, expected", [
    ("Home Slice Pizza", True),  # sponsored results
    ("Home Slice 1. Pizza", True),
    ("1. Home Slice Pizza", False), # non-sponsored results
    ("10. Home Slice Pizza", False)     
])
def test_is_sponsored(yelp_name, expected):
    actual = string_utils.is_sponsored(yelp_name)
    assert actual == expected

@pytest.mark.parametrize("name, expected", [
    ("home slice pizza", True), # different capitalization
    ("HomeSlicePizza", True), # different spacing
    ("Home Slice", True), # shortened name
    ("Home Slice Restaraunt", True), # different last word
    ("Home Slice's Pizza", True), # different punctuation 
    ("Luigi's Pizza from Home", False) # false match
])
def test_fuzzy_match(name, expected):
    yelp_name = "Home Slice Pizza"
    actual = string_utils.is_fuzzy_match(name, yelp_name)
    assert actual == expected

def test_remove_non_alphanumeric_chars():
    a_string = "\tHomeslice's Pizza, Restaraunt"
    expected = "HomeslicesPizzaRestaraunt"
    actual = string_utils.remove_non_alphanumeric_chars(a_string)
    assert actual == expected

@pytest.mark.parametrize("a_string, expected", [
    ("10", "10"),  
    ("(10)", "10"), 
    ("10 reviews", "10"),
    ("(10 reviews)", "10"),
    ("1,000 reviews", "1,000"),
    ("10,000 reviews", "10,000")
])
def test_extract_review_count(a_string, expected):
    actual = string_utils.extract_review_count(a_string)
    assert actual == expected