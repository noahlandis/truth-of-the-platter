import requests
from .search_api import SearchApi  # Update this line
import os

class GooglePlacesApi(SearchApi):
    api_key = os.getenv('GOOGLE_API_KEY')

    @staticmethod
    def get_response(name: str, location: str) -> dict:
        base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        query = f"{name} in {location}"
        
        # Add the type filter for restaurants
        type_filter = "restaurant"
        
        # Make the API request with the type filter
        response = requests.get(f"{base_url}?query={query}&type={type_filter}&key={GooglePlacesApi.api_key}")
        
        if response.status_code == 200:
            data = response.json()
            # Limit the results to the first 5 restaurants
            data['results'] = data['results'][:4]
            return data['results']
        else:
            error_message = GooglePlacesApi._get_error_message(response.json())
            raise Exception(f"Google Places API request failed: {error_message}")

    @staticmethod
    def _get_error_message(response: dict) -> str:
        if 'error_message' in response:
            return response['error_message']
        return "Unknown error occurred"
    
    def get_formatted_restaurant_data(self, restaurant: dict) -> dict:
        photo_reference = restaurant.get('photos', [{}])[0].get('photo_reference', '')
        photo_url = ''
        if photo_reference:
            photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={self.api_key}"

        return {
            'name': restaurant['name'],
            'location': f"{restaurant['formatted_address']}",
            'review_count': f"{restaurant['user_ratings_total']:,}",
            'rating': restaurant['rating'],
            'imageUrl': photo_url,
            'source': 'Google'
        }

