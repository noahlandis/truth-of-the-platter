import logging
import os

import requests

from server.src.model.api_handler import YelpApiGraphQLHandler, YelpApiRegularHandler
from exceptions import NoResultsFoundError, UnknownLocationError
from utils.string_utils import is_potential_match

logger = logging.getLogger()

def get_yelp_matches(name, location):
    chain = YelpApiGraphQLHandler(      
        YelpApiRegularHandler(          
        )
    )
    response = chain.handle(name, location)
    if response == 'LOCATION_NOT_FOUND':
        raise UnknownLocationError(f"Sorry... we we're not able to recognize {location} as a valid location. Please try again...")
    if not response:
        # if we don't get any results, we don't need to filter them
        raise NoResultsFoundError(f'No results could be found for {name} located in {location}. Please try again...')
    filtered_restaurants = get_filtered_yelp_matches(response, name)
    if not filtered_restaurants:
        raise NoResultsFoundError(f'No results could be found for {name} located in {location}. Please try again...')
    return filtered_restaurants


def get_filtered_yelp_matches(yelp_restaurants, name):
    """
    Filters the Yelp matches to only include potential matches
    """
    
    # filter matches
    filtered_restaurants = [
        {
            'name': yelp_restaurant['name'],
            'location': f"{yelp_restaurant['location']['address1']} {yelp_restaurant['location']['city']}, {yelp_restaurant['location']['state']}",
            'review_count': yelp_restaurant['review_count'],
            'rating': yelp_restaurant['rating'],
            'imageUrl': yelp_restaurant['image_url'] if 'image_url' in yelp_restaurant else yelp_restaurant['photos'][0] if 'photos' in yelp_restaurant else None
        }
        for yelp_restaurant in yelp_restaurants
        if is_potential_match(name, yelp_restaurant['name'])
    ]
    print("The filtered restaurants are: ", filtered_restaurants)
    
    return filtered_restaurants
    
    