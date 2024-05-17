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

def test_remove_non_alphanumeric_chars():
    # setup
    a_string = "\tHomeslice's Pizza, Restaraunt"
    expected = "HomeslicesPizzaRestaraunt"
    # invoke
    actual = src.scrape.remove_non_alphanumeric_chars(a_string)
    # analyze
    assert expected == actual

def test_is_fuzzy_match_true_different_capitalization():
    # setup
    user_input = "home slice pizza"
    search_result = "Home Slice Pizza"
    # invoke
    actual = src.scrape.is_fuzzy_match(user_input, search_result)
    # analyze 
    assert actual == True

def test_is_fuzzy_match_true_different_spacing():
    # setup
    user_input = "HomeSlicePizza"
    search_result = "Home Slice Pizza"
    # invoke
    actual = src.scrape.is_fuzzy_match(user_input, search_result)
    # analyze
    assert actual == True

def test_is_fuzzy_match_true_shortened_name():
    # setup
    user_input = "Home Slice"
    search_result = "Home Slice Pizza"
    # invoke
    actual = src.scrape.is_fuzzy_match(user_input, search_result)
    # analyze
    assert actual == True


def test_is_fuzzy_match_true_different_word():
    # setup
    user_input = "Home Slice Restaraunt"
    search_result = "Home Slice Pizza"
    # invoke
    actual = src.scrape.is_fuzzy_match(user_input, search_result)
    # analyze
    assert actual == True

def test_is_fuzzy_match_true_different_punctuation():
    # setup
    user_input = "Home Slice's Pizza"
    search_result = "Home Slice Pizza"
    # invoke
    actual = src.scrape.is_fuzzy_match(user_input, search_result)
    # analyze
    assert actual == True


def test_is_fuzzy_match_false():
    # setup
    user_input = "Luigi's Pizza from Home"
    search_result = "Home Slice Pizza"
    # invoke
    actual = src.scrape.is_fuzzy_match(user_input, search_result)
    # analyze
    assert actual == False


    
