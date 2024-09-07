import logging
import os

import requests

from exceptions import NoResultsFoundError
from utils.string_utils import is_potential_match

logger = logging.getLogger()

def get_yelp_matches(name, location):
    try:
        yelp_restaurants = _collect_yelp_restaurants_graph_ql(name, location)['data']['search']['business']
    except:
        logger.info('Trying regular API')
        yelp_restaurants = _collect_yelp_restaurants_regular_api(name, location)

    if not yelp_restaurants:
        raise NoResultsFoundError(f'No results could be found for {name} located in {location}. Please try again...')

    # filter matches
    filtered_restaurants = [
        {
            'name': yelp_restaurant['name'],
            'location': f"{yelp_restaurant['location']['address1']} {yelp_restaurant['location']['city']}, {yelp_restaurant['location']['state']}",
            'review_count': yelp_restaurant['review_count'],
            'rating': yelp_restaurant['rating']
        }
        for yelp_restaurant in yelp_restaurants
        if is_potential_match(name, yelp_restaurant['name'])
    ]
    
    if not filtered_restaurants:
        raise NoResultsFoundError(f'No results could be found for {name} located in {location}. Please try again...')

    
    return filtered_restaurants


def _collect_yelp_restaurants_graph_ql(name, location):
    # Get the API key from the .env file
    api_key = os.getenv('YELP_API_KEY')

    # Define the headers with your API key
    url = 'https://api.yelp.com/v3/graphql'

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    # Define the GraphQL query
    query = '''
    query SearchBusinesses($term: String!, $location: String!) {
        search(term: $term, location: $location, limit: 5) {
            business {
                name
                location {
                    address1
                    city
                    state
                    country
                }
                review_count
                rating
            }
        }
    }
    '''

    # Define the variables
    variables = {
        "term": name,
        "location": location
    }

    # Make the request to the Yelp GraphQL API
    response = requests.post(url, headers=headers, json={'query': query, 'variables': variables})

    # Parse and print the response
    if response.status_code == 200:
        business_data = response.json()
        return business_data
    else:
        logger.info(f'Error getting Yelp restaurants for GraphQL API: {response.text}')


def _collect_yelp_restaurants_regular_api(name, location):
    # Get the API key from the .env file
    api_key = os.getenv('YELP_API_KEY')

    # Define the endpoint and parameters for the regular Yelp API
    url = 'https://api.yelp.com/v3/businesses/search'
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    params = {
        'term': name,
        'location': location,
        'limit': 5
    }

    # Make the request to the Yelp API
    response = requests.get(url, headers=headers, params=params)

    # Parse and return the response
    if response.status_code == 200:
        business_data = response.json()
        return business_data['businesses']
    else:
        logger.error(f'Error getting Yelp restaurants for Regular API: {response.text}')