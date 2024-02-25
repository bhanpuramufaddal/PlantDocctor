from geopy.geocoders import Nominatim

geocoder = Nominatim(user_agent = 'plant_doctor')

# Get the location of the place
def get_location(latitude, longitude):
    lat,long = float(12.9715987),float(77.5945667)
    location = geocoder.reverse((lat, long))
    return location

def generate_location_summary(lat, long):
    location = get_location(lat, long)
    return f"Location: {location.address}\n Altitude is {location.altitude}\n Latitude is {location.latitude}\n Longitude is {location.longitude}\n"

