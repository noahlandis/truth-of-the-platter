from bs4 import BeautifulSoup
import requests
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import re
# to do
# 1. Refactor
# 2. Add tests
# 2. Create URL builder (interface/higher order functions?)
# 3. Implement Regex Matching feature
# 4. Create front end
YELP_ROOT = "https://www.yelp.com"


def read_input():
    name = input("Enter a restaraunt name: ")
    location = input("Enter the name of a city: ")
    scrape(name, location)

def get_html(name, location):
    url = url_builder_yelp(name, location)
    response = requests.get(url, headers={'User-Agent': "Mozilla/5.0"})
    print(response.status_code) # test to make sure this is 200
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def url_builder_yelp(name, location):
    return f"{YELP_ROOT}/search?find_desc={name}&find_loc={location}"

def scrape(name, location):
    soup = get_html(name, location)    
    
    # collect buisness name tags
    filtered_tags = get_filtered_tags(name, soup)
    pages, search_results = get_pages_and_search_results(filtered_tags)
    

    print(search_results)
    
def get_filtered_tags(name, soup):
    buisness_name_tags = soup.select('[class*="businessName"]', limit=10)
    filtered_tags = []
    # only collect tags that match name
    for tag in buisness_name_tags:
        buisness_name = tag.get_text(strip=True)
        # As sponsored results are irrelevant to the search, we ignore them. Only non-sponsored results are in the format "integer.<name>. 
        if re.match(r'^\d\.', buisness_name) and is_fuzzy_match(name, buisness_name):
            # remove integer and period as it isn't relevant
            buisness_name = buisness_name[2::]

            # we store the buisness name as well so we don't need another list
            filtered_tags.append((tag, buisness_name))
    return filtered_tags


def get_pages_and_search_results(filtered_tags):

    # get the individual page url's for the filtered tags
    pages = []

    # aggregate in form (buisness name, location)
    search_results = []
    
    # we collect address info here. We don't collect ratings, because it's only needed for the restaraunt the user selects
    for filtered_tag, buisness_name in filtered_tags:
        restaraunt_url = filtered_tag.find('a', href=True)['href']
        url = f"{YELP_ROOT}" + restaraunt_url
        individual_restaraunt_page = requests.get(url, headers={'User-Agent': "Mozilla/5.0"})
        page = BeautifulSoup(individual_restaraunt_page.text, 'html.parser')
        # we only need to get the rating for the one the user clicks, so we store every web page just in case
        pages.append(page)
        element = page.find(string="Get Directions")
        location = element.parent.parent.next_sibling.string
        search_results.append((buisness_name, location))
    return pages, search_results

def remove_non_alphanumeric_chars(a_string):
    return re.sub(r'\W+', '', a_string)

def is_fuzzy_match(user_input, search_result):
    user_input = remove_non_alphanumeric_chars(user_input)
    search_result = remove_non_alphanumeric_chars(search_result)
    match_ratio = fuzz.partial_token_set_ratio(user_input, search_result)
    return match_ratio > 70





    



   

def main():
    # string in first search box: luigis
    # string in second search box: fairfield

    read_input()

if __name__ == "__main__":
    main()