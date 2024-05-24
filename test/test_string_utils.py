import pytest
from src import string_utils

@pytest.mark.parametrize("yelp_name, expected", [
    ("Home Slice Pizza", True),  # test sponsored results
    ("Home Slice 1. Pizza", True),
    ("1. Home Slice Pizza", False), # test non-sponsored results
    ("10. Home Slice Pizza", False)     
])
def test_is_sponsored(yelp_name, expected):
    actual = string_utils.is_sponsored(yelp_name)
    assert actual == expected

def test_remove_non_alphanumeric_chars():
    a_string = "\tHomeslice's Pizza, Restaraunt"
    expected = "HomeslicesPizzaRestaraunt"
    actual = string_utils.remove_non_alphanumeric_chars(a_string)
    assert expected == actual

@pytest.mark.parametrize("name, expected", [
    ("home slice pizza", True), # test different capitalization
    ("HomeSlicePizza", True), # test different spacing
    ("Home Slice", True), # test shortened name
    ("Home Slice Restaraunt", True), # test different last word
    ("Home Slice's Pizza", True), # test different punctuation 
    ("Luigi's Pizza from Home", False) # test false match
])
def test_fuzzy_match(name, expected):
    yelp_name = "Home Slice Pizza"
    actual = string_utils.is_fuzzy_match(name, yelp_name)
    assert actual == expected