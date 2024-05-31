"""
This module controls the flow of the program.
It reads the user input, scrapes the ratings and review counts for the given restaurant, and prints the results.
Author: Noah Landis
"""

from scrape import scrape
from input import read_input, output_site_ratings

def main():
    name, city = read_input()
    site_ratings = scrape(name, city)
    output_site_ratings(site_ratings)

if __name__ == "__main__":
    main()