import requests
from bs4 import BeautifulSoup
from model.yelp import Yelp
from model.google import Google
from model.website import Website
from input import get_user_selection
from string_utils import is_potential_match, extract_review_count


YELP_ROOT = "https://www.yelp.com"



def scrape(name, city):
    # list of websites to scrape
    websites = [Yelp(), Google()]
    results = []
    for i in range(len(websites)):

        # search results page
        url = websites[i].build_url(name, city)
        page = get_html(url)

        # We first the matching Yelp results and ask user to select which address they intended
        if i == 0:

            # collect pages for each yelp restaraunt that is a good candidate base, as well as their city
            yelp_pages, search_results = get_pages_and_search_results(name, page)
            selected_index = get_user_selection(search_results)

            # we determined the intended restaraunt, so we can get the matching page
            page = yelp_pages[selected_index]
            name = search_results[selected_index][0]
            city = search_results[selected_index][1]

        # After we got the yelp results, we can get the ratings and review count for the intended result
        website_name = websites[i].__class__.__name__
        rating = websites[i].get_rating_and_review_count(page)[0]
        review_count = extract_review_count(websites[i].get_rating_and_review_count(page)[1])
        results.append((website_name, rating, review_count))
    return results



def get_html(url):
    """
    Gets the HTML for a paticular url
    :param - The URL to get the HTML for
    
    returns - the HTML for the given URL
    """
    response = requests.get(url, headers={'User-Agent': "Mozilla/5.0"})
    print(response.status_code) # test to make sure this is 200
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

        

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
            page = get_html(url)

            # we only need to get the rating for the one the user clicks, so we store every web page just in case
            pages.append(page)
            element = page.find(string="Get Directions")
            address = element.parent.parent.next_sibling.string
            search_results.append((buisness_name, address))
    return pages, search_results


