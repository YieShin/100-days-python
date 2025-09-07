import requests
from datetime import date, timedelta

USERNAME = "shintracker"
TOKEN = "thisissecretcode"
GRAPH_ID = "graph1"
pixela_endpoint = "https://pixe.la/v1/users"

user_params = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

# response = requests.post(url=pixela_endpoint, json=user_params)
# print(response.text)

graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"

graph_config = {
    "id": "graph1",
    "name": "Python Learning Graph",
    "unit": "Min",
    "type": "int",
    "color": "sora",
}

headers = {
    "X-USER-TOKEN": TOKEN,
}

# response = requests.post(url=graph_endpoint, json=graph_config, headers=headers)
# print(response.text)
today = date.today()
yesterday = today - timedelta(days=1)

pixel_creation_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}"
pixel_data = {
    "date": today.strftime("%Y%m%d"),
    "quantity": input("How long time did you study Python today? "),
}

response = requests.post(url=pixel_creation_endpoint, json=pixel_data, headers=headers)
print(response.text)

update_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{today.strftime("%Y%m%d")}"
# response = requests.put(url=graph1_endpoint, json=pixel_data, headers=headers)
# print(response.text)
delete_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs/{GRAPH_ID}/{today.strftime("%Y%m%d")}"
# response = requests.del(url=graph1_endpoint, json=pixel_data, headers=headers)
# print(response.text)