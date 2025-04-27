from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from yup import findUserCoords, findBearing, callAPI, windDirectionCheck  # Your functions!

app = FastAPI()

# Allow frontend to talk to backend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Server is running!"}

@app.post("/checkweather")
async def check_weather(start_city: str = Form(...), start_country: str = Form(...), end_city: str = Form(...), end_country: str = Form(...)):
    # Find coords
    lat1, lon1, _ = findUserCoords((start_city.lower(), start_country.lower()))
    lat2, lon2, _ = findUserCoords((end_city.lower(), end_country.lower()))

    # Weather at start
    url_start = f"https://api.tomorrow.io/v4/weather/realtime?location={lat1},{lon1}&apikey=h75GN8Qsauua0KkdNNq2QJtvpOYFyTEn"
    values = callAPI(url_start)

    # Your cycling logic here
    bearingAngle = findBearing(lat1, lon1, lat2, lon2)
    
    if values['windDirection'] >= 180:
        WindDirection = values['windDirection'] - 180
    else:
        WindDirection = values['windDirection'] + 180

    check = windDirectionCheck(bearingAngle, WindDirection)

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

    if conditionsOK and (check or values['windSpeed'] < 10):
        recommendation = "Today is a great day to cycle!"
    else:
        recommendation = "It's not a good day to cycle."

    return {"recommendation": recommendation, "weather": values}
