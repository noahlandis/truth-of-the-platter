from src import input
from unittest.mock import Mock, patch

@patch('builtins.input', side_effect=['John Doe', 'New York'])
def test_read_input(mock_input: Mock):
    expected = ("John Doe", "New York")
    actual = input.read_input()
    assert actual == expected

@patch('builtins.input', side_effect=['', 'John Doe', 'New York'])
@patch('builtins.print')
def test_read_input_blank_name(mock_print: Mock, mock_input: Mock):
    input.read_input()
    mock_print.assert_called_once_with("The restaurant name cannot be blank.")

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

@patch('builtins.input', side_effect=["2", "0"])
@patch('builtins.print')
def test_get_intended_restaurant_index_error_out_of_range(mock_print: Mock, mock_input: Mock):
    yelp_potential_matches = [("page 1", "name 1", "location 1"), ("page 2", "name 2", "location 2")]
    input.get_intended_restaurant(yelp_potential_matches)
    mock_print.assert_any_call("The number you enter must correspond to one of the listed restaurants.")

@patch('builtins.input', side_effect=["-1", "0"])
@patch('builtins.print')
def test_get_intended_restaurant_index_error_negative_one(mock_print: Mock, mock_input: Mock):
    yelp_potential_matches = [("page 1", "name 1", "location 1"), ("page 2", "name 2", "location 2")]
    input.get_intended_restaurant(yelp_potential_matches)
    mock_print.assert_any_call("The number you enter must correspond to one of the listed restaurants.")

@patch('builtins.input', side_effect=["a", "0"])
@patch('builtins.print')
def test_get_intended_restaurant_value_error_letter_given(mock_print: Mock, mock_input: Mock):
    yelp_potential_matches = [("page 1", "name 1", "location 1"), ("page 2", "name 2", "location 2")]
    input.get_intended_restaurant(yelp_potential_matches)
    mock_print.assert_any_call("The number you enter must correspond to one of the listed restaurants.")

@patch('builtins.input', side_effect=["", "0"])
@patch('builtins.print')
def test_get_intended_restaurant_value_error_empty_string(mock_print: Mock, mock_input: Mock):
    yelp_potential_matches = [("page 1", "name 1", "location 1"), ("page 2", "name 2", "location 2")]
    input.get_intended_restaurant(yelp_potential_matches)
    mock_print.assert_any_call("The number you enter must correspond to one of the listed restaurants.")




    

