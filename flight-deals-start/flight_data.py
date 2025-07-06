class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self, lowest_price):
        self.lowest_price = lowest_price

    def json_flight_data(self):
        json = {
            "price": {
                "lowestPrice": self.lowest_price,
            }
        }
        return json
