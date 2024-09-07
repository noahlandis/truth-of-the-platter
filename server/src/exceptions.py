"""
This module contains custom Exceptions
Author: Noah Landis
"""

class NoResultsFoundError(Exception):
    """
    Exception raised when no Yelp results are found for the given restaurant
    """


class UserLocationNotFoundError(Exception):
    """
    Exception raised when the user's location is not found
    """

class UnknownLocationError(Exception):
    """
    Exception raised when the location is not found
    """