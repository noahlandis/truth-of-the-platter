


import website

ROOT = "https://www.google.com"

class Googl(website.Website):
    def build_url(self, name, city):
        return f"{ROOT}/search?q={name} {city}"

    def get_rating_and_review_count(self, page):
        div = page.find('div', class_='BNeawe tAd8D AP7Wnd')
        rating_tag = div.find('span', class_='oqSTJd')
        rating = rating_tag.get_text(strip=True)
        review_count = rating_tag.next_sibling.next_sibling.next_sibling.next_sibling.get_text(strip=True)
        return rating, review_count