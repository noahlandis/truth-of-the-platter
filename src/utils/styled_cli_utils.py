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

def get_styled_input(message: str, is_optional: bool=False) -> str:
    """
    Returns a styled input prompt to be printed to the console
    :param str message - the message to be styled
    :bool is_optional - indicates whether or not the field is optional
    :return str - the styled message
    """
    prompt_str = f"{MessageType.PROMPT.value}{message}"
    if is_optional:
        prompt_str += f"{MessageType.INFO.value} (optional)"
    prompt_str += f"{MessageType.PROMPT.value}:"
    return input(f"{prompt_str}{MessageType.INPUT.value} ").strip()
