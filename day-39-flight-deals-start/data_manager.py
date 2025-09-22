import os
import requests
from dotenv import load_dotenv
from flight_data import FlightData
from requests.auth import HTTPBasicAuth


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

SHEETY_PRICES_ENDPOINT = os.getenv("DAY_39_FLIGHT_DEALS_START_SHEETY_ENDPOINT")


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self._user = os.environ["DAY_39_FLIGHT_DEALS_START_SHEETY_USERNAME"]
        self._password = os.environ["DAY_39_FLIGHT_DEALS_START_SHEETY_PASSWORD"]
        self._authorization = HTTPBasicAuth(self._user, self._password)
        self.destination_data = {}
        # self.sheety_header = {"Authorization": os.getenv("SHEETY_HEADERS")}

    def get_destination_data(self):
        # 2. Use the Sheety API to GET all the data in that sheet and print it out.
        response = requests.get(url=SHEETY_PRICES_ENDPOINT, auth=self._authorization)
        data = response.json()
        self.destination_data = data["prices"]
        # 3. Try importing pretty print and printing the data out again using pprint() to see it formatted.
        # pprint(data)
        return self.destination_data

    # 6. In the DataManager Class make a PUT request and use the row id from sheet_data
    # to update the Google Sheet with the IATA codes. (Do this using code).
    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_PRICES_ENDPOINT}/{city['id']}",
                json=new_data,
                auth=self._authorization
            )
            print(response.text)

    # SHIN'S CODE
    # def get_google_sheet(self):
    #     get_response = requests.get(url=self.endpoint, auth=self._authorization)
    #     return get_response.json()
    #
    # def get_iata_list(self):
    #     iata_code_list = []
    #     for item in self.get_google_sheet()["prices"]:
    #         iata_code_list.append(item["iataCode"])
    #
    #     return iata_code_list
    #
    # def edit_google_sheet(self, lowest_price, row_id):
    #     flight_data = FlightData(lowest_price=lowest_price)
    #     new_data = flight_data.json_flight_data()
    #     requests.put(url=f"{self.endpoint}/{row_id}", json=new_data, headers=self.sheety_header)