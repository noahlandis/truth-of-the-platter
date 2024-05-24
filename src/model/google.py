"""
This module contains the concrete class Google.
Author: Noah Landis
"""

from model.website import Website

class Google(Website):
    ROOT = "https://www.google.com"

    @staticmethod
    def build_url(name, city):
        """
        Builds the URL to search for a restaurant on Google
        :param str name - the name of the restaurant
        :param str city - the city the restaurant is in
        :return str url - the URL to search for the restaurant
        """
        return f"{Google.ROOT}/search?q={name} {city}"

    @staticmethod
    def get_rating_and_review_count(page):
        """
        Scrapes the rating and review count from the Google page
        :param page - the page to scrape
        :return tuple (<rating>, <review_count>) - the rating and review count for the restaurant
        """
        div = page.find('div', class_='BNeawe tAd8D AP7Wnd')
        rating_tag = div.find('span', class_='oqSTJd')
        rating = rating_tag.get_text(strip=True)
        review_count = rating_tag.next_sibling.next_sibling.next_sibling.next_sibling.get_text(strip=True)
        return rating, review_count
    
 