from unittest.mock import patch, Mock

import pytest
from requests import RequestException
from src.scrape import scrape, NoResultsFoundError, get_html


@patch('src.scrape.get_yelp_potential_matches')
def test_scrape_no_results(mock_get_yelp_potential_matches):
    mock_get_yelp_potential_matches.return_value = []
    with pytest.raises(NoResultsFoundError):
        scrape("foo", "bar")

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




    

