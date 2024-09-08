
import requests
from model.yelp_api import YelpApi


class YelpApiGraphQL(YelpApi):


    def get_response(self) -> str:
        """
        Gets the response from the regular Yelp API
        :return str response - the response from the API
        """
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
                }
            }
        }
        '''

        
        # Make the request to the Yelp API
        response = requests.post(url, headers=self.headers, json={'query': query, 'variables': self.params})

        
        return response.json()
    
    def get_error(response) -> str:
        return response['errors'][0]['extensions']['code']