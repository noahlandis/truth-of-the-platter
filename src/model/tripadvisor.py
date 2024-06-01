"""
This module contains the concrete class Yelp.
Author: Noah Landis
"""

import re
from bs4 import BeautifulSoup
from model.google import Google
from model.website import Website

class TripAdvisor(Website):
    ROOT = "https://www.google.com"

    @staticmethod
    def build_url(name: str, city: str) -> str:
        """
        Builds the URL to search for a restaurant on Google
        :param str name - the name of the restaurant
        :param str city - the city the restaurant is in
        :return str url - the URL to search for the restaurant
        """
        return Google.build_url(name, city)

    @staticmethod
    def get_rating_and_review_count(page: BeautifulSoup) -> tuple:
        """
        Scrapes the rating and review count from the Google page
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
        return rating, review_count

        
        

        
        print(list(rating_block.stripped_strings))
        # rating_tag = div.find('span', class_='oqSTJd')
        # rating = rating_tag.get_text(strip=True)
        # review_count = rating_tag.next_sibling.next_sibling.next_sibling.next_sibling.get_text(strip=True)
        # return rating, review_count


  