import logging
import os

import requests

from server.src.model.api_handler import YelpApiGraphQLHandler, YelpApiRegularHandler, GooglePlacesApiHandler
from exceptions import NoResultsFoundError, UnknownLocationError
from utils.string_utils import is_potential_match

logger = logging.getLogger()

def get_yelp_matches(name, location):
    chain = YelpApiGraphQLHandler(      
        YelpApiRegularHandler(
            GooglePlacesApiHandler()
        )
    )
    response = chain.handle(name, location)
    if response == 'LOCATION_NOT_FOUND':
        raise UnknownLocationError(f"Sorry... we we're not able to recognize {location} as a valid location. Please try again...")
    if not response:
        # if we don't get any results, we don't need to filter them
        raise NoResultsFoundError(f'No results could be found for {name} located in {location}. Please try again...')
    
    processed_handler = chain.get_processed_handler()
    
    filtered_restaurants = get_filtered_yelp_matches(response, name, processed_handler)
    if not filtered_restaurants:
        raise NoResultsFoundError(f'No results could be found for {name} located in {location}. Please try again...')
    return filtered_restaurants

def get_filtered_yelp_matches(yelp_restaurants, name, handler):
    """
    Filters the Yelp matches to only include potential matches
    """
    # filter matches
    filtered_restaurants = [
        handler.get_formatted_restaurant_data(yelp_restaurant)
        for yelp_restaurant in yelp_restaurants
        if is_potential_match(name, yelp_restaurant['name'])
    ]
    
    return filtered_restaurants

