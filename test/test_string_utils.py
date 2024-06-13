import pytest
from src.utils.string_utils import remove_leading_number, is_potential_match, remove_non_alphanumeric_chars, extract_review_count

@pytest.mark.parametrize("yelp_name, expected", [
    ("1. Home Slice Pizza", "Home Slice Pizza"),
    ("Home Slice Pizza", "Home Slice Pizza")
])
def test_remove_leading_number(yelp_name, expected):
    actual = remove_leading_number(yelp_name)
    assert actual == expected

@pytest.mark.parametrize("name, expected", [
    ("home slice pizza", True), # different capitalization
    ("HomeSlicePizza", True), # different spacing
    ("Home Slice", True), # shortened name
    ("Home Slice Restaraunt", True), # different last word
    ("Home Slice's Pizza", True), # different punctuation 
    ("Luigi's Pizza from Home", False) # false match
])
def test_potential_match(name, expected):
    yelp_name = "Home Slice Pizza"
    actual = is_potential_match(name, yelp_name)
    assert actual == expected

def test_remove_non_alphanumeric_chars():
    a_string = "\tHomeslice's Pizza, Restaraunt"
    expected = "HomeslicesPizzaRestaraunt"
    actual = remove_non_alphanumeric_chars(a_string)
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
    actual = extract_review_count(a_string)
    assert actual == expected