from abc import ABC, abstractmethod
from model.yelp_api_graph_ql import YelpApiGraphQL
from model.yelp_api_regular import YelpApiRegular
from model.google_places_api import GooglePlacesApi

class ApiHandler(ABC):
    def __init__(self, next_handler=None):
        self._next_handler = next_handler
        self._processed_handler = None

    def handle(self, name, location):
        try:
            result = self.process_request(name, location)
            self._processed_handler = self
            return result
        except Exception as e:
            if self._next_handler:
                return self._next_handler.handle(name, location)
            else:
                raise e

    def get_processed_handler(self):
        if self._processed_handler:
            return self._processed_handler
        elif self._next_handler:
            return self._next_handler.get_processed_handler()
        else:
            return None

    @abstractmethod
    def process_request(self, name, location):
        pass

class YelpApiGraphQLHandler(ApiHandler):
    def process_request(self, name, location):
        print("Yelp API GraphQL handler hit")
        response = YelpApiGraphQL.get_response(name, location)
        if response == 'DAILY_POINTS_LIMIT_REACHED':
            print("GraphQL API limit reached, passing to next handler")
            raise Exception("GraphQL API limit reached")
        if response == 'TRIAL_EXPIRED':
            print("GraphQL API trial expired, passing to next handler")
            raise Exception("GraphQL API trial expired")
        if response == 'TOKEN_INVALID':
            print("GraphQL API token invalid, passing to next handler")
            raise Exception("GraphQL API token invalid")
        if response == 'VALIDATION_ERROR':
            print("GraphQL API validation error, passing to next handler")
            raise Exception("GraphQL API validation error")
        return response
    
    def get_formatted_restaurant_data(self, restaurant):
        return YelpApiGraphQL().get_formatted_restaurant_data(restaurant)

class YelpApiRegularHandler(ApiHandler):
    def process_request(self, name, location):
        print("Yelp API Regular handler hit")
        response = YelpApiRegular.get_response(name, location)
        if response == 'DAILY_POINTS_LIMIT_REACHED':
            print("Regular API limit reached, passing to next handler")
            raise Exception("Regular API limit reached")
        if response == 'TRIAL_EXPIRED':
            print("Regular API trial expired, passing to next handler")
            raise Exception("Regular API trial expired")
        if response == 'TOKEN_INVALID':
            print("Regular API token invalid, passing to next handler")
            raise Exception("Regular API token invalid")
        if response == 'VALIDATION_ERROR':
            print("Regular API validation error, passing to next handler")
            raise Exception("Regular API validation error")
        return response

    def get_formatted_restaurant_data(self, restaurant):
        return YelpApiRegular().get_formatted_restaurant_data(restaurant)

class GooglePlacesApiHandler(ApiHandler):
    def process_request(self, name, location):
        print("Google Places API handler hit")
        response = GooglePlacesApi.get_response(name, location)
        return response

    def get_formatted_restaurant_data(self, restaurant):
        return GooglePlacesApi().get_formatted_restaurant_data(restaurant)

