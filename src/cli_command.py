"""
This module contains the functions to handle user commands
Author: Noah Landis
"""

import os
import sys
from colorama import Style
from utils.styled_cli_utils import MessageType, get_styled_input, get_styled_output

COMMANDS = {
    "\\h": "Display this help menu",
    "\\r": "Restart the program",
    "\\q": "Quit the program"
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
        case "\\h":
            display_commands()
            return True
        case "\\r":
            # we want a new line to make it clear the program is restarting
            print()
            os.execl(sys.executable, sys.executable, *sys.argv)
        case "\\q":
            sys.exit()
    return False

def prompt_next_command():
    """
    Prompts the user to enter a command
    """
    user_input = ""
    # prompt the user until a valid command is entered
    while user_input not in COMMANDS.keys():
        user_input = get_styled_input("Enter '\\r' to search again, or '\\q' to quit the program")
    handle_commands(user_input)
