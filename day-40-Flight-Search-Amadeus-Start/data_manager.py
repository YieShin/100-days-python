import os
from pprint import pprint

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

# Load environment variables from .env file
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))


class DataManager:

    def __init__(self):
        self._user = os.environ["DAY_40_FLIGHT_SEARCH_AMADEUS_START_SHEETY_USERS_ENDPOINT"]
        self._password = os.environ["DAY_40_FLIGHT_SEARCH_AMADEUS_START_SHEETY_PASSWORD"]
        self._authorization = HTTPBasicAuth(self._user, self._password)
        self.prices_endpoint = os.environ["DAY_40_FLIGHT_SEARCH_AMADEUS_START_SHEETY_PRICES_ENDPOINT"]
        self.users_endpoint = os.environ["DAY_40_FLIGHT_SEARCH_AMADEUS_START_SHEETY_USERS_ENDPOINT"]
        self.destination_data = {}
        self.customer_data = {}

    def get_destination_data(self):
        # Use the Sheety API to GET all the data in that sheet and print it out.
        response = requests.get(url=self.sheety_price_endpoint, auth=self._authorization)
        data = response.json()
        pprint(data)
        self.destination_data = data["prices"]
        # Try importing pretty print and printing the data out again using pprint() to see it formatted.

        return self.destination_data

    # In the DataManager Class make a PUT request and use the row id from sheet_data
    # to update the Google Sheet with the IATA codes. (Do this using code).
    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{self.sheety_price_endpoint}/{city['id']}",
                json=new_data
            )
            print(response.text)

    def get_customer_emails(self):
        response = requests.get(url=self.sheety_user_endpoint, auth=self._authorization)
        data = response.json()
        print(data)
        self.customer_data = data["users"]
        return self.customer_data
