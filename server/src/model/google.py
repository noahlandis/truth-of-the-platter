"""
This module contains the concrete class Google.
Author: Noah Landis
"""

from bs4 import BeautifulSoup

from model.website import Website
from utils.string_utils import extract_review_count
from model.api_handler import GooglePlacesApiHandler

class Google(Website):
    ROOT = "https://www.google.com"

    @staticmethod
    def build_url(name: str, location: str) -> str:
        """
        Builds the URL to search for a restaurant on Google
        :param str name - the name of the restaurant
        :param str location - the location the restaurant
        :return str url - the URL to search for the restaurant
        """
        # Replace the ampersand with "and" to avoid URL encoding issues
        name = name.replace("&", "and")
        return f"{Google.ROOT}/search?q={name} {location}"

    @staticmethod
    def _get_rating_and_review_count_scrape(page: BeautifulSoup) -> tuple:
        """
        Scrapes the rating and review count from the Google page
        :param BeautifulSoup page - the page to scrape
        :return tuple (<rating>, <review_count>) - the rating and review count for the restaurant
        """
        div = page.find('div', class_='BNeawe tAd8D AP7Wnd')
        rating_tag = div.find('span', class_='oqSTJd')
        rating = rating_tag.get_text(strip=True)
        review_count = rating_tag.next_sibling.next_sibling.next_sibling.next_sibling.get_text(strip=True)
        return rating, extract_review_count(review_count)
    
    @staticmethod
    def _get_rating_and_review_count_api(name: str, location: str) -> tuple:
        # since we already know the exact restaurant, we can pass the full name and location to the api and extract the rating and review count from the result
        results = GooglePlacesApiHandler().process_request(name, location)
        # given that the name and location are fully specified (based on the user selection), we can be fairly confident that the result will be the rating and review count of the restaurant the user intended to find ratings for.
        restaurant = results[0]
        print(restaurant['rating'])
        print(restaurant['user_ratings_total'])
        return str(restaurant['rating']), str(restaurant['user_ratings_total'])
 