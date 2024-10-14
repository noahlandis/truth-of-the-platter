from model.yelp_api import YelpApi
import requests

class YelpApiRegular(YelpApi):
    @staticmethod
    def get_response(name: str, location: str) -> dict:
        url = 'https://api.yelp.com/v3/businesses/search'
        params = {
            'term': name,
            'location': location,
            'limit': 4
        }
        response = requests.get(url, headers=YelpApi.headers, params=params).json()
        error = YelpApiRegular._get_error_message(response)
        if error:
            return error
        return response['businesses']
    
    def _get_error_message(response: dict) -> str:
        if 'error' in response and 'code' in response['error']:
            return response['error']['code']
        return None
    
   