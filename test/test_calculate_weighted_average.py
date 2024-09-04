import pytest

from src.calculate_weighted_average import \
    get_weighted_average_and_total_review_count


@pytest.mark.parametrize("site_ratings, expected", [
    ([("Yelp", "1.0", "1"), ("Google", "5.0", "1")], (3.0, "2")), # weighted average and count is calculated correctly
    ([("Yelp", "1.0", "1"), ("Google", "5.0", "2")], (3.67, "3")), # weighted average is correctly rounded
    ([("Yelp", "1.0", "1,000")], (1.0, "1,000")), # commas are formatted correctly
    ([("Yelp", "1.0", "1"), ("Google", None, None)], (1.0, "1")) # ratings that couldn't be found aren't factored into calculation
])
def test_get_weighted_average_and_total_review_count(site_ratings, expected):
    actual = get_weighted_average_and_total_review_count(site_ratings)
    assert actual == expected
    
    

