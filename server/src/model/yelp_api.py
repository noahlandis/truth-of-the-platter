from abc import ABC, abstractmethod

class YelpApi(ABC):
    """
    Abstract class representing a generic Yelp Api type (regular or GraphQL)
    """
    api_key = 'vh49slh9rlYEAYZ44isMebG-lOr3Sz7XKfIqrhME6BovN1Fs4lBWbD3PD5BgvNV1IyvAW8w2NTpqcXb2TTtgnzfl_4M2tqEJb_4JFBmRdoMVp0VuTVkA5KjpWDjXZnYx'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    def __init__(self, name: str, location: str):
        self.name = name
        self.location = location
        self.params = {
            'term': self.name,
            'location': self.location,
            'limit': 5
        }

    @abstractmethod
    def get_response(self) -> str:
        """
        Abstract method to get response from Yelp API
        :return str response - the response from the API
        """
        pass


    @staticmethod
    @abstractmethod
    def get_error(response: str) -> str:
        """
        Abstract method to get error message
        :return str error - the error message
        """
        pass




        


    