"""
This module handles the main scraping logic.
Given a restaurant name and a city, it identifies potential matching restaurants on Yelp, where a match is defined as the restaurant the user intended to search for.
The user is then prompted to select their intended restaurant from the list of potential matches.
The ratings and review counts for the selected restaurant are then scraped from Yelp, Google, and TripAdvisor and the results are printed.
Author: Noah Landis
"""

import requests
from bs4 import BeautifulSoup
from model.yelp import Yelp
from model.google import Google
from model.tripadvisor import TripAdvisor
from input import get_intended_restaurant
from exceptions import NoResultsFoundError
from utils.string_utils import is_potential_match
from utils.styled_cli_utils import MessageType, get_styled_output

# list of websites to scrape
WEBSITES = [Yelp, Google, TripAdvisor]

def scrape(name: str, city: str) -> list:
    """
    Scrapes the ratings and review counts for the given restaurant name and city from Yelp, Google, and TripAdvisor
    :param str name - the name of the restaurant
    :param str city - the city the restaurant is in
    :return tuple results - a list of tuples, where each tuple is in the form (<website name>, <rating>, <review count>), the full name of the restaurant, and the address of the restaurant
    """
    last_url = ""
    results = []
    for i in range(len(WEBSITES)):
        url = WEBSITES[i].build_url(name, city)

        # since TripAdvisor's API costs money, we scrape the data from the TripAdvisor rich snippet from the Google results. Therefore, we only need to send one request to the Google URL.
        if url != last_url:
            page = get_html(url)
            last_url = url

        # we first scrape Yelp to collect the name, address, and associated page for each restaurant which closely matches the user's input
        if i == 0:
            yelp_page, yelp_name, yelp_address = get_yelp_data(name, city, page)

            # we update the page to the individual restaurant's yelp page so we can scrape the rating and review count
            page = yelp_page

            # we now have the full name and address of the intended restaurant, so we can use it for more accurate scraping in the future
            name = yelp_name
            city = yelp_address

        # get the rating and review count for the given website
        website_name = WEBSITES[i].__name__
        rating, review_count = WEBSITES[i].get_rating_and_review_count(page)
        results.append((website_name, rating, review_count))
    
    return results, name, city

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

def get_yelp_data(name: str, city: str, page: BeautifulSoup) -> tuple:
    """
    Handles the Yelp scraping to get the intended restaurant details and returns the page, name, and address corresponding to the intended restaurant
    :param str name - the name of the restaurant
    :param str city - the city the restaurant is in
    :param BeautifulSoup page - the Yelp search results page
    :return tuple - the page, name, and address of the intended restaurant as displayed on Yelp 
    :raises NoResultsFoundError - if no yelp results match the user's input 
    """
    # get the pages, full names, and addresses of yelp restaurants which potentially match the restaurant the user had in mind
    yelp_potential_matches = get_yelp_potential_matches(name, page)
    if not yelp_potential_matches:
        raise NoResultsFoundError(get_styled_output(f"No results could be found for \"{name}\" located in \"{city}\". Please try again...", MessageType.ERROR))
    intended_restaurant = get_intended_restaurant(yelp_potential_matches)
    yelp_page, yelp_name, yelp_address = intended_restaurant
    return yelp_page, yelp_name, yelp_address

def get_yelp_potential_matches(name: str, yelp_search_results: BeautifulSoup) -> list:
    """
    Searches Yelp to get the HTML, full names, and addresses of restaurants that match the user's input
    :param str name - the name of the restaurant
    :param BeautifulSoup yelp_search_results - the HTML of the search results page
    :return list yelp_potential_matches - a list of tuples, where each tuple is in the form (<page>, <yelp_name>, <yelp_address>)
    """
    yelp_name_tags = yelp_search_results.select('[class*="businessName"]', limit=10)

    # store the potential yelp restaurants in the form of [<yelp_page>, <yelp_name>, <yelp_address>]
    yelp_potential_matches = []
    
    # iterate over the search results to find potential matches
    for tag in yelp_name_tags:
        yelp_name = tag.get_text(strip=True)
        
        # we only care about yelp restaurants with names that are potential matches
        if is_potential_match(name, yelp_name):

            # remove integer and period as it isn't relevant
            yelp_name = yelp_name[2::]

            # we store the pages of the individual restaurants so we can scrape the rating and review count of the intended restaurant later
            restaurant_url = tag.find('a', href=True)['href']
            url = f"{Yelp.ROOT}" + restaurant_url
            yelp_page = get_html(url)

            # get the address of the restaurant
            yelp_address = yelp_page.find('p', class_='y-css-dg8xxd').get_text(strip=True)
            yelp_potential_matches.append((yelp_page, yelp_name, yelp_address))

    return yelp_potential_matches


