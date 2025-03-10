"""
This module contains the concrete class TripAdvisor.
Author: Noah Landis
"""

import re
import os
from bs4 import BeautifulSoup

from model.google import Google
from model.website import Website
from utils.string_utils import is_potential_match, extract_review_count
import requests

class TripAdvisor(Website):
    ROOT = "https://www.google.com"

    @staticmethod
    def build_url(name: str, location: str) -> str:
        """
        Builds the URL to search for a restaurant on Google, to scrape TripAdvisor info from Google's rich snippets 
        :param str name - the name of the restaurant
        :param str location - the location of the restaurant
        :return str url - the URL to search for the restaurant
        """
        return Google.build_url(name, location)

    @staticmethod
    def _get_rating_and_review_count_scrape(page: BeautifulSoup) -> tuple:
        """
        Scrapes the rating and review count from the TripAdvisor rich snippet
        :param BeautifulSoup page - the page to scrape
        :return tuple (<rating>, <review_count>) - the rating and review count for the restaurant
        """
        # find the div that contains the tripadvisor link
        div = page.find('div', class_='BNeawe UPmit AP7Wnd lRVwie', string=re.compile('www.tripadvisor.com'))
        trip_advisor_description = div.parent.parent.parent.parent.next_sibling
        span = trip_advisor_description.find('span', class_='r0bn4c rQMQod tP9Zud')

        # strip the text and turn it into a list so it can be parsed
        rating_and_review_count = list(span.stripped_strings)
        rating = rating_and_review_count[0]
        review_count = rating_and_review_count[1]
        return rating, extract_review_count(review_count)

    @staticmethod
    def _get_rating_and_review_count_api(name: str, location: str) -> tuple:
        search_query = f"{name} {location}"
        # first we do search with filtered address
        
        url = f"https://api.content.tripadvisor.com/api/v1/location/search?key={os.getenv('TRIPADVISOR_API_KEY')}&language=en&category=restaurants&searchQuery={name}&address={location}"
        response = requests.get(url, headers={"accept": "application/json"})
        restaurant_data = response.json()['data']
        location_id = None
        if len(restaurant_data) == 0:
            # we do a more general search if we don't find anything
            url = f"https://api.content.tripadvisor.com/api/v1/location/search?key={os.getenv('TRIPADVISOR_API_KEY')}&language=en&category=restaurants&searchQuery={search_query}"
            response = requests.get(url, headers={"accept": "application/json"})
            location_id = response.json()['data'][0]['location_id']
        else:
            location_id = restaurant_data[0]['location_id']
        details_url = f"https://api.content.tripadvisor.com/api/v1/location/{location_id}/details?key={os.getenv('TRIPADVISOR_API_KEY')}&language=en"
        details_response = requests.get(details_url, headers={"accept": "application/json"})
        details_response_json = details_response.json()
        rating = details_response_json['rating']
        review_count = details_response_json['num_reviews']
        return rating, review_count
