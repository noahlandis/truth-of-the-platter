"""
This module controls the flow of the program.
It reads the user input, scrapes the ratings and review counts for the given restaurant, and prints the results.
Author: Noah Landis
"""
import logging
import os

import bugsnag
import geocoder
from bugsnag.handlers import BugsnagHandler
from dotenv import load_dotenv

from calculate_weighted_average import \
    get_weighted_average_and_total_review_count
from cli_command import prompt_next_command
from exceptions import NoResultsFoundError
from input import (display_results, display_welcome_message,
                   output_site_ratings, read_input)
from scrape import scrape

logger = logging.getLogger()


def _get_name_and_location():
    name, location = read_input()
    if not location:
        try:
            g = geocoder.ip('me')
            location = f"{g.city}, {g.state}"
            logger.info(f"Retrieved location: {location}")
        except Exception as e:
            logger.error(f"Error retrieving location: {e}")
    

    return name, location

def setup():
    load_dotenv()

    bugsnag.configure(
        api_key=os.getenv('BUGSNAG_API_KEY'),
    )

    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("app.log")
    ])
    handler = BugsnagHandler()
    # Send only ERROR-level logs and above
    handler.setLevel(logging.WARNING)
    logger.addHandler(handler)


def main():
    """
    Controls the flow of the program
    """
    setup()

    display_welcome_message()
    name, location = _get_name_and_location()
    while True:
        try:
            site_ratings, full_name, address = scrape(name, location)
            break
        except NoResultsFoundError as e:
            print(e)
            name, location = _get_name_and_location()

    output_site_ratings(site_ratings, full_name, address)
    star_average, total_review_count = get_weighted_average_and_total_review_count(site_ratings)
    display_results(full_name, star_average, total_review_count)
    prompt_next_command()

if __name__ == "__main__":
    main()