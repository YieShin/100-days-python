import os
from datetime import datetime
import requests
from dotenv import load_dotenv


load_dotenv()
APP_ID = os.getenv("APP_ID")
API_KEY = os.getenv("API_KEY")

GENDER = "Male"
WEIGHT = "65"
HEIGHT = "170"
AGE = "40"

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
exercise_text = input("Tell me which exercise you did? ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE,

}

response = requests.post(url=exercise_endpoint, json=parameters, headers=headers)
result = response.json()
print(result)

SHEETY_ENDPOINT = os.getenv("SHEETY_ENDPOINT")

SHEETY_HEADERS = {"Authorization": os.getenv("SHEETY_HEADERS")}
sheety_get_response = requests.get(url=SHEETY_ENDPOINT)
# print(sheety_get_response.json())

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

# sheety_post_response = requests.post(url=SHEETY_ENDPOINT, json=sheet_inputs, headers=SHEETY_HEADERS)
# print(sheety_post_response.text)
