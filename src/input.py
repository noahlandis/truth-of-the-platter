"""
This module handles the user input logic.
It reads the user input to be used in website search and allows the user to select their intended restaurant from a list of potential matches.
Author: Noah Landis
"""

def read_input() -> tuple:
    """
    Reads the user input to be used in website search
    :return tuple - a tuple containing the user's inputted restaurant name and city
    """
    while True:
        name = input("Enter a restaraunt name: ")
        if name:
            break
        print("The restaraunt name cannot be blank")
    city = input("Enter the name of a city: ")
    return name, city


def get_intended_restaurant_index(search_results: list) -> int:
    """
    Allows the user to select their intended restaurant from a list of potential matches
    :param list search_results - a list of tuples, where each tuple is in the form (<website page>, <name>, <address>)
    :return int selection - the index of the user's selected restaurant
    """
    for i in range(len(search_results)):
        print(str(i) + ": " + str(search_results[i][1] + " - " + search_results[i][2]))
    selection = input("Enter a number to select what restaraunt you had in mind: ")
    return int(selection)