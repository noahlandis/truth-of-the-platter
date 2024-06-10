"""
This module handles the user input logic.
It reads the user input to be used in website search and allows the user to select their intended restaurant from a list of potential matches.
Author: Noah Landis
"""
from exceptions import IntendedRestaurantNotFoundError
from colorama import Fore, Style
from styled_console import print_info, print_warning, get_input
UNDERLINE_START = "\033[4m"
UNDERLINE_END = "\033[0m"

def read_input() -> tuple:
    """
    Reads the user input to be used in website search
    :return tuple - a tuple containing the user's inputted restaurant in the format (<name>, <city>)
    """
    while True:
        name = input(f"{Fore.CYAN}Enter a restaurant name:{Fore.GREEN} ")
        if name:
            break
        print(f"{Fore.YELLOW}The restaurant name cannot be blank.")
    city = input(f"{Fore.CYAN}Enter the name of a city:{Fore.GREEN} ")
    print(f"{Fore.LIGHTBLACK_EX}Loading...")
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

    # continuously prompt user to indicate their intended restaurant until they provide valid input 
    while True:
        try:
            for i in range(len(yelp_potential_matches)):
                print(f"{Fore.LIGHTMAGENTA_EX}{Style.BRIGHT}{str(i)}{Style.RESET_ALL}{Fore.LIGHTMAGENTA_EX}: {str(yelp_potential_matches[i][1])} - {yelp_potential_matches[i][2]}")      
            print(f"{Fore.LIGHTBLACK_EX}Enter the number corresponding to the restaurant you had in mind\n{UNDERLINE_START}OR{UNDERLINE_END}\n{Fore.LIGHTBLACK_EX}not seeing the restaurant you were looking for? Enter -1 to search again!")
            selected_index = int(input(f"{Fore.CYAN}Enter your selection:{Fore.GREEN} "))
            if selected_index == -1:
                raise IntendedRestaurantNotFoundError
            
            # python allows negative indexing, but we still raise an error as the number should correspond to the list
            elif selected_index < -1:
                raise IndexError
            intended_restaurant = yelp_potential_matches[selected_index]
            break
        except (IndexError, ValueError):
            print(f"{Fore.YELLOW}The number you enter must correspond to one of the listed restaurants.")
    return intended_restaurant

def output_site_ratings(site_ratings: list, full_name: str, address: str):
    """
    Displays the ratings of the websites
    :param list site_ratings - a list of tuples, where each tuple is in the form (<website>, <rating>, <number of reviews>)
    :param str full_name - the full name of the restaurant
    :param str address - the address of the restaurant
    """
    print(f"{Fore.LIGHTBLACK_EX}Showing Results for {full_name} - {address}...")
    for site_rating in site_ratings:
        print(f"{Fore.LIGHTMAGENTA_EX}{site_rating[0]} - {site_rating[1]} stars, {site_rating[2]} reviews")

def display_results(full_name: str, star_average: str, total_review_count: str):
    """
    Displays the weighted average and the total number of reviews
    :param str full_name -  the full name of the restaurant
    :param str star_average - the weighted average of the star ratings, rounded to 2 decimal places
    :param str total_review_count - the sum of the review counts across all scraped websites
    """
    print(f"{Fore.MAGENTA}{Style.BRIGHT}A more accurate rating of {full_name} is {star_average} stars, {total_review_count} reviews{Style.RESET_ALL}")
