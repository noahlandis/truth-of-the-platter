"""
This module handles the main scraping logic.
Given a restaurant name and a location, it identifies potential matching restaurants on Yelp, where a match is defined as the restaurant the user intended to search for.
The user is then prompted to select their intended restaurant from the list of potential matches.
The ratings and review counts for the selected restaurant are then scraped from Yelp, Google, and TripAdvisor and the results are printed.
Author: Noah Landis
"""

import logging

import requests
from bs4 import BeautifulSoup

from server.src.model.google import Google
from server.src.model.tripadvisor import TripAdvisor
from server.src.model.yelp import Yelp

logger = logging.getLogger()

# list of websites to scrape
WEBSITES = [Google, Yelp, TripAdvisor]

def scrape(name, location, source) -> tuple:
    """
    Scrapes the ratings and review counts for the given restaurant name and location from Yelp, Google, and TripAdvisor.
    :param dict yelp_info: Dictionary containing restaurant details from Yelp.
    :return tuple results: A tuple containing:
        - a list of tuples with the form (<website name>, <rating>, <review count>)
        - the full name of the restaurant
        - the address of the restaurant
    """
    last_url = ""    
    results = []
    for i in range(len(WEBSITES)):
        if WEBSITES[i].__name__ == source:
            continue
        url = WEBSITES[i].build_url(name, location)

        if url != last_url:
            page = get_html(url)
            last_url = url

        # Get the rating and review count for the given website
        website_name = WEBSITES[i].__name__
        rating, review_count = WEBSITES[i].get_rating_and_review_count(name, location, page)
        results.append((website_name, rating, review_count))

    return results

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