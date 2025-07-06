import time
from datetime import datetime, timedelta

from data_manager import DataManager
from flight_data import find_cheapest_flight
from flight_search import FlightSearch
from notification_manager import NotificationManager

# ==================== Set up the Flight Search ====================

data_manager = DataManager()
# sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
notification_manager = NotificationManager()

# Set your origin airport
ORIGIN_CITY_IATA = "KUL"

# ==================== Update the Airport Codes in Google Sheet ====================

# for row in sheet_data:
#     if row["iataCode"] == "":
#         row["iataCode"] = flight_search.get_destination_code(row["city"])
#         # slowing down requests to avoid rate limit
#         time.sleep(2)
# print(f"sheet_data:\n {sheet_data}")

# SHEETY USAGE if there's no update in IATA CODE don't use this
# data_manager.destination_data = sheet_data
# data_manager.update_destination_codes()

# ==================== Search for Flights and Send Notifications ====================

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))

# Dummy sheet_data
dummy_sheet_data = [{'city': 'Tokyo', 'iataCode': 'TYO', 'lowestPrice': '775.00', 'id': 2},
                    {'city': 'Hong Kong', 'iataCode': 'HKG', 'lowestPrice': '339.00', 'id': 3},
                    {'city': 'Beijing', 'iataCode': 'BJS', 'lowestPrice': '588.00', 'id': 4},
                    {'city': 'Seoul', 'iataCode': 'SEL', 'lowestPrice': '626.00', 'id': 5},
                    {'city': 'Shanghai', 'iataCode': 'SHA', 'lowestPrice': '762.00', 'id': 6}]

# TODO Replace dummy_sheet_data
for destination in dummy_sheet_data:
    print(f"Getting flights for {destination['city']}...")
    flights = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )
    cheapest_flight = find_cheapest_flight(flights)
    print(f"{destination['city']}: RM{cheapest_flight.price}")
    # Slowing down requests to avoid rate limit
    time.sleep(2)

    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        print(f"Lower price flight found to {destination['city']}!")
        # notification_manager.send_sms(
        #     message_body=f"Low price alert! Only £{cheapest_flight.price} to fly "
        #                  f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
        #                  f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        # )
        # SMS not working? Try whatsapp instead.
        # notification_manager.send_whatsapp(
        #     message_body=f"Low price alert! Only £{cheapest_flight.price} to fly "
        #                  f"from {cheapest_flight.origin_airport} to {cheapest_flight.destination_airport}, "
        #                  f"on {cheapest_flight.out_date} until {cheapest_flight.return_date}."
        # )
