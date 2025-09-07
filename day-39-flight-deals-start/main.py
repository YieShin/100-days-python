from flight_search import FlightSearch
from data_manager import DataManager
from datetime import datetime, timedelta
from pprint import pprint

# DATE PICKER, DATE CONFIGURATOR
day_picker = datetime(2025, 9, 1)
depart_date = day_picker.date()
new_datetime = depart_date + timedelta(days=5)

# FLIGHT SEARCH
flight_details = FlightSearch(depart_date=(depart_date, new_datetime), adults=2, destination="PEK")
flight_result = flight_details.search_flight()
print(flight_result["data"][0]["price"]["grandTotal"])

# GET IATA CODE TO LIST
data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
pprint(sheet_data)


# for item in sheet_data["prices"]:
#     iata_code = item["iataCode"]
#     google_price = item["lowestPrice"]
#     flight_details = FlightSearch(depart_date=(depart_date, new_datetime), adults=1, destination=iata_code)
#
#     flight_result = flight_details.search_flight()
#     current_price = flight_result["data"][0]["price"]["grandTotal"]
#
#     if float(current_price) < float(google_price):
#         edit_google_sheet = data_manager.edit_google_sheet(lowest_price=current_price, row_id=row_id)
#         print(f"{iata_code} got low price!")




