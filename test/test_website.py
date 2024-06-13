
from unittest.mock import Mock
from bs4 import BeautifulSoup
from src.model.yelp import Yelp
from src.model.google import Google
from src.model.tripadvisor import TripAdvisor

def test_get_rating_and_review_count_cant_parse():
    expected = (None, None)
    html = "<div></div>"
    page = BeautifulSoup(html, 'html.parser')
    actual = Yelp.get_rating_and_review_count(page)
    assert actual == expected
