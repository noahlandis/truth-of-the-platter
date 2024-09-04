import pytest
from unittest.mock import patch, Mock
from requests import RequestException
from src.scrape import get_html
from src.yelp_api import get_yelp_data, NoResultsFoundError

@patch('src.yelp_api.collect_yelp_restaurants_regular_api')
def test_collect_yelp_restaurants_regular_api(collect_yelp_restaurants_regular_api):
    collect_yelp_restaurants_regular_api.return_value = []
    with pytest.raises(NoResultsFoundError):
        get_yelp_data("foo", "bar")

@patch('src.yelp_api.collect_yelp_restaurants_graph_ql')
def test_collect_yelp_restaurants_graph_ql(collect_yelp_restaurants_graph_ql):
    collect_yelp_restaurants_graph_ql.return_value = []
    with pytest.raises(NoResultsFoundError):
        get_yelp_data("foo", "bar")

@patch('requests.get')
def test_get_html_makes_request(mock_get: Mock):
    mock_response = Mock()
    mock_response.text = "foo bar"
    mock_get.return_value = mock_response
    get_html("https://www.google.com/")
    mock_get.assert_called_once_with("https://www.google.com/", headers={'User-Agent': "Mozilla/5.0"})

@patch('requests.get')
def test_get_html_valid_html(mock_get: Mock):
    mock_response = Mock()
    mock_response.text = "<html><head></head><body><h1>Test</h1></body></html>"
    mock_get.return_value = mock_response
    page = get_html("https://www.google.com/")
    assert page.find('h1').text == "Test"

def test_get_html_invalid_url():
    with pytest.raises(RequestException):
        get_html("https://url.invalid")


    

