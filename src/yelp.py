import website

ROOT = "https://www.yelp.com"

class Yelp(website.Website):
    def build_url(self, name, city):
        return f"{ROOT}/search?find_desc={name}&find_loc={city}"

    def get_rating_and_review_count(self, page):
        div = page.find('div', class_='arrange-unit__09f24__rqHTg arrange-unit-fill__09f24__CUubG y-css-lbeyaq')
        span_tags = div.find_all('span')
        rating = span_tags[0].get_text(strip=True)
        review_count = span_tags[1].get_text(strip=True)
        return rating, review_count
    