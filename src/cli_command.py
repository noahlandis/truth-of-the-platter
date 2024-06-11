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
    Determines if the user input is a command, wrapper function to make sure a user
    can enter a command at any time
    :param str prompt - the prompt to display to the user
    """
    while True:
        user_input = get_styled_input(prompt)
        is_command = handle_commands(user_input)
        
        # we stop prompting user for their input after we've determined they didn't enter a command
        if not is_command:
            return user_input
    
def handle_commands(user_input: str) -> bool:
    """
    Handles the user input commands
    :param str user_input - the user's input
    :return bool - True if the user input is a command, False otherwise
    """
    match user_input:
        case const.HELP:
            display_commands()
            return True
        case const.RESTART:
            # we want a new line to make it clear the program is restarting
            print()
            os.execl(sys.executable, sys.executable, *sys.argv)
        case const.QUIT:
            sys.exit()
    return False

def prompt_next_command():
    """
    Prompts the user to enter a command
    """
    user_input = ""
    # prompt the user until a valid command is entered
    while user_input not in COMMANDS.keys():
        user_input = get_styled_input(f"Enter '{const.RESTART}' to search again, or '{const.QUIT}' to quit the program")
    handle_commands(user_input)
