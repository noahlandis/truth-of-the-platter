import src.scrape

def test_url_builder_yelp():
    # setup
    name = "homeslice"
    city = "austin"
    # invoke
    expected = f"https://www.yelp.com/search?find_desc={name}&find_loc={city}"
    actual = src.scrape.url_builder_yelp(name, city)
    # analyze
    assert expected == actual
