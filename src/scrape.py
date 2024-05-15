from bs4 import BeautifulSoup
import requests

def scrape(url):
    response = requests.get(url, headers={'User-Agent': "Mozilla/5.0"})
    print(response.status_code) # test to make sure this is 200
    soup = BeautifulSoup(response.text, 'html.parser')
    h3_tags = soup.find_all('h3')    

def main():
    # string in first search box: luigis
    # string in second search box: fairfield


    url = "https://www.yelp.com/search?find_desc=luigis&find_loc=fairfield"
    scrape(url)

main()