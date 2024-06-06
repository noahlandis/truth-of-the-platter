"""
This module contains the concrete class Yelp.
Author: Noah Landis
"""

from bs4 import BeautifulSoup
from model.website import Website
from string_utils import extract_review_count

class Yelp(Website):
    ROOT = "https://www.yelp.com"

    @staticmethod
    def build_url(name: str, city: str) -> str:
        """
        Builds the URL to search for a restaurant on Yelp
        :param str name - the name of the restaurant
        :param str city - the city the restaurant is in
        :return str url - the URL to search for the restaurant
        """
        return f"{Yelp.ROOT}/search?find_desc={name}&find_loc={city}"

    @staticmethod
    def get_rating_and_review_count(page: BeautifulSoup) -> tuple:
        """
        Scrapes the rating and review count from the Yelp page
        :param BeautifulSoup page - the page to scrape
        :return tuple (<rating>, <review_count>) - the rating and review count for the restaurant
        """
        div = page.find('div', class_='arrange-unit__09f24__rqHTg arrange-unit-fill__09f24__CUubG y-css-lbeyaq')
        span_tags = div.find_all('span')
        rating = span_tags[0].get_text(strip=True)
        review_count = span_tags[1].get_text(strip=True)
        return rating, extract_review_count(review_count)
    
  