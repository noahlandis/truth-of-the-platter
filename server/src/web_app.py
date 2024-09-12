from flask import Flask, request, session, jsonify

from exceptions import NoResultsFoundError, UnknownLocationError
from services.yelp_service import get_yelp_matches
from server.src.services.scrape_service import scrape
from server.src.services.calculate_weighted_average_service import get_weighted_average_and_total_review_count
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will allow all origins



@app.route('/')
def home():
    return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Search Form</title>
        </head>
        <body>
            <h1>Search</h1>
            <form action="/search" method="GET">
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" required><br><br>

                <label for="location">Location:</label>
                <input type="text" id="location" name="location" required><br><br>

                <button type="submit">Search</button>
            </form>
        </body>
        </html>
    '''

@app.route('/search', methods=['GET'])
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

@app.route('/select', methods=['POST'])
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



    
     