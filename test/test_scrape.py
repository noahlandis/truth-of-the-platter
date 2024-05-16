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

def test_remove_whitespace():
    # setup
    a_string = "\tHomeslice's Pizza, Restaraunt"
    expected = "HomeslicesPizzaRestaraunt"
    # invoke
    actual = src.scrape.remove_non_alphanumeric_chars(a_string)
    # analyze
    assert expected == actual

def test_fuzzy_matching_all_strings_match():
    # setup
    query = "homeslice pizza"
    choices = ["Homeslice Pizza", "homeslice's Pizzeria", "homeslice", "Pizza Homeslice"]
    # invoke
    actual = src.scrape.get_fuzzy_matches(query, choices)
    # analyze
    assert choices == actual
    
def test_fuzzy_matching_no_strings_match():
    # setup
    query = "homeslice pizza"
    choices = ["Andrew's home kitchen", "Pizza palace", "Subway", "luigis Pizzeria"]
    expected = []
    # invoke
    actual = src.scrape.get_fuzzy_matches(query, choices)
    # analyze
    assert expected == actual


    
