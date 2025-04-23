import requests
import json
import math
import numpy as np
import csv
from cityFinder import load_city_coords

lat1 = 51.4416 #Eindhoven
lon1 = 5.4697
lat2 = 52.3676 #Amsterdam
lon2 = 4.9041


filepath = r"C:\Users\franc\OneDrive\Bureaublad\Newer Beginnings\Amsterdam Cycling baby\worldcities.csv"

city_coords = load_city_coords(filepath)

user_input = input("Enter a city: ").strip().lower()

if user_input in city_coords:
    lat, lon = city_coords[user_input]
else:
    print("City not found.")
    exit()



user_input = input("Enter a city: ").strip().lower()
coords = load_city_coords(user_input)

if coords:
    lat, lon = coords
    # ✅ Plug lat/lon into your weather API call
    url = "https://api.tomorrow.io/v4/weather/realtime?location=",coords,"&apikey=h75GN8Qsauua0KkdNNq2QJtvpOYFyTEn"
    # Continue with your weather + cycling logic
else:
    print("City not found.")


def callAPI(url):
    headers = {
        "accept": "application/json",
        "accept-encoding": "deflate, gzip, br"
    }

    response = requests.get(url, headers=headers)

    # Check for a successful response
    if response.status_code == 200:
        data = response.json()
        values = data["data"]["values"]
        print(values)  # Or return values if you're using this elsewhere
        return values
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None
    
def findBearing(lat1, lon1, lat2, lon2):

    # Convert from degrees to radians
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_lambda = math.radians(lon2 - lon1)

    x = math.sin(delta_lambda) * math.cos(phi2)
    y = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(delta_lambda)

    theta = math.atan2(x, y)

    # Convert from radians to degrees and normalize
    bearing = (math.degrees(theta) + 360) % 360
    return bearing

bearingAngle = round(findBearing(lat1, lon1, lat2, lon2),2)
print('bearing Angle', bearingAngle)

def angle_to_vector(deg):

    rad = math.radians(deg)
    return [math.cos(rad), math.sin(rad)]

def dotProduct(x,y):
    dot = np.dot(x,y)
    return dot


def windDirectionCheck(bearingAngle, WindDirection):
    bearingAngleVector = angle_to_vector(bearingAngle)
    WindDirectionVector = angle_to_vector(WindDirection)

    alignment = dotProduct(bearingAngleVector,WindDirectionVector)

    if alignment > -0.1:
        check = True
    else:
        check = False
    return check







try:
    values = callAPI()
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")

if values['windDirection'] >=180:
    WindDirection = values['windDirection']-180
else:
    WindDirection = values['windDirection']+180

check = windDirectionCheck(bearingAngle,WindDirection)
print('check', check)


# Format it cleanly
print("📍 Weather Snapshot:")
print(f"🌡️ Temp: {values['temperature']}°C (feels like {values['temperatureApparent']}°C)")
print(f"💧 Humidity: {values['humidity']}%")
print(f"💨 Wind: {values['windSpeed']} m/s, Gusts: {values['windGust']} m/s, Direction: {values['windDirection']}°")
print(f"🌧️ Rain Intensity: {values['rainIntensity']} mm/h | Cloud Cover: {values['cloudCover']}%")
print(f"🔍 Visibility: {values['visibility']} km")
print(f"☁️ Cloud Base: {values['cloudBase']} km | Cloud Ceiling: {values['cloudCeiling']} km")
print(f"🧪 Pressure: {values['pressureSeaLevel']} hPa (sea level)")


conditionsOK =     (values['cloudBase'] is None or values['cloudBase'] > 1) and (values['cloudCeiling'] is None or values['cloudCeiling'] > 0.5) and  (values['rainIntensity'] is None or values['rainIntensity'] < 0.1) and (values['sleetIntensity'] is None or values['sleetIntensity'] < 0.1) and  (values['snowIntensity'] is None or values['snowIntensity'] < 0.1) and (values['temperature'] is None or values['temperature'] > 2) and (values['visibility'] is None or values['visibility'] > 2) and (values['windSpeed'] is None or values['windSpeed'] < 40)

# Add logic to say whether it's good for cycling:
if  conditionsOK:
    if check == False and values['windSpeed']<10:
        print('\n Today is a great day to cycle')
    elif check == True:
        print("\nToday is a great day to cycle")
    else:
        print("\nits jover dont go out")

else:
    print("\nits jover dont go out")


