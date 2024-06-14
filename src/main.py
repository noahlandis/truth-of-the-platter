"""
This module controls the flow of the program.
It reads the user input, scrapes the ratings and review counts for the given restaurant, and prints the results.
Author: Noah Landis
"""

from cli_command import prompt_next_command
from scrape import scrape
from input import read_input, output_site_ratings, display_results, display_welcome_message
from calculate_weighted_average import get_weighted_average_and_total_review_count
from exceptions import NoResultsFoundError

def main():
    """
    Controls the flow of the program
    """
    display_welcome_message()
    name, city, state = read_input()
    while True:
        try:
            site_ratings, full_name, address = scrape(name, city, state)
            break
        except NoResultsFoundError as e:
            print(e)
            name, city = read_input()

    output_site_ratings(site_ratings, full_name, address)
    star_average, total_review_count = get_weighted_average_and_total_review_count(site_ratings)
    display_results(full_name, star_average, total_review_count)
    prompt_next_command()
    
if __name__ == "__main__":
    main()