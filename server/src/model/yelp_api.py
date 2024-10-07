from .search_api import SearchApi  # Update this line
import os

class YelpApi(SearchApi):
    api_key = os.getenv('YELP_API_KEY')

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    @staticmethod
    def get_response(name: str, location: str) -> dict:
        # Implement Yelp-specific get_response method
        pass

    def _get_error_message(response: dict) -> str:
        # Implement Yelp-specific error message extraction
        pass
    
    def get_formatted_restaurant_data(self, restaurant: dict) -> dict:
        return {
            'name': restaurant['name'],
            'location': f"{restaurant['location']['address1']} {restaurant['location']['city']}, {restaurant['location']['state']}",
            'review_count': restaurant['review_count'],
            'rating': restaurant['rating'],
            'imageUrl': restaurant['image_url'] if 'image_url' in restaurant else restaurant['photos'][0] if 'photos' in restaurant else None,
            'source': 'Yelp'
        }


