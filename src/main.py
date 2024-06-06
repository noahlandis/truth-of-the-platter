"""
This module controls the flow of the program.
It reads the user input, scrapes the ratings and review counts for the given restaurant, and prints the results.
Author: Noah Landis
"""

from scrape import scrape
from input import read_input, output_site_ratings
from exceptions import NoResultsFoundError, IntendedRestaurantNotFoundError

def main():
    name, city = read_input()
    while True:
        try:
            site_ratings, full_name, address = scrape(name, city)
            break
        except (NoResultsFoundError, IntendedRestaurantNotFoundError) as e:
            print(e)
            name, city = read_input()

    output_site_ratings(site_ratings, full_name, address)

if __name__ == "__main__":
    main()