from src.model.tripadvisor import TripAdvisor

def test_build_url():
    expected = "https://www.google.com/search?q=Home Slice Pizza Austin"
    actual = TripAdvisor.build_url("Home Slice Pizza", "Austin")
    assert actual == expected