import requests
import math
import numpy as np
import csv
from cityFinder import load_city_coords

filepath = "worldcities.csv"
city_coords = load_city_coords(filepath)

def findUserCoords(user_input):
    if user_input in city_coords:
        lat, lon = city_coords[user_input]
        url = f"https://api.tomorrow.io/v4/weather/realtime?location={lat},{lon}&apikey=h75GN8Qsauua0KkdNNq2QJtvpOYFyTEn"
        return lat, lon, url
    else:
        print("City not found.")
        exit()

def callAPI(url):
    headers = {
        "accept": "application/json",
        "accept-encoding": "deflate, gzip, br"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        values = data["data"]["values"]
        return values
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def findBearing(lat1, lon1, lat2, lon2):
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_lambda = math.radians(lon2 - lon1)
    x = math.sin(delta_lambda) * math.cos(phi2)
    y = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(delta_lambda)
    theta = math.atan2(x, y)
    bearing = (math.degrees(theta) + 360) % 360
    return bearing

def angle_to_vector(deg):
    rad = math.radians(deg)
    return [math.cos(rad), math.sin(rad)]

def dotProduct(x, y):
    return np.dot(x, y)

def windDirectionCheck(bearingAngle, WindDirection):
    bearingAngleVector = angle_to_vector(bearingAngle)
    WindDirectionVector = angle_to_vector(WindDirection)
    alignment = dotProduct(bearingAngleVector, WindDirectionVector)
    return alignment > -0.1





if __name__ == "__main__":
    # This code will ONLY run when you call `python yup.py`
    user_input1 = input("Enter start city: ").strip().lower()
    user_input2 = input("Enter end city: ").strip().lower()

    lat1, lon1, urlStart = findUserCoords(user_input1)
    lat2, lon2, urlEnd = findUserCoords(user_input2)

    print(user_input1, 'has latitude', lat1, lon1)
    print(user_input2, 'has latitude', lat2, lon2)

    values = callAPI(urlStart)

    bearingAngle = round(findBearing(lat1, lon1, lat2, lon2), 2)
    print('bearing Angle', bearingAngle)

    if values['windDirection'] >= 180:
        WindDirection = values['windDirection'] - 180
    else:
        WindDirection = values['windDirection'] + 180

    check = windDirectionCheck(bearingAngle, WindDirection)
    print('check', check)

    # Your weather snapshot printing here
    print("📍 Weather Snapshot:")
    print(f"🌡️ Temp: {values['temperature']}°C (feels like {values['temperatureApparent']}°C)")
    print(f"💧 Humidity: {values['humidity']}%")
    print(f"💨 Wind: {values['windSpeed']} m/s, Gusts: {values['windGust']} m/s, Direction: {values['windDirection']}°")
    print(f"🌧️ Rain Intensity: {values['rainIntensity']} mm/h | Cloud Cover: {values['cloudCover']}%")
    print(f"🔍 Visibility: {values['visibility']} km")
    print(f"☁️ Cloud Base: {values['cloudBase']} km | Cloud Ceiling: {values['cloudCeiling']} km")
    print(f"🧪 Pressure: {values['pressureSeaLevel']} hPa (sea level)")

    conditionsOK = (
        (values['cloudBase'] is None or values['cloudBase'] > 1) and
        (values['cloudCeiling'] is None or values['cloudCeiling'] > 0.5) and
        (values['rainIntensity'] is None or values['rainIntensity'] < 0.1) and
        (values['sleetIntensity'] is None or values['sleetIntensity'] < 0.1) and
        (values['snowIntensity'] is None or values['snowIntensity'] < 0.1) and
        (values['temperature'] is None or values['temperature'] > 2) and
        (values['visibility'] is None or values['visibility'] > 2) and
        (values['windSpeed'] is None or values['windSpeed'] < 40)
    )

    if conditionsOK:
        if check == False and values['windSpeed'] < 10:
            print('\nToday is a great day to cycle')
        elif check == True:
            print("\nToday is a great day to cycle")
        else:
            print("\nIt's jover, don't go out")
    else:
        print("\nIt's jover, don't go out")
