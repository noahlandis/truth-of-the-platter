from abc import ABC, abstractmethod

class SearchApi(ABC):

    @staticmethod
    @abstractmethod
    def get_response(name: str, location: str) -> dict:
        pass


    @abstractmethod
    def get_formatted_restaurant_data(self, restaurant: dict) -> dict:
        pass

    @abstractmethod
    def _get_error_message(response: dict) -> str:
        pass

