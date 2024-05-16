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



def read_input():
    name = input("Enter a restaraunt name: ")
    location = input("Enter the restaraunt's location: ")
    scrape(name, location)

def get_html(name, location):
    url = url_builder_yelp(name, location)
    response = requests.get(url, headers={'User-Agent': "Mozilla/5.0"})
    print(response.status_code) # test to make sure this is 200
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def url_builder_yelp(name, location):
    return f"https://www.yelp.com/search?find_desc={name}&find_loc={location}"

def scrape(name, location):
    soup = get_html(name, location)
    buisness_name_tags = soup.select('[class*="businessName"]', limit=10)

    # get the text from the buisness name tags
    potential_intended_restaurant_names = []
    for tag in buisness_name_tags:
        buisness_name = tag.get_text(strip=True)

        # As sponsored results are irrelevant to the search, we ignore them. Only non-sponsored results are in the format "integer.<name>. 
        if re.match(r'^\d\.', buisness_name):
            potential_intended_restaurant_names.append(buisness_name)

    # in case of multiple sponsored results, we only consider numbered results
    filtered_matches = get_fuzzy_matches(name, potential_intended_restaurant_names)
    print(filtered_matches)
    
    




def remove_non_alphanumeric_chars(a_string):
    return re.sub(r'\W+', '', a_string)

def get_fuzzy_matches(query, choices):
    query = remove_non_alphanumeric_chars(query)
    choices_copy = [remove_non_alphanumeric_chars(element) for element in choices]
    matches = process.extract(query, choices_copy, scorer=fuzz.partial_token_set_ratio) 
    # only extract matches with ratio above 75
    filtered_matches = []
    for i in range(len(matches)):
        # choices copy is what we used for filtering, we want to add the names of the original restaraunts when we match to the HTML parsing
        name = choices[i]
        ratio = matches[i][1]
        if ratio > 75:
            filtered_matches.append(name)

    return filtered_matches



    



   

def main():
    # string in first search box: luigis
    # string in second search box: fairfield

    url = "https://www.yelp.com/search?find_desc=luigis&find_loc=fairfield"
    scrape("homeslice", "austin")
main()