
from bs4 import BeautifulSoup

from src.model.yelp import Yelp


def test_get_rating_and_review_count_cant_parse():
    expected = (None, None)
    html = "<div></div>"
    page = BeautifulSoup(html, 'html.parser')
    actual = Yelp.get_rating_and_review_count(page)
    assert actual == expected
