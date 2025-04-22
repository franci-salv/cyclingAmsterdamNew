import requests
import json



import requests

def callAPI():
    url = "https://api.tomorrow.io/v4/weather/realtime?location=austin&apikey=h75GN8Qsauua0KkdNNq2QJtvpOYFyTEn"
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


try:
    values = callAPI()
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")




# Format it cleanly
print("📍 Weather Snapshot:")
print(f"🌡️ Temp: {values['temperature']}°C (feels like {values['temperatureApparent']}°C)")
print(f"💧 Humidity: {values['humidity']}%")
print(f"💨 Wind: {values['windSpeed']} m/s, Gusts: {values['windGust']} m/s, Direction: {values['windDirection']}°")
print(f"🌧️ Rain Intensity: {values['rainIntensity']} mm/h | Cloud Cover: {values['cloudCover']}%")
print(f"🔍 Visibility: {values['visibility']} km")
print(f"☁️ Cloud Base: {values['cloudBase']} km | Cloud Ceiling: {values['cloudCeiling']} km")
print(f"🧪 Pressure: {values['pressureSeaLevel']} hPa (sea level)")

# Add logic to say whether it's good for cycling:
if  values['cloudBase']> 1 and values['cloudCeiling']>0.5 and values['rainIntensity']<0.1 and values['sleetIntensity']< 0.1 and values['snowIntensity']< 0.1 and values['temperature']>2 and values['visibility']>3 and values['windSpeed']< 40: #direction need to be added
    print("\nToday is a great day to cycle")
else:
    print("\nits jover dont go out")


