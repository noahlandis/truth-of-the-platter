# import all the necessary libraries
import requests
from bs4 import BeautifulSoup


# import the websites so that they are resolved


from model.yelp import Yelp
from model.googl import Googl
from model.website import Website
from input import get_user_selection, read_input
from string_utils import is_potential_match, extract_review_count




# Modules
# Scrape: main scrape function and get_soup, get_html, get_pages_and_search_results
# String utils: remove_non_alphanumeric_chars, is_fuzzy_match, extract_review_count
# Command Line: read_input, get_user_selection

"""
Concatanate name and city to search google : home slice pizza 502 austin
Search google, identify matching place
Get review and rating score
"""

YELP_ROOT = "https://www.yelp.com"


# setup: reads input, gets list of sites
# get yelp city and names



def get_html(website: Website, name: str, city: str):
    """
    Builds the URL and returns displayed HTML 
    :param website - class representing a paticular website (Yelp, Google, etc.)
    :param name - name of restaraunt to view reviews for
    :param city - the city where the restaraunt is located
    """
    url = website.build_url(name, city)
    return get_soup(url)

def get_soup(url):
    """
    Gets the HTML for a paticular url
    :param - The URL to get the HTML for
    
    returns - the HTML for the given URL
    """
    response = requests.get(url, headers={'User-Agent': "Mozilla/5.0"})
    print(response.status_code) # test to make sure this is 200
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def scrape(name, city):
    # list of websites to scrape
    websites = [Yelp(), Googl()]
    results = []
    for i in range(len(websites)):

        # search results page
        page = get_html(websites[i], name, city)

        # We first the matching Yelp results and ask user to select which address they intended
        if i == 0:

            # collect pages for each yelp buisness, as well as their city
            yelp_pages, search_results = get_pages_and_search_results(name, page)
            i = get_user_selection(search_results)

            # we determined the intended restaraunt, so we can get the matching page
            page = yelp_pages[i]
            name = search_results[i][0]
            city = search_results[i][1]

        # After we got the yelp results, we can get the ratings and review count for the intended result
        website_name = websites[i].__class__.__name__
        rating = websites[i].get_rating_and_review_count(page)[0]
        review_count = extract_review_count(websites[i].get_rating_and_review_count(page)[1])
        results.append((website_name, rating, review_count))
    return results
        

def get_pages_and_search_results(name, soup):
    """
    Searches Yelp to get the HTML tags and names of buisnesses which are good candidates for the user's intended restaraunt
    """
    buisness_name_tags = soup.select('[class*="businessName"]', limit=10)
    pages = []

    # aggregate in form (buisness name, city)
    search_results = []
    
    # only collect tags that match name
    for tag in buisness_name_tags:
        buisness_name = tag.get_text(strip=True)
        # As sponsored results are irrelevant to the search, we ignore them. Only non-sponsored results are in the format "integer.<name>. 
        if is_potential_match(name, buisness_name):
            # remove integer and period as it isn't relevant
            buisness_name = buisness_name[2::]

            # we store the buisness name as well so we don't need another list
            restaraunt_url = tag.find('a', href=True)['href']
            url = f"{YELP_ROOT}" + restaraunt_url
            page = get_soup(url)

            # we only need to get the rating for the one the user clicks, so we store every web page just in case
            pages.append(page)
            element = page.find(string="Get Directions")
            address = element.parent.parent.next_sibling.string
            search_results.append((buisness_name, address))
    return pages, search_results


def main():
    name, city = read_input()
    ratings_and_reviews = scrape(name, city)
    print(ratings_and_reviews)

if __name__ == "__main__":
    main()