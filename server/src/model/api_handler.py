import requests
from abc import ABC, abstractmethod
from model.yelp_api_graph_ql import YelpApiGraphQL
from model.yelp_api_regular import YelpApiRegular

class ApiHandler(ABC):
    def __init__(self, next_handler=None):
        self._next_handler = next_handler

    @abstractmethod
    def handle(self, name, location):
        pass

class YelpApiGraphQLHandler(ApiHandler):
    def handle(self, name, location):
        response = YelpApiGraphQL.get_response(name, location)
        if response == 'DAILY_POINTS_LIMIT_REACHED':
            print("GraphQL API limit reached, passing to next handler")
            if self._next_handler:
                return self._next_handler.handle(name, location)
            
        if response == 'TRIAL_EXPIRED':
            print("GraphQL API trial expired, passing to next handler")
            if self._next_handler:
                return self._next_handler.handle(name, location)
        return response

class YelpApiRegularHandler(ApiHandler):
    def handle(self, name, location):
        response = YelpApiRegular.get_response(name, location)
        if response == 'DAILY_POINTS_LIMIT_REACHED':
            print("Regular API limit reached, passing to next handler")
            if self._next_handler:
                return self._next_handler.handle(name, location)
        if response == 'TRIAL_EXPIRED':
            print("Regular API trial expired, passing to next handler")
            if self._next_handler:
                return self._next_handler.handle(name, location)
        return response

class GooglePlacesApiHandler(ApiHandler):
    def handle(self, name, location):
        print("Google Places API handler hit")
        
        # Construct the API request URL
        base_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        api_key = "API KEY"  # Replace with your actual API key
        query = f"{name} in {location}"
        
        # Make the API request
        response = requests.get(f"{base_url}?query={query}&key={api_key}")
        
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK' and data['results']:
                print("Search Results:")
                for result in data['results']:
                    print(f"Name: {result['name']}")
                    print(f"Address: {result['formatted_address']}")
                    print(f"Rating: {result.get('rating', 'N/A')}")
                    print(f"Review Count: {result.get('user_ratings_total', 'N/A')}")
                    print("---")
                return data['results']
            else:
                print(f"No results found or error: {data['status']}")
        else:
            print(f"API request failed with status code: {response.status_code}")
        
        return None