from unittest.mock import Mock, patch

import pytest

from ..src.cli_command import get_input_with_command_handling, handle_command, is_command


@pytest.mark.parametrize("user_input, expected", [
    ("\\h", True), # help command
    ("\\r", True), # restart command
    ("\\q", True), # quit command
    ("\\a", False), # invalid command
    ("", False)    # invalid command
])
def test_is_command(user_input, expected):
    actual = is_command(user_input)
    assert actual == expected

@patch('cli.src.cli_command.display_commands')
def test_handle_command_help(mock_display_commands: Mock):
    handle_command("\\h")
    mock_display_commands.assert_called_once()

@patch('cli.src.cli_command.restart_program')
def test_handle_command_restart(mock_restart: Mock):
    handle_command("\\r")
    mock_restart.assert_called_once()

def test_handle_command_quit():
    with pytest.raises(SystemExit):
        handle_command("\\q")

@patch('builtins.input', return_value='foo bar')
def test_get_input_with_command_handling_no_command(mock_input: Mock):
    expected = "foo bar"
    actual = get_input_with_command_handling(expected)
    assert actual == expected

@patch('builtins.input', side_effect=['\\h', 'foo bar'])
def test_get_input_with_command_handling_command(mock_input: Mock):
    expected = "foo bar"
    actual = get_input_with_command_handling(expected)
    assert actual == expected

@patch('cli.src.cli_command.handle_command')
@patch('builtins.input', return_value='foo bar')
def test_get_input_with_command_handling_no_command_handle_command_not_called(mock_input: Mock, mock_handle_command: Mock):
    expected = "foo bar"
    get_input_with_command_handling(expected)
    mock_handle_command.assert_not_called()

@patch('cli.src.cli_command.handle_command')
@patch('builtins.input', side_effect=['\\h', 'foo bar'])
def test_get_input_with_command_handling_command_is_called(mock_input: Mock, mock_handle_command: Mock):
    expected = "foo bar"
    get_input_with_command_handling(expected)
    mock_handle_command.assert_called_once_with('\\h')

