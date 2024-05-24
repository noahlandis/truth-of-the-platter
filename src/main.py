"""
This module controls the flow of the program.
It reads the user input, scrapes the ratings and review counts for the given restaurant, and prints the results.
Author: Noah Landis
"""

from scrape import scrape
from input import read_input

def main():
    name, city = read_input()
    ratings_and_reviews = scrape(name, city)
    print(ratings_and_reviews)

if __name__ == "__main__":
    main()