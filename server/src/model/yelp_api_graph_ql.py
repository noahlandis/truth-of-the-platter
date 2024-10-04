from model.yelp_api import YelpApi
import requests

class YelpApiGraphQL(YelpApi):
    @staticmethod
    def get_response(name: str, location: str) -> dict:
        url = 'https://api.yelp.com/v3/graphql'
        query = '''
        query SearchBusinesses($term: String!, $location: String!) {
            search(term: $term, location: $location, limit: 5) {
                business {
                    name
                    location {
                        address1
                        city
                        state
                        country
                    }
                    review_count
                    rating
                    photos
                }
            }
        }
        '''
        variables = {
            'term': name,
            'location': location
        }
        response = requests.post(url, headers=YelpApi.headers, json={'query': query, 'variables': variables}).json()
        error = YelpApiGraphQL._get_error_message(response)
        if error:
            return error  # This now returns the error code directly
        print(response)
        return response['data']['search']['business']
    
    @staticmethod
    def _get_error_message(response: dict) -> str:
        if 'errors' in response and response['errors']:
            return response['errors'][0]['extensions']['code']
        if 'error' in response and 'code' in response['error']:
            return response['error']['code']  # Add this line to handle the new error format
        return None
    
