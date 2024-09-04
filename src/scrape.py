"""
This module handles the main scraping logic.
Given a restaurant name and a location, it identifies potential matching restaurants on Yelp, where a match is defined as the restaurant the user intended to search for.
The user is then prompted to select their intended restaurant from the list of potential matches.
The ratings and review counts for the selected restaurant are then scraped from Yelp, Google, and TripAdvisor and the results are printed.
Author: Noah Landis
"""

import concurrent.futures
import requests
from requests_ip_rotator import ApiGateway
from bs4 import BeautifulSoup
from model.yelp import Yelp
from model.google import Google
from model.tripadvisor import TripAdvisor
from input import get_intended_restaurant
from exceptions import NoResultsFoundError
from utils.string_utils import is_potential_match, remove_leading_number, extract_review_count
from utils.styled_cli_utils import MessageType, get_styled_output
from yelp_api import get_yelp_data
import logging
logger = logging.getLogger()

# list of websites to scrape
WEBSITES = [Google, TripAdvisor]

def scrape(name: str, location: str) -> list:
    """
    Scrapes the ratings and review counts for the given restaurant name and location from Yelp, Google, and TripAdvisor
    :param str name - the name of the restaurant
    :param str location- the location of the restaurant 
    :return tuple results - a list of tuples, where each tuple is in the form (<website name>, <rating>, <review count>), the full name of the restaurant, and the address of the restaurant
    """
    last_url = ""
    results = []
    yelp_data = get_yelp_data(name, location)
    name = yelp_data['name']
    location = yelp_data['location']
    results.append(("Yelp", str(yelp_data['rating']), f"{yelp_data['review_count']:,}"))
    for i in range(len(WEBSITES)):
        url = WEBSITES[i].build_url(name, location)

        # since TripAdvisor's API costs money, we scrape the data from the TripAdvisor rich snippet from the Google results. Therefore, we only need to send one request to the Google URL.
        if url != last_url:
            page = get_html(url)
            last_url = url

        # get the rating and review count for the given website
        website_name = WEBSITES[i].__name__
        rating, review_count = WEBSITES[i].get_rating_and_review_count(page)
        results.append((website_name, rating, review_count))
    
    return results, name, location

def get_html(url: str) -> BeautifulSoup:
    """
    Returns the HTML for a particular URL
    :param str url - The URL to get the HTML for
    :return BeautifulSoup page - the HTML for the given URL
    """

    response = requests.get(url, headers={'User-Agent': "Mozilla/5.0"})
    response.raise_for_status()
    page = BeautifulSoup(response.text, 'html.parser')
    return page
   


def is_captcha(page):
    return page.find('div', class_='h-captcha') is not None