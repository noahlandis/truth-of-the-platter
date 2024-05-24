import unittest
from src import input
from unittest.mock import patch


def test_read_input():
    expected = ("John Doe", "New York")
    with patch('builtins.input', side_effect=['John Doe', 'New York']):
        actual = input.read_input()
    assert actual == expected    

    