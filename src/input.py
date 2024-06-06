"""
This module handles the user input logic.
It reads the user input to be used in website search and allows the user to select their intended restaurant from a list of potential matches.
Author: Noah Landis
"""
from exceptions import IntendedRestaurantNotFoundError
def read_input() -> tuple:
    """
    Reads the user input to be used in website search
    :return tuple - a tuple containing the user's inputted restaurant in the format (<name>, <city>)
    """
    while True:
        name = input("Enter a restaurant name: ")
        if name:
            break
        print("The restaurant name cannot be blank.")
    city = input("Enter the name of a city: ")
    return name, city

def get_intended_restaurant(yelp_potential_matches: list) -> tuple:
    """
    Allows the user to select their intended restaurant from a list of potential matches (if multiple matches exist)
    :param list search_results - a list of tuples, where each tuple is in the form (<website page>, <name>, <address>)
    :return tuple intended_restaurant - a tuple representing the restaurant selected by the user, in the form (<website page>, <name>, <address>)
    :raises IntendedRestaurantNotFoundError - if user enters -1, indicating that the restaurant they're looking was not one of the yelp matches
    """

    # if there's only one potential match, return it
    if len(yelp_potential_matches) == 1:
        return yelp_potential_matches[0]
    
    # otherwise, determine the intended restaurant
    for i in range(len(yelp_potential_matches)):
        print(str(i) + ": " + str(yelp_potential_matches[i][1] + " - " + yelp_potential_matches[i][2]))  

    # continuously prompt user to indicate their intended restaurant until they provide valid input 
    while True:
        try:    
            print("Enter the number corresponding to the restaurant you had in mind\nOR\nnot seeing the restaurant you were looking for? Enter -1 to search again!")
            selected_index = int(input("Enter your selection: "))

            if selected_index == -1:
                raise IntendedRestaurantNotFoundError
            intended_restaurant = yelp_potential_matches[selected_index]
            break
        except (IndexError, ValueError):
            print("The number you enter must correspond to one of the listed restaurants.")
    return intended_restaurant

def output_site_ratings(site_ratings: list, full_name: str, address: str):
    """
    Displays the ratings of the websites
    :param list site_ratings - a list of tuples, where each tuple is in the form (<website>, <rating>, <number of reviews>)
    :param str full_name - the full name of the restaurant
    :param str address - the address of the restaurant
    """
    print(f"Showing Results for {full_name} - {address}...")
    for site_rating in site_ratings:
        print(f"{site_rating[0]} - {site_rating[1]} stars, {site_rating[2]} reviews")