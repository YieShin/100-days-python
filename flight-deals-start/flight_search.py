import os

import requests
from dotenv import load_dotenv

load_dotenv()


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.

    def __init__(self, depart_date, adults=1, departure="KUL", destination="NTR"):
        self.token_api_key = os.getenv('AMA_API_KEY')
        self.token_api_secret = os.getenv('AMA_API_SECRET')
        self.adults = adults
        self.depart_date = depart_date
        self.flight_offer_response = None
        self.iata_departure_code = departure
        self.iata_destination_code = destination
        self._token = self._bearer_token()

    def _bearer_token(self):
        auth_token_endpoint = "https://test.api.amadeus.com/v1/security/oauth2/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": self.token_api_key,
            "client_secret": self.token_api_secret
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        amadeus_response = requests.post(url=auth_token_endpoint, data=data, headers=headers)
        return amadeus_response.json()["access_token"]

    def get_destination_code(self, city_name):
        iata_code_endpoint = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
        query = {
            "keyword": city_name,
            "max": 2,
            "include": ["AIRPORTS"],
        }
        headers = {"Authorization": f"Bearer {self._token}"}
        response = requests.get(url=iata_code_endpoint, params=query, headers=headers)

        try:
            code = response.json()["data"][0]['iataCode']
            return code
        except requests.exceptions.HTTPError as e:
            # Handle HTTP errors (e.g., 404 Not Found, 500 Internal Server Error)
            print(f"HTTP Error: {e}")
            return None

    def search_flight(self):
        flight_offer_endpoint = "https://test.api.amadeus.com/v2/shopping/flight-offers"
        access_token_headers = {"Authorization": f"Bearer {self._bearer_token()}"}

        flight_offer_params = {
            "originLocationCode": "KUL",
            "destinationLocationCode": self.iata_destination_code,
            "departureDate": self.depart_date,
            "currencyCode": "MYR",
            "adults": self.adults,
            "max": 50,
        }

        self.flight_offer_response = requests.get(url=flight_offer_endpoint, params=flight_offer_params,
                                                  headers=access_token_headers)
        return self.flight_offer_response.json()
