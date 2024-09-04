from bs4 import BeautifulSoup

from src.model.yelp import Yelp


def test_build_url():
    expected = "https://www.yelp.com/search?find_desc=Home Slice Pizza&find_loc=Austin"
    actual = Yelp.build_url("Home Slice Pizza", "Austin")
    assert actual == expected

def test_get_rating_and_review_count_yelp():
    expected = ("4.5", "1,000")
    html = '''
        <div class="arrange-unit__09f24__rqHTg arrange-unit-fill__09f24__CUubG y-css-lbeyaq">
            <span>4.5</span>
            <span>1,000 reviews</span>
        </div>
        '''
    page = BeautifulSoup(html, 'html.parser')
    actual = Yelp.get_rating_and_review_count(page)
    assert actual == expected