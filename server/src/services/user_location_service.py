import geocoder
from exceptions import UserLocationNotFoundError

def get_user_location():
    try:
        g = geocoder.ip('me')
        location = f"{g.city}, {g.state}"
        return location
    except Exception as e:
        raise UserLocationNotFoundError("An error occurred while trying to get your location. Please enter it manually.")
