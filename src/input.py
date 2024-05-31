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
        name = input("Enter a restaurant name: ")
        if name:
            break
        print("The restaurant name cannot be blank")
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

def output_site_ratings(site_ratings):
    """
    Displays the ratings of the websites
    :param list site_ratings - a list of tuples, where each tuple is in the form (<website>, <rating>, <number of reviews>)
    """
    for site_rating in site_ratings:
        print(f"{site_rating[0]} - {site_rating[1]} stars, {site_rating[2]} reviews")