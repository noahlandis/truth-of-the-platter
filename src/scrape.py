from bs4 import BeautifulSoup
import requests

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
    # name = "Luigi's Restaraunt"
    # location = "fairfield"    

    soup = get_html(name, location)
    potential_intended_restaurant_names = soup.findAll(string="Home Slice Pizza") # this should use regex to match against multiple possible spellings
    # if location was left blank, we can end show results here once we get the reviews
    restaraunts_matching_location_criteria = list()
    for restaraunt in potential_intended_restaurant_names:
        location_info = restaraunt.parent['href'] 
        print(location_info)
        if location in location_info: #this shouldnt be a direct contains, again it should use regex to account for user error and get things that are 'close enough': Fairfield ct, ct Fairfield, CT fairfield, ct-fairfield, etc
            restaraunts_matching_location_criteria.append(location_info)

    print(restaraunts_matching_location_criteria) # this can be renamed as results to display
    for restaraunt in restaraunts_matching_location_criteria:
        url = "https://www.yelp.com" + restaraunt
        individual_restaraunt = requests.get(url, headers={'User-Agent': "Mozilla/5.0"})



        # url = "https://www.yelp.com" + restaraunts_matching_location_criteria[0]
        # individual_restaraunt = requests.get(url, headers={'User-Agent': "Mozilla/5.0"})
        
        soup = BeautifulSoup(individual_restaraunt.text, 'html.parser')
        element = soup.find(string="Get Directions")
        location = element.parent.parent.next_sibling.string
        print("NAME " + name)
        print("LOCATION " + location)
        # rating = soup.find(href="#reviews")
        # print(rating.string)





   

def main():
    # string in first search box: luigis
    # string in second search box: fairfield

    url = "https://www.yelp.com/search?find_desc=luigis&find_loc=fairfield"
    read_input()
    # scrape(url)

if __name__ == "__main__":
    main()