from bs4 import BeautifulSoup
from src.model.google import Google

def test_build_url():
    expected = "https://www.google.com/search?q=Home Slice Pizza Austin"
    actual = Google.build_url("Home Slice Pizza", "Austin")
    assert actual == expected

def test_build_url_with_ampersand():
    expected = "https://www.google.com/search?q=Jordan's Restaurant and Pizza Norwalk"
    actual = Google.build_url("Jordan's Restaurant & Pizza", "Norwalk")
    assert actual == expected

def test_get_rating_and_review_count_google():
    expected = ("4.5", "1,000")
    html = '''
        <div class="BNeawe tAd8D AP7Wnd">
            <span class="oqSTJd">4.5</span>
            <span> • </span>
            <span>1,000 reviews</span>
        </div>
        '''
    page = BeautifulSoup(html, 'html.parser')
    actual = Google.get_rating_and_review_count(page)
    assert actual == expected