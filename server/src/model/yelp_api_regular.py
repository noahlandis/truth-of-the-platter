
import requests
from model.yelp_api import YelpApi    

class YelpApiRegular(YelpApi):
    def get_response(self) -> str:
        """
        Gets the response from the regular Yelp API
        :return str response - the response from the API
        """
        url = 'https://api.yelp.com/v3/businesses/search'
        
        # Make the request to the Yelp API
        response = requests.get(url, headers=self.headers, params=self.params)
        
        return response.json()
    
    def get_error(response) -> str:
        """
        Gets the error message from the regular Yelp API
        :return str error - the error message
        """
        return response['error']['code']