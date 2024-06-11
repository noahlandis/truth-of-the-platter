from unittest.mock import Mock, patch, ANY
import pytest
from cli_command import is_command, handle_command

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

@patch('cli_command.display_commands')
def test_handle_command_help(mock_display_commands: Mock):
    handle_command("\\h")
    mock_display_commands.assert_called_once()

@patch('cli_command.restart_program')
def test_handle_command_restart(mock_restart: Mock):
    handle_command("\\r")
    mock_restart.assert_called_once()

def test_handle_command_quit():
    with pytest.raises(SystemExit):
        handle_command("\\q")