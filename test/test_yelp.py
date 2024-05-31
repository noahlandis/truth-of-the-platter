from src.model.yelp import Yelp


def test_build_url():
    expected = "https://www.yelp.com/search?find_desc=Home Slice Pizza&find_loc=Austin"
    actual = Yelp.build_url("Home Slice Pizza", "Austin")
    assert actual == expected

