import logging
import os

import requests

from server.src.model.api_handler import YelpApiGraphQLHandler, YelpApiRegularHandler
from exceptions import NoResultsFoundError
from utils.string_utils import is_potential_match
from server.src.model.yelp_api import YelpApi
from server.src.model.yelp_api_graph_ql import YelpApiGraphQL
from server.src.model.yelp_api_regular import YelpApiRegular

logger = logging.getLogger()

def get_yelp_matches(name, location):
    chain = YelpApiGraphQLHandler(      # GraphQLHandler is the first handler
        YelpApiRegularHandler(          # RegularHandler is the next in the chain
        )
    )

    # 
    response = chain.handle(name, location)
    print(response)
    
    