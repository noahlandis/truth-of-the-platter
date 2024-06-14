import pytest
import input
from unittest.mock import Mock, patch


@pytest.mark.parametrize("side_effect, expected", [
    (["Home Slice Pizza", "Austin", "TX"], ("Home Slice Pizza", "Austin", "TX")),  # all input given
    (["Home Slice Pizza", "Austin", ""], ("Home Slice Pizza", "Austin", "")),     # no state given
    (["Home Slice Pizza", "", "TX"], ("Home Slice Pizza", "", "TX")),             # no city given
    (["Home Slice Pizza", "", ""], ("Home Slice Pizza", "", ""))                 # no city and state given
])
@patch('builtins.input')
def test_read_input(mock_input: Mock, side_effect, expected):
    mock_input.side_effect = side_effect
    actual = input.read_input()
    assert actual == expected


@patch('builtins.input', side_effect=['', 'Home Slice Pizza', 'Austin', 'TX'])
@patch('builtins.print')
def test_read_input_blank_name(mock_print: Mock, mock_input: Mock):
    input.read_input()
    assert any("The restaurant name cannot be blank." in call.args[0] for call in mock_print.call_args_list)

def test_get_intended_restaurant_one_match():
    yelp_potential_matches = [("page 1", "Home Slice Pizza", "501 E 53rd St Austin, TX 78751")]
    expected = ("page 1", "Home Slice Pizza", "501 E 53rd St Austin, TX 78751")
    actual = input.get_intended_restaurant(yelp_potential_matches)
    assert actual == expected

@patch('builtins.input', return_value="1")
def test_get_intended_restaurant_multiple_matches(mock_input: Mock):
    yelp_potential_matches = [("page 1", "Home Slice Pizza", "501 E 53rd St Austin, TX 78751"), ("page 2", "Home Slice Pizza", "1415 S Congress St Austin, TX 78704")]
    expected = ("page 2", "Home Slice Pizza", "1415 S Congress St Austin, TX 78704")
    actual = input.get_intended_restaurant(yelp_potential_matches)
    assert actual == expected

@pytest.mark.parametrize("side_effect", [
    ("2", "0"), # invalid index: out of bounds positive
    ("-2", "0"), # invalid index: out of bounds negative
    ("a", "0"), # letter given
    ("", "0") # empty string given
])
@patch('builtins.print')
@patch('builtins.input')
def test_get_intended_restaurant_errors(mock_input: Mock, mock_print: Mock, side_effect):
    yelp_potential_matches = [("page 1", "name 1", "location 1"), ("page 2", "name 2", "location 2")]
    mock_input.side_effect = side_effect
    input.get_intended_restaurant(yelp_potential_matches)
    assert any("The number you enter must correspond to one of the listed restaurants." in call.args[0] for call in mock_print.call_args_list)


    

