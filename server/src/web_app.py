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
    # Retrieve match_id from form
    match_id = int(request.form.get('match_id'))

    # Retrieve the matches from the session
    matches = session.get('matches', [])

    # Find the selected match by its index (match_id)
    selected_match = matches[match_id]

    # Display the selected match details
    selected_match_info = f'''
    <h1>Selected Restaurant Details</h1>
    <p><strong>Name:</strong> {selected_match['name']}</p>
    <p><strong>Address:</strong> {selected_match['location']}</p>
    '''

    # Scrape results for the selected match
    name = selected_match['name']
    location = selected_match['location']
    results, name, address = scrape(selected_match)
    star_average, total_review_count = get_weighted_average_and_total_review_count(results)

    # Display site ratings
    site_ratings_html = ""
    for website_name, star_rating, review_count in results:
        if star_rating is None:
            display_message = f"<p>{website_name} - Ratings could not be found for this site, it will not be considered for the aggregate rating.</p>"
        else:
            display_message = f"<p>{website_name} - {star_rating} stars, {review_count} reviews.</p>"
        site_ratings_html += display_message

    # Display final weighted average and total review count
    final_result = f'''
    <h2>A more accurate rating of {name} is {star_average} stars based on {total_review_count} reviews.</h2>
    '''

    # Combine all the HTML to display
    html_output = f'''
    {selected_match_info}
    <h2>Ratings from Various Websites:</h2>
    {site_ratings_html}
    {final_result}
    '''

    return html_output