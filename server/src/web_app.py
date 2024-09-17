import os
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request, session, jsonify

from exceptions import NoResultsFoundError, UnknownLocationError
from services.yelp_service import get_yelp_matches
from server.src.services.scrape_service import scrape
from server.src.services.calculate_weighted_average_service import get_weighted_average_and_total_review_count
from server.src.services.user_location_service import get_user_location
from flask_cors import CORS
import requests



app = Flask(
    __name__,
    static_folder='../../client/react-frontend/dist/assets',  # React static assets like JS and CSS
    template_folder='../../client/react-frontend/dist'  # Path to index.html
)
CORS(app)  # This will allow all origins



@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return render_template("index.html")


@app.route('/api/search', methods=['GET'])
def search():
    name = request.args.get('name')
    location = request.args.get('location')
    try:
        matches = get_yelp_matches(name, location)
        return jsonify(matches), 200
    except UnknownLocationError as e:
        return jsonify({
            "error": str(e),
            "error_code": "UNKNOWN_LOCATION"
        }), 404
    except NoResultsFoundError as e:
        return jsonify({
            "error": str(e),
            "error_code": "NO_RESULTS"
        }), 404
    


    # Dynamically add the matches as radio butto

@app.route('/api/select', methods=['POST'])
def select_match():
    print("CALLED AGAIN")
    print(request.json)
    intended_restaurant = request.json
    site_ratings = []
    site_ratings.append(("Yelp", str(intended_restaurant['rating']), str(intended_restaurant['review_count'])))
    full_name = intended_restaurant['name']
    full_location = intended_restaurant['location']
    site_ratings.extend(scrape(full_name, full_location))
    star_average, total_review_count = get_weighted_average_and_total_review_count(site_ratings)
    return jsonify({
        'site_ratings': site_ratings,
        'star_average': star_average,
        'total_review_count': total_review_count
    })


@app.route('/api/autocomplete', methods=['GET'])
def google_places_autocomplete():
    url = "https://maps.googleapis.com/maps/api/place/autocomplete/json"

    

    # Get the search query from the request
    input_text = request.args.get('text')  # This is the user's input
    
    # Set up parameters for the request, including filtering for cities and US locations
    params = {
        'input': input_text,
        'types': 'geocode',  # Filter results to only cities
        'components': 'country:us',  # Limit results to the US
        'key': os.getenv('GOOGLE_API_KEY')
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        return jsonify(response.json())  # Return the Google Places API response
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/user-location', methods=['GET']) 
def get_location():
    return jsonify(get_user_location())


    
     