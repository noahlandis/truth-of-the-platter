from src.calculate_weighted_average import get_weighted_average

def test_get_weighted_average():
    expected = (3.0, "2")
    actual = get_weighted_average([("Home Slice Pizza", "1.0", "1"), 
                                   ("More Home Slice", "5.0", "1")])
    assert actual == expected

def test_get_weighted_average_rounding():
    expected = (3.67, "3")
    actual = get_weighted_average([("Home Slice Pizza", "1.0", "1"), 
                                   ("More Home Slice", "5.0", "2")])
    assert actual == expected


def test_get_weighted_average_format_commas():
    expected = (1.0, "1,000")
    actual = get_weighted_average([("Home Slice Pizza", "1.0", "1,000")])
    assert actual == expected


