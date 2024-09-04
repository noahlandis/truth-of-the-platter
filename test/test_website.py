
from bs4 import BeautifulSoup

from src.model.google import Google


def test_get_rating_and_review_count_cant_parse():
    expected = (None, None)
    html = "<div></div>"
    page = BeautifulSoup(html, 'html.parser')
    actual = Google.get_rating_and_review_count(page)
    assert actual == expected
