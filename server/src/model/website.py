"""
This module contains the abstract class Website.
Author: Noah Landis
"""

import logging
from abc import ABC, abstractmethod

from bs4 import BeautifulSoup

logger = logging.getLogger()

class Website(ABC):
    """
    Abstract class representing a generic website to scrape
    """
    
    @staticmethod
    @abstractmethod
    def build_url(name: str, location: str) -> str:
        """
        Builds the URL to search for a restaurant on the website
        :param str name - the name of the restaurant
        :param str location - the location the restaurant
        :return str url - the URL to search for the restaurant
        """

    @classmethod
    def get_rating_and_review_count(cls, page: BeautifulSoup) -> tuple:
        """
        Scrapes the rating and review count from the given page
        :param BeautifulSoup page - the page to scrape
        :return tuple (<rating>, <review_count>) - the rating and review count for the restaurant, or (<None>, <None>) if the rating and review couldn't be parsed
        """
        try:
            return cls._get_rating_and_review_count(page)
        # handle case when the rating and review count couldn't be parsed
        except AttributeError as e:
            # logger.warning(f"Couldn't parse rating and review count: {e}")
            return None, None
        
    @staticmethod
    @abstractmethod
    def _get_rating_and_review_count(page: BeautifulSoup) -> tuple:
        pass




