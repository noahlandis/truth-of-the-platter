from abc import ABC, abstractmethod

class YelpApi(ABC):
    api_key = 'vh49slh9rlYEAYZ44isMebG-lOr3Sz7XKfIqrhME6BovN1Fs4lBWbD3PD5BgvNV1IyvAW8w2NTpqcXb2TTtgnzfl_4M2tqEJb_4JFBmRdoMVp0VuTVkA5KjpWDjXZnYx'
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

  

        


    