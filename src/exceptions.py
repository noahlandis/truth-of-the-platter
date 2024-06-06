"""
This module contains custom Exceptions
Author: Noah Landis
"""

class NoResultsFoundError(Exception):
    """
    Exception raised when no Yelp results are found for the given restaurant
    """
    pass

class IntendedRestaurantNotFoundError(Exception):
    """
    Exception raised when the user indicates that their intended restaurant was not
    one of the collected Yelp matches
    """
    pass
