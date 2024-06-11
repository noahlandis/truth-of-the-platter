"""
Utility class to handle styling CLI input and output.
Author: Noah Landis
"""
from colorama import Fore
from enum import Enum

class MessageType(Enum):
    """
    Defines the colors to be applied based on the type of message
    """
    INFO = Fore.LIGHTBLACK_EX
    WARNING = Fore.YELLOW
    ERROR = Fore.RED
    PROMPT = Fore.CYAN
    INPUT = Fore.GREEN
    LIST_RESULT = Fore.LIGHTMAGENTA_EX
    WELCOME = FINAL_RESULT = Fore.MAGENTA

def get_styled_output(message: str, message_type: MessageType) -> str:
    """
    Returns a styled message to be printed to the console
    :param str message - the message to be styled
    :param MessageType message_type - the type of message to be styled
    :return str - the styled message
    """
    return f"{message_type.value}{message}"

def get_styled_input(message: str) -> str:
    """
    Returns a styled input prompt to be printed to the console
    :param str message - the message to be styled
    :return str - the styled message
    """
    return input(f"{MessageType.PROMPT.value}{message}:{MessageType.INPUT.value} ")
