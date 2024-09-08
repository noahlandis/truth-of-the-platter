


import logging

import requests

from .cli_command import get_input_with_command_handling, prompt_next_command
from .input import display_results, display_welcome_message, get_intended_restaurant, output_site_ratings, read_input
from server.src.services.calculate_weighted_average_service import get_weighted_average_and_total_review_count
from server.src.exceptions import NoResultsFoundError, UserLocationNotFoundError
from server.src.services.scrape_service import scrape
from server.src.services.user_location_service import get_user_location
from server.src.services.yelp_service import get_yelp_matches

from .utils.styled_cli_utils import MessageType, get_styled_output


FLASK_APP_URL = "http://127.0.0.1:5000"

logger = logging.getLogger(__name__)



def _get_name_and_location():
    name, location = read_input()
    if not location:
        try:
            location = get_user_location()
            print(get_styled_output(f"No location entered. Using your location: {location}", MessageType.INFO))
        except UserLocationNotFoundError as e:
            print(get_styled_output(f"An error occurred while trying to get your location. The location is now required", MessageType.ERROR))
            while True:
                location = get_input_with_command_handling("Enter the location")
                if location:
                    break
                print(get_styled_output("The location cannot be blank.", MessageType.WARNING))
    return name, location

def run_cli():
    """
    Controls the flow of the program
    """
    
    display_welcome_message()
    name, location = _get_name_and_location()
    get_yelp_matches(name, location)
    # while True:
    #     try:
    #         params = {'name': name, 'location': location}
    #         print(get_styled_output(f"Searching for {name} near {location}", MessageType.INFO))
    #         print(get_styled_output("Loading...", MessageType.INFO))
    #         response = requests.get(f"{FLASK_APP_URL}/search", params=params)
    #         if response.status_code == 404:
    #             raise NoResultsFoundError(response.json()['error'])
    #         yelp_matches = response.json()
        
    #         intended_restaurant = get_intended_restaurant(yelp_matches)

    #         site_ratings = []
    #         # since we got the Yelp data from the API, we can add it to the results right away
    #         site_ratings.append(("Yelp", str(intended_restaurant['rating']), str(intended_restaurant['review_count'])))

    #         # we use the more detailed name and location from the Yelp data to help us scrape the other sites
    #         full_name = intended_restaurant['name']
    #         full_location = intended_restaurant['location']

    #         # append the Google and TripAdvisor ratings and review counts to the results
    #         site_ratings.extend(scrape(full_name, full_location))
    #         break
    #     except NoResultsFoundError as e:
    #         print(get_styled_output(e, MessageType.ERROR))
    #         name, location = _get_name_and_location()

    # output_site_ratings(site_ratings, full_name, full_location)
    # star_average, total_review_count = get_weighted_average_and_total_review_count(site_ratings)
    # display_results(full_name, star_average, total_review_count)
    prompt_next_command()
