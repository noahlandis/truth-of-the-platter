from abc import ABC, abstractmethod

class Website(ABC):
    
    @abstractmethod
    def build_url(self, name, city):
        pass

    @abstractmethod
    def get_rating_and_review_count(self, page):
        pass
    


