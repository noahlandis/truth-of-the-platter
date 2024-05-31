import unittest
from src import input
from unittest.mock import Mock, patch
import pytest

@patch('builtins.input', side_effect=['John Doe', 'New York'])
def test_read_input(mock_input: Mock):
    expected = ("John Doe", "New York")
    actual = input.read_input()
    assert actual == expected

@patch('builtins.input', side_effect=['', 'John Doe', 'New York'])
@patch('builtins.print')
def test_read_input_blank_name(mock_print: Mock, mock_input: Mock):
    input.read_input()
    mock_print.assert_called_once_with("The restaurant name cannot be blank")