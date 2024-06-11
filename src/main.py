"""
This module controls the flow of the program.
It reads the user input, scrapes the ratings and review counts for the given restaurant, and prints the results.
Author: Noah Landis
"""

import time
from scrape import scrape
from input import read_input, output_site_ratings, display_results
from calculate_weighted_average import get_weighted_average_and_total_review_count
from exceptions import NoResultsFoundError, IntendedRestaurantNotFoundError
from colorama import init

def main():
    init(autoreset=True)
    name, city = read_input()
    while True:
        try:
            site_ratings, full_name, address = scrape(name, city)
            break
        except (NoResultsFoundError, IntendedRestaurantNotFoundError) as e:
            print(e)
            name, city = read_input()

            # sleep to avoid block caused by multiple requests in a short duration
            time.sleep(10)

    output_site_ratings(site_ratings, full_name, address)
    star_average, total_review_count = get_weighted_average_and_total_review_count(site_ratings)
    display_results(full_name, star_average, total_review_count)
    
if __name__ == "__main__":
    main()