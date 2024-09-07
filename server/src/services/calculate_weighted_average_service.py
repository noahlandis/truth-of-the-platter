"""
This module contains the logic to calculate the weighted average of the ratings and the total number of reviews
Author: Noah Landis
"""

def get_weighted_average_and_total_review_count(site_ratings: list):
    """
    Calculates the weighted average of the ratings and the total number of reviews
    :param list site_ratings - a list of tuples, where each tuple is in the form (<website name>, <rating>, <number of reviews>)
    :return tuple  - (<weighted average of the star ratings *rounded to 2 decimal places*>, <total number of reviews across all scraped sites>)
    """
    total_stars = 0
    total_review_count = 0
    for _, star_rating, review_count in site_ratings:
        # if we were unable to find the rating for the site, we don't consider the site when calculating the weighted average
        if star_rating is not None:

            # remove the commas so review_count can be converted into an integer
            review_count = int(review_count.replace(',', ''))  
            total_stars += float(star_rating) * review_count
            total_review_count += review_count
    
    weighted_average = total_stars / total_review_count
    
    # add commas to the total review count to be consistent with the review counts for individual sites
    total_review_count = "{:,}".format(total_review_count)
    return round(weighted_average, 2), total_review_count