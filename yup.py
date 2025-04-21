import requests
import json


url = "https://api.tomorrow.io/v4/weather/realtime?location=amsterdam&apikey=h75GN8Qsauua0KkdNNq2QJtvpOYFyTEn"



headers = {
    "accept": "application/json",
    "accept-encoding": "deflate, gzip, br"
}

response = requests.get(url, headers=headers)

print(response.text)


# Sample API response (replace this with your actual `response.json()`)
data = response.json()

values = data["data"]["values"]

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
if values['windSpeed'] > 8 or values['rainIntensity'] > 0.5 or values['precipitationProbability'] > 50:
    print("\n🚫 Not ideal for cycling today. Stay cozy 😕")
else:
    print("\n✅ Great day to cycle! Go enjoy the ride 🚴‍♂️")
