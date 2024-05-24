"""
This module handles the main scraping logic.
Given a restaurant name and a city, it identifies potential matching restaurants on Yelp.
The user is then prompted to select their intended restaurant from the list of potential matches.
The ratings and review counts for the selected restaurant are then scraped from Yelp and Google, and the results are printed.
Author: Noah Landis
"""

import requests
from bs4 import BeautifulSoup
from model.yelp import Yelp, ROOT as YELP_ROOT
from model.google import Google
from input import get_user_selection
from string_utils import is_potential_match, extract_review_count

# list of websites to scrape
WEBSITES = [Yelp(), Google()]

def scrape(name: str, city: str) -> list:
    """
    Scrapes the ratings and review counts for the given restaurant name and city from Yelp and Google
    :param str name - the name of the restaurant
    :param str city - the city the restaurant is in
    :return list results - a list of tuples, where each tuple is in the form (<website name>, <rating>, <review count>)
    """
    results = []
    for i in range(len(WEBSITES)):
        url = WEBSITES[i].build_url(name, city)
        page = get_html(url)

        # we first scrape Yelp to collect the name, address, and associated page for each restaurant which closely matches the user's input
        if i == 0:

            # get the pages, full names, and addresses of potential yelp restaurants
            potential_yelp_restaurants = get_potential_yelp_restaurants(name, page)

            # determine the intended restaurant
            selected_index = get_user_selection(potential_yelp_restaurants)
            page = potential_yelp_restaurants[selected_index][0]
            yelp_name = potential_yelp_restaurants[selected_index][1]
            yelp_address = potential_yelp_restaurants[selected_index][2]

            # we now have the full name and address of the intended restaurant, so we can use it for more accurate scraping in the future
            name = yelp_name
            city = yelp_address

        # get the rating and review count for the given website
        website_name = WEBSITES[i].__class__.__name__
        rating_and_review_count = WEBSITES[i].get_rating_and_review_count(page)
        rating = rating_and_review_count[0]
        review_count = extract_review_count(rating_and_review_count[1])
        results.append((website_name, rating, review_count))

    return results

def get_html(url: str) -> BeautifulSoup:
    """
    Returns the HTML for a particular URL
    :param str url - The URL to get the HTML for
    :return BeautifulSoup page - the HTML for the given URL
    """
    response = requests.get(url, headers={'User-Agent': "Mozilla/5.0"})
    print(response.status_code) # test to make sure this is 200
    page = BeautifulSoup(response.text, 'html.parser')
    return page

def get_potential_yelp_restaurants(name: str, yelp_search_results: BeautifulSoup) -> list:
    """
    Searches Yelp to get the HTML, full names, and addresses of restaurants that match the user's input
    :param str name - the name of the restaurant
    :param BeautifulSoup yelp_search_results - the HTML of the search results page
    :return list potential_yelp_restaurants - a list of tuples, where each tuple is in the form (<page>, <yelp_name>, <yelp_address>)
    """
    yelp_name_tags = yelp_search_results.select('[class*="businessName"]', limit=10)

    # store the potential yelp restaurants in the form of [<yelp_page>, <yelp_name>, <yelp_address>]
    potential_yelp_restaurants = []
    
    # iterate over the search results to find potential matches
    for tag in yelp_name_tags:
        yelp_name = tag.get_text(strip=True)
        
        # we only care about yelp restaurants with names that are potential matches
        if is_potential_match(name, yelp_name):

            # remove integer and period as it isn't relevant
            yelp_name = yelp_name[2::]

            # get the html for restaurant's page
            restaurant_url = tag.find('a', href=True)['href']
            url = f"{YELP_ROOT}" + restaurant_url
            yelp_page = get_html(url)

            # get the address of the restaurant
            element = yelp_page.find(string="Get Directions")
            yelp_address = element.parent.parent.next_sibling.string
            potential_yelp_restaurants.append((yelp_page, yelp_name, yelp_address))

    return potential_yelp_restaurants


