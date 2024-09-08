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
        return response

class YelpApiRegularHandler(ApiHandler):
    def handle(self, name, location):
        response = YelpApiRegular.get_response(name, location)
        return response