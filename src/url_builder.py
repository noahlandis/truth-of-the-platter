# other option is to use interface that builds URL and scrapes for a specific site: Yelp interface includes build_url and scrape, Google interface includes build_url and scrape, etc
def build_urls(name, location):
    url_factory = [build_yelp_url, build_google_url]
    urls = []
    for factory in url_factory:
        urls.append(factory(name, location))
    return urls

def build_yelp_url(name, location):
    return f"https://www.yelp.com/search?find_desc={name}&find_loc={location}"

def build_google_url(name, location):
    return f"https://www.google.com/search?q={name} {location}"

def main():
    name = "homeslice"
    location = "austin"
    print(build_urls(name, location))


main()