"""Tool to track how many calories were burned from simple inputs.
Also stores the data on a file"""

from datetime import datetime
from pip._vendor import requests
import data

GENDER = data.GENDER
WEIGHT = data.WEIGHT
HEIGHT = data.HEIGHT
AGE = data.AGE

APP_ID = data.APP_ID
API_KEY = data.API_KEY

exercise_text = input("Tell me which exercises you did: ")
EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}
parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE
}

response = requests.post(url=EXERCISE_ENDPOINT, json=parameters, headers=headers)
result = response.json()
print(result)
EXERCISE_ENTRY = 0

for entry in result:
    while EXERCISE_ENTRY <= len(result["exercises"]) -1:
        duration = result["exercises"][EXERCISE_ENTRY]["duration_min"]
        exercise_name = result["exercises"][EXERCISE_ENTRY]["name"]
        calories = result["exercises"][EXERCISE_ENTRY]["nf_calories"]
        EXERCISE_ENTRY += 1

        today = datetime.now()
        date = today.strftime('%d/%m/%Y')
        time = today.strftime('%H:%M:%S')

        SHEETY_ENDPOINT = "https://api.sheety.co/3321d2040411eefb1d6e1f43a17d5bed/myWorkouts/workouts"
        parameters = {
            "workout": {
                "date": date,
                "time": time,
                "exercise": exercise_name.title(),
                "duration": duration,
                "calories": calories
            }
        }

        response = requests.post(url=SHEETY_ENDPOINT, json=parameters, headers=headers)
        print(response.text)
