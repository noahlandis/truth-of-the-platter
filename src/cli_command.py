"""
This module contains the functions to handle user commands
Author: Noah Landis
"""
import types
import os
import sys
from colorama import Style
from utils.styled_cli_utils import MessageType, get_styled_input, get_styled_output

# not the cleanest, but we use const to avoid "Irrefutable pattern is allowed only for the last case statementPylance error in the switch statement
const = types.SimpleNamespace()
const.HELP = "\\h"
const.RESTART = "\\r"
const.QUIT = "\\q"

COMMANDS = {
    const.HELP: "Display this help menu",
    const.RESTART: "Restart the program",
    const.QUIT: "Quit the program"
}

def display_commands():
    """
    Displays the available commands to the user
    """
    print(get_styled_output("Available commands:", MessageType.INFO))
    for command, description in COMMANDS.items():
        print(get_styled_output(f"  {Style.BRIGHT}{command}{Style.NORMAL} - {description}", MessageType.INFO))

def get_input_with_command_handling(prompt: str) -> str:
    """
    Wrapper function to make sure a user can enter a command at any time
    :param str prompt - the prompt to display to the user
    :return str user_input - the user's input if a command wasn't entered
    """
    while True:
        user_input = get_styled_input(prompt)
        if is_command(user_input):
            handle_command(user_input)
        else:
            return user_input

def is_command(user_input: str) -> bool:
    """
    Determines if the user input is a command
    :param str user_input - the user's input
    :return bool - True if the user input is a command, False otherwise
    """
    return user_input in COMMANDS.keys()

def handle_command(command: str):
    """
    Handles the user input command
    :param str user_input - the user's input
    """
    match command:
        case const.HELP:
            display_commands()
        case const.RESTART:
            restart_program()
        case const.QUIT:
            sys.exit()

def restart_program():
    """
    Restarts the program.
    """
    # we want a new line to make it clear the program is restarting
    print()
    os.execl(sys.executable, sys.executable, *sys.argv)

def prompt_next_command():
    """
    Prompts the user to enter a command until a valid command is entered.
    """
    # we use a loop so that the prompt displays again if the HELP command is entered
    while True:
        get_input_with_command_handling(f"Enter '{const.RESTART}' to restart, or '{const.QUIT}' to quit the program")
        
