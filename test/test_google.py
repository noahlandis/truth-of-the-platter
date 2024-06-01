from src.model.google import Google

def test_build_url():
    expected = "https://www.google.com/search?q=Home Slice Pizza Austin"
    actual = Google.build_url("Home Slice Pizza", "Austin")
    assert actual == expected

def test_build_url_with_ampersand():
    expected = "https://www.google.com/search?q=Jordan's Restaurant and Pizza Norwalk"
    actual = Google.build_url("Jordan's Restaurant & Pizza", "Norwalk")
    assert actual == expected