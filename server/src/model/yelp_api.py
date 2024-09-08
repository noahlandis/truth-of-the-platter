from abc import ABC, abstractmethod
import os

class YelpApi(ABC):
    api_key = os.getenv('YELP_API_KEY')

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    @staticmethod
    @abstractmethod
    def get_response(name: str, location: str) -> dict:
        pass

    @abstractmethod
    def _get_error_message(response: dict) -> str:
        pass

  

        


    